import json
import os
import sys
import base64
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import requests
from outerbounds._vendor import click
from ..utils import metaflowconfig
from ..utils.schema import (
    CommandStatus,
    OuterboundsCommandResponse,
    OuterboundsCommandStatus,
)


class IntegrationOperation(str, Enum):
    """Enum for integration operations."""

    CREATE = "create"
    UPDATE = "update"


@click.group()
def cli(**kwargs):
    pass


@click.group(help="Manage resource integrations")
def integrations(**kwargs):
    pass


def get_integration_api_url(config_dir: str, profile: str, perimeter_id: str) -> str:
    """Constructs the API URL for resource integrations."""
    api_url = metaflowconfig.get_sanitized_url_from_config(
        config_dir, profile, "OBP_API_SERVER"
    )
    return f"{api_url}/v1/perimeters/{perimeter_id}/resourceintegrations"


def get_auth_headers(config_dir: str, profile: str) -> Dict[str, str]:
    """Returns headers with the metaflow token."""
    token = metaflowconfig.get_metaflow_token_from_config(config_dir, profile)
    return {
        "x-api-key": token,
        "Content-Type": "application/json",
    }


def get_current_perimeter(config_dir: str, profile: str) -> str:
    """Helper to get the current perimeter from config."""
    path_to_config = metaflowconfig.get_ob_config_file_path(config_dir, profile)
    if not os.path.exists(path_to_config):
        return ""

    with open(path_to_config, "r") as file:
        ob_config_dict = json.load(file)
    return ob_config_dict.get("OB_CURRENT_PERIMETER", "")


def get_cloud_provider_from_backend_type(backend_type: str) -> Optional[str]:
    """Get the cloud provider from the secret backend type."""
    if backend_type == "aws-secrets-manager":
        return "aws"
    elif backend_type == "gcp-secret-manager":
        return "gcp"
    elif backend_type == "az-key-vault":
        return "azure"
    return None


def get_cloud_credentials(
    config_dir: str, profile: str, cloud_provider: str
) -> Optional[Dict[str, Any]]:
    """Get temporary cloud credentials from the auth server."""
    token = metaflowconfig.get_metaflow_token_from_config(config_dir, profile)
    auth_url = metaflowconfig.get_sanitized_url_from_config(
        config_dir, profile, "OBP_AUTH_SERVER"
    )

    try:
        response = requests.get(
            f"{auth_url}/generate/{cloud_provider}",
            headers={"x-api-key": token},
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        click.secho(
            f"Failed to get {cloud_provider} credentials: {str(e)}", fg="red", err=True
        )
        return None


def fetch_secret_from_aws(
    secret_arn: str, credentials: Dict[str, Any]
) -> Optional[Dict[str, str]]:
    """Fetch secret value from AWS Secrets Manager."""
    try:
        import boto3
        from botocore.exceptions import ClientError

        # The credentials from /generate/aws contain role_arn and token
        # We need to assume the role using the web identity token
        role_arn = credentials.get("role_arn")
        web_identity_token = credentials.get("token")
        region = credentials.get("region", "us-east-1")

        if not role_arn or not web_identity_token:
            click.secho("Invalid AWS credentials format", fg="red", err=True)
            return None

        # Use STS to assume role with web identity
        sts_client = boto3.client("sts", region_name=region)
        assumed_role = sts_client.assume_role_with_web_identity(
            RoleArn=role_arn,
            RoleSessionName="outerbounds-cli-secrets",
            WebIdentityToken=web_identity_token,
        )

        # Create a new session with the assumed role credentials
        session = boto3.Session(
            aws_access_key_id=assumed_role["Credentials"]["AccessKeyId"],
            aws_secret_access_key=assumed_role["Credentials"]["SecretAccessKey"],
            aws_session_token=assumed_role["Credentials"]["SessionToken"],
            region_name=region,
        )

        client = session.client("secretsmanager")
        response = client.get_secret_value(SecretId=secret_arn)

        if "SecretBinary" in response:
            secret_data = json.loads(response["SecretBinary"])
        else:
            secret_data = json.loads(response["SecretString"])

        return secret_data
    except ImportError:
        click.secho(
            "boto3 is required to fetch AWS secrets. Install it with: pip install boto3",
            fg="yellow",
            err=True,
        )
        return None
    except ClientError as e:
        click.secho(f"Failed to fetch secret from AWS: {str(e)}", fg="red", err=True)
        return None
    except Exception as e:
        click.secho(f"Error fetching AWS secret: {str(e)}", fg="red", err=True)
        return None


def fetch_secret_from_gcp(
    secret_name: str, credentials: Dict[str, Any]
) -> Optional[Dict[str, str]]:
    """Fetch secret value from GCP Secret Manager."""
    try:
        from google.cloud import secretmanager  # type: ignore[import-untyped]
        from google.auth import identity_pool  # type: ignore[import-untyped]
        import tempfile

        # The credentials from /generate/gcp use workload identity federation
        jwt_token = credentials.get("token")
        project_number = credentials.get("gcpProjectNumber")
        workload_pool = credentials.get("gcpWorkloadIdentityPool")
        workload_provider = credentials.get("gcpWorkloadIdentityPoolProvider")
        service_account_email = credentials.get("gcpServiceAccountEmail")

        if not all(
            [
                jwt_token,
                project_number,
                workload_pool,
                workload_provider,
                service_account_email,
            ]
        ):
            click.secho("Invalid GCP credentials format", fg="red", err=True)
            return None

        # Write the JWT token to a temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as token_file:
            token_file.write(jwt_token or "")
            token_file_path = token_file.name

        # Create external account credentials config
        external_account_config = {
            "type": "external_account",
            "audience": f"//iam.googleapis.com/projects/{project_number}/locations/global/workloadIdentityPools/{workload_pool}/providers/{workload_provider}",
            "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
            "token_url": "https://sts.googleapis.com/v1/token",
            "service_account_impersonation_url": f"https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/{service_account_email}:generateAccessToken",
            "credential_source": {"file": token_file_path},
        }

        # Create a temporary file with the external account credentials
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as config_file:
            json.dump(external_account_config, config_file)
            config_file_path = config_file.name

        try:
            # Create credentials from the external account config
            creds = identity_pool.Credentials.from_file(config_file_path)

            # Create the Secret Manager client with these credentials
            client = secretmanager.SecretManagerServiceClient(credentials=creds)
            response = client.access_secret_version(
                request={"name": f"{secret_name}/versions/latest"}
            )
            secret_data = json.loads(response.payload.data)

            return secret_data
        finally:
            # Clean up temporary files
            if os.path.exists(token_file_path):
                os.unlink(token_file_path)
            if os.path.exists(config_file_path):
                os.unlink(config_file_path)
    except ImportError:
        click.secho(
            "google-cloud-secret-manager is required to fetch GCP secrets. Install it with: pip install google-cloud-secret-manager",
            fg="yellow",
            err=True,
        )
        return None
    except Exception as e:
        click.secho(f"Error fetching GCP secret: {str(e)}", fg="red", err=True)
        return None


def fetch_secret_from_azure(
    secret_url: str, credentials: Dict[str, Any]
) -> Optional[Dict[str, str]]:
    """Fetch secret value from Azure Key Vault."""
    try:
        from azure.keyvault.secrets import SecretClient  # type: ignore[import-not-found]
        from azure.identity import ClientAssertionCredential  # type: ignore[import-not-found]
        from urllib.parse import urlparse
        import tempfile

        # Parse vault URL from the secret URL
        parsed = urlparse(secret_url)
        vault_url = f"{parsed.scheme}://{parsed.netloc}"
        secret_name = parsed.path.split("/")[-1] if parsed.path else ""

        # The credentials from /generate/azure contain a JWT token for workload identity
        tenant_id = credentials.get("azureTenantId")
        client_id = credentials.get("azureClientId")
        jwt_token = credentials.get("token")
        authority_host = credentials.get(
            "azureAuthorityHost", "login.microsoftonline.com"
        )

        if not tenant_id or not client_id or not jwt_token:
            click.secho("Invalid Azure credentials format", fg="red", err=True)
            return None

        # Create a credential using the JWT token
        def token_callback():
            return jwt_token

        credential = ClientAssertionCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            func=token_callback,
            authority=f"https://{authority_host}",
        )

        client = SecretClient(vault_url=vault_url, credential=credential)
        secret = client.get_secret(secret_name)
        secret_data = json.loads(secret.value)

        return secret_data
    except ImportError:
        click.secho(
            "azure-keyvault-secrets and azure-identity are required to fetch Azure secrets. Install them with: pip install azure-keyvault-secrets azure-identity",
            fg="yellow",
            err=True,
        )
        return None
    except Exception as e:
        click.secho(f"Error fetching Azure secret: {str(e)}", fg="red", err=True)
        return None


def get_integrations_url(config_dir: str, profile: str) -> Optional[str]:
    """Get the integrations URL from config."""
    try:
        # Try to get from environment variable first
        integrations_url = os.environ.get("OBP_INTEGRATIONS_URL")
        if integrations_url:
            return integrations_url

        # Try to construct it from the API server URL
        api_url = metaflowconfig.get_sanitized_url_from_config(
            config_dir, profile, "OBP_API_SERVER"
        )
        if api_url:
            # The integrations URL is the same as the API server URL
            return api_url

        return None
    except Exception as e:
        return None


def fetch_integration_secret_metadata(
    integration_name: str, perimeter: str, config_dir: str, profile: str
) -> Optional[Tuple[str, str]]:
    """Fetch secret metadata (resource ID and backend type) from the integrations API."""
    try:
        integrations_url = get_integrations_url(config_dir, profile)
        if not integrations_url:
            click.secho(
                "Could not determine integrations URL from config",
                fg="yellow",
                err=True,
            )
            return None

        # Call the secrets metadata endpoint
        metadata_url = f"{integrations_url}/integrations/secrets/metadata"
        headers = get_auth_headers(config_dir, profile)

        payload = {
            "perimeter_name": perimeter,
            "integration_name": integration_name,
        }

        res = requests.get(metadata_url, json=payload, headers=headers)
        res.raise_for_status()

        data = res.json()
        secret_resource_id = data.get("secret_resource_id")
        secret_backend_type = data.get("secret_backend_type")

        if not secret_resource_id or not secret_backend_type:
            click.secho(
                "Invalid response from secrets metadata API", fg="yellow", err=True
            )
            return None

        return (secret_resource_id, secret_backend_type)

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            click.secho(
                f"Integration '{integration_name}' not found or has no secrets",
                fg="yellow",
                err=True,
            )
        else:
            click.secho(
                f"API error: {e.response.status_code} - {e.response.text}",
                fg="red",
                err=True,
            )
        return None
    except Exception as e:
        click.secho(f"Error fetching secret metadata: {str(e)}", fg="red", err=True)
        return None


def fetch_integration_secret_values(
    integration_name: str, perimeter: str, config_dir: str, profile: str
) -> Optional[Dict[str, str]]:
    """Fetch secret values for an integration."""
    try:
        # Get secret metadata from the integrations API
        metadata = fetch_integration_secret_metadata(
            integration_name, perimeter, config_dir, profile
        )
        if not metadata:
            return None

        secret_resource_id, secret_backend_type = metadata

        # Determine cloud provider from the backend type
        cloud_provider = get_cloud_provider_from_backend_type(secret_backend_type)
        if not cloud_provider:
            click.secho(
                f"Unsupported secret backend type: {secret_backend_type}",
                fg="yellow",
                err=True,
            )
            return None

        # Get credentials for the cloud provider
        credentials = get_cloud_credentials(config_dir, profile, cloud_provider)
        if not credentials:
            return None

        # Fetch the secret based on the backend type
        if secret_backend_type == "aws-secrets-manager":
            return fetch_secret_from_aws(secret_resource_id, credentials)
        elif secret_backend_type == "gcp-secret-manager":
            return fetch_secret_from_gcp(secret_resource_id, credentials)
        elif secret_backend_type == "az-key-vault":
            return fetch_secret_from_azure(secret_resource_id, credentials)
        else:
            click.secho(
                f"Unsupported secret backend type: {secret_backend_type}",
                fg="yellow",
                err=True,
            )
            return None

    except Exception as e:
        click.secho(f"Error fetching integration secret: {str(e)}", fg="red", err=True)
        return None


def handle_api_error(
    e: Exception, step: CommandStatus, response: OuterboundsCommandResponse, output: str
):
    """Handles API errors and updates the response object."""
    click.secho(f"API Request Failed: {e}", fg="red", err=True)
    if isinstance(e, requests.exceptions.HTTPError):
        try:
            error_details = e.response.json()
            click.secho(
                f"Details: {json.dumps(error_details, indent=2)}", fg="red", err=True
            )
        except Exception:
            click.secho(f"Response content: {e.response.text}", fg="red", err=True)

    step.update(
        status=OuterboundsCommandStatus.FAIL,
        reason=f"API Request Failed: {str(e)}",
        mitigation="Check your network connection, authentication token, and permissions.",
    )
    response.add_step(step)
    if output == "json":
        click.echo(json.dumps(response.as_dict(), indent=4))
    sys.exit(1)


@integrations.command(name="list", help="List all resource integrations in a perimeter")
@click.option(
    "--perimeter",
    help="Perimeter ID. Defaults to the currently active perimeter.",
)
@click.option(
    "-d",
    "--config-dir",
    default=os.path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default=os.environ.get("METAFLOW_PROFILE", ""),
    help="The named metaflow profile",
)
@click.option(
    "-o",
    "--output",
    default="",
    help="Show output in the specified format.",
    type=click.Choice(["json", ""]),
)
def _list(perimeter=None, config_dir=None, profile=None, output=""):
    response = OuterboundsCommandResponse()
    step = CommandStatus(
        "ListIntegrations",
        OuterboundsCommandStatus.OK,
        "Successfully listed integrations.",
    )

    if not perimeter:
        perimeter = get_current_perimeter(config_dir, profile)

    if not perimeter:
        click.secho(
            "No perimeter specified and no active perimeter found.", fg="red", err=True
        )
        sys.exit(1)

    try:
        url = get_integration_api_url(config_dir, profile, perimeter)
        headers = get_auth_headers(config_dir, profile)

        res = requests.get(url, headers=headers)
        res.raise_for_status()

        data = res.json()
        integrations_list = data.get("resource_integrations", [])

        # Filter out internal/aggregate integration types
        hidden_types = ["PRIVATE_PYPI_REPOSITORIES", "PRIVATE_CONDA_CHANNELS"]
        integrations_list = [
            i
            for i in integrations_list
            if i.get("integration_type") not in hidden_types
        ]

        if output == "json":
            response.add_or_update_data("integrations", integrations_list)
            response.add_step(step)
            click.echo(json.dumps(response.as_dict(), indent=4))
        else:
            if not integrations_list:
                click.secho("No integrations found.", fg="yellow", err=True)
            else:
                # Print table header
                click.echo(
                    f"{'NAME':<40} {'PERIMETER':<15} {'TYPE':<30} {'HAS_SECRET':<12} {'DESCRIPTION':<50}",
                    err=True,
                )

                # Print each integration
                for integ in integrations_list:
                    name = integ.get("integration_name", "")[:40]
                    integ_type = integ.get("integration_type", "")[:30]
                    description = integ.get("integration_description", "")[:50]
                    has_secrets = (
                        "Yes" if integ.get("integration_has_secrets", False) else "No"
                    )

                    click.echo(
                        f"{name:<40} {perimeter:<15} {integ_type:<30} {has_secrets:<12} {description:<50}",
                        err=True,
                    )

    except Exception as e:
        handle_api_error(e, step, response, output)


@integrations.command(help="Get a specific resource integration")
@click.argument("name")
@click.option(
    "--perimeter",
    help="Perimeter ID. Defaults to the currently active perimeter.",
)
@click.option(
    "-d",
    "--config-dir",
    default=os.path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default=os.environ.get("METAFLOW_PROFILE", ""),
    help="The named metaflow profile",
)
@click.option(
    "-o",
    "--output",
    default="",
    help="Show output in the specified format.",
    type=click.Choice(["json", ""]),
)
@click.option(
    "--show-secret-values",
    is_flag=True,
    default=False,
    help="Fetch and display secret values from the cloud provider.",
)
def get(
    name,
    perimeter=None,
    config_dir=None,
    profile=None,
    output="",
    show_secret_values=False,
):
    response = OuterboundsCommandResponse()
    step = CommandStatus(
        "GetIntegration",
        OuterboundsCommandStatus.OK,
        f"Successfully fetched integration {name}.",
    )

    if not perimeter:
        perimeter = get_current_perimeter(config_dir, profile)

    if not perimeter:
        click.secho(
            "No perimeter specified and no active perimeter found.", fg="red", err=True
        )
        sys.exit(1)

    try:
        url = f"{get_integration_api_url(config_dir, profile, perimeter)}/{name}"
        headers = get_auth_headers(config_dir, profile)

        res = requests.get(url, headers=headers)
        res.raise_for_status()

        data = res.json()

        # Fetch secret values if requested
        if show_secret_values and data.get("integration_secret_keys"):
            secret_values = fetch_integration_secret_values(
                name, perimeter, config_dir, profile
            )
            if secret_values:
                # Merge secret values into integration_secret_keys
                # Transform from list to dict with actual values
                data["integration_secret_keys"] = secret_values
            # If fetching failed, keep integration_secret_keys as a list

        if output == "json":
            response.add_or_update_data("integration", data)
            response.add_step(step)
            click.echo(json.dumps(response.as_dict(), indent=4))
        else:
            click.echo(json.dumps(data, indent=2))

    except Exception as e:
        handle_api_error(e, step, response, output)


@integrations.command(help="Delete a resource integration")
@click.argument("name")
@click.option(
    "--perimeter",
    help="Perimeter ID. Defaults to the currently active perimeter.",
)
@click.option(
    "-d",
    "--config-dir",
    default=os.path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default=os.environ.get("METAFLOW_PROFILE", ""),
    help="The named metaflow profile",
)
@click.option(
    "-o",
    "--output",
    default="",
    help="Show output in the specified format.",
    type=click.Choice(["json", ""]),
)
def delete(name, perimeter=None, config_dir=None, profile=None, output=""):
    response = OuterboundsCommandResponse()
    step = CommandStatus(
        "DeleteIntegration",
        OuterboundsCommandStatus.OK,
        f"Successfully deleted integration {name}.",
    )

    if not perimeter:
        perimeter = get_current_perimeter(config_dir, profile)

    if not perimeter:
        click.secho(
            "No perimeter specified and no active perimeter found.", fg="red", err=True
        )
        sys.exit(1)

    try:
        url = f"{get_integration_api_url(config_dir, profile, perimeter)}/{name}"
        headers = get_auth_headers(config_dir, profile)

        res = requests.delete(url, headers=headers)
        res.raise_for_status()

        click.secho(f"Integration {name} deleted successfully.", fg="green", err=True)
        response.add_step(step)

        if output == "json":
            click.echo(json.dumps(response.as_dict(), indent=4))

    except Exception as e:
        handle_api_error(e, step, response, output)


# Helper function to create standard options for all create/update commands
def common_integration_options(func):
    func = click.option(
        "--perimeter",
        help="Perimeter ID. Defaults to the currently active perimeter.",
    )(func)
    func = click.option(
        "-d",
        "--config-dir",
        default=os.path.expanduser(
            os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")
        ),
        help="Path to Metaflow configuration directory",
        show_default=True,
    )(func)
    func = click.option(
        "-p",
        "--profile",
        default=os.environ.get("METAFLOW_PROFILE", ""),
        help="The named metaflow profile",
    )(func)
    func = click.option(
        "-o",
        "--output",
        default="",
        help="Show output in the specified format.",
        type=click.Choice(["json", ""]),
    )(func)
    return func


def create_or_update_integration(
    operation: IntegrationOperation,
    name: str,
    integration_type: str,
    description: str,
    spec: Dict[str, Any],
    secrets: Dict[str, str],
    perimeter: Optional[str],
    config_dir: str,
    profile: str,
    output: str,
):
    """
    Generic handler for creating or updating an integration.
    """
    response = OuterboundsCommandResponse()
    step_name = (
        "CreateIntegration"
        if operation == IntegrationOperation.CREATE
        else "UpdateIntegration"
    )
    msg = f"Successfully {operation.value}d integration {name}."
    step = CommandStatus(step_name, OuterboundsCommandStatus.OK, msg)

    if not perimeter:
        perimeter = get_current_perimeter(config_dir, profile)

    if not perimeter:
        click.secho(
            "No perimeter specified and no active perimeter found.", fg="red", err=True
        )
        sys.exit(1)

    try:
        url = get_integration_api_url(config_dir, profile, perimeter)
        if operation == IntegrationOperation.UPDATE:
            url = f"{url}/{name}"

        headers = get_auth_headers(config_dir, profile)

        payload = {
            "integration_name": name,
            "integration_description": description,
            "integration_type": integration_type,
            "integration_status": "CREATED",
            "integration_spec": spec,
        }
        if secrets:
            import base64

            encoded_secrets = {}
            for k, v in secrets.items():
                if v:
                    encoded_secrets[k] = base64.b64encode(v.encode("utf-8")).decode(
                        "utf-8"
                    )
            payload["integration_secrets"] = encoded_secrets

        if operation == IntegrationOperation.CREATE:
            res = requests.post(url, headers=headers, json=payload)
        else:
            res = requests.put(url, headers=headers, json=payload)

        res.raise_for_status()

        data = res.json()
        click.secho(msg, fg="green", err=True)

        if output == "json":
            response.add_or_update_data("integration", data)
            response.add_step(step)
            click.echo(json.dumps(response.as_dict(), indent=4))

    except Exception as e:
        handle_api_error(e, step, response, output)


# ------------------------------------------------------------------------------
# Storage Integrations
# ------------------------------------------------------------------------------

# --- S3 Proxy ---
@integrations.group(
    name="s3-proxy",
    help="""
    This command is used to create an S3 Proxy integration, which will allow you to
    use your local Nebius or CoreWeave object storage service as your local caching storage
    when reading from or writing to AWS S3 buckets.

    Example usage:
        outerbounds integrations s3-proxy create --name my-s3-proxy --bucket-name my-bucket \\
            --endpoint-url https://my-bucket.s3.nebius.com --region us-central1 \\
            --access-key-id my-access-key --secret-access-key my-secret-access-key
    """,
)
def s3_proxy():
    pass


@s3_proxy.command(help="Create an S3 Proxy integration")
@click.argument("name")
@click.option("--description", help="Description of the integration", default="")
@click.option("--bucket-name", required=True, help="The S3 bucket name")
@click.option("--endpoint-url", required=True, help="The S3 endpoint URL")
@click.option("--region", required=True, help="The AWS region")
@click.option("--access-key-id", required=True, help="AWS Access Key ID")
@click.option("--secret-access-key", required=True, help="AWS Secret Access Key")
@common_integration_options
def create(  # type: ignore[no-redef]
    name,
    description,
    bucket_name,
    endpoint_url,
    region,
    access_key_id,
    secret_access_key,
    perimeter,
    config_dir,
    profile,
    output,
):
    spec = {
        "bucket_name": bucket_name,
        "endpoint_url": endpoint_url,
        "region": region,
    }
    secrets = {
        "access_key_id": access_key_id,
        "secret_access_key": secret_access_key,
    }
    create_or_update_integration(
        IntegrationOperation.CREATE,
        name,
        "S3_PROXY",
        description,
        spec,
        secrets,
        perimeter,
        config_dir,
        profile,
        output,
    )


@s3_proxy.command(help="Update an S3 Proxy integration")
@click.argument("name")
@click.option("--description", help="Description of the integration")
@click.option("--bucket-name", help="The S3 bucket name")
@click.option("--endpoint-url", help="The S3 endpoint URL")
@click.option("--region", help="The AWS region")
@click.option("--access-key-id", help="AWS Access Key ID")
@click.option("--secret-access-key", help="AWS Secret Access Key")
@common_integration_options
def update(  # type: ignore[no-redef]
    name,
    description,
    bucket_name,
    endpoint_url,
    region,
    access_key_id,
    secret_access_key,
    perimeter,
    config_dir,
    profile,
    output,
):
    if not perimeter:
        perimeter = get_current_perimeter(config_dir, profile)

    url = f"{get_integration_api_url(config_dir, profile, perimeter)}/{name}"
    headers = get_auth_headers(config_dir, profile)
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    existing = res.json()

    spec = existing.get("integration_spec", {})
    if bucket_name:
        spec["bucket_name"] = bucket_name
    if endpoint_url:
        spec["endpoint_url"] = endpoint_url
    if region:
        spec["region"] = region

    if description is None:
        description = existing.get("integration_description", "")

    secrets = {}
    if access_key_id:
        secrets["access_key_id"] = access_key_id
    if secret_access_key:
        secrets["secret_access_key"] = secret_access_key

    create_or_update_integration(
        IntegrationOperation.UPDATE,
        name,
        "S3_PROXY",
        description,
        spec,
        secrets,
        perimeter,
        config_dir,
        profile,
        output,
    )


# ------------------------------------------------------------------------------
# Artifacts & Packages Integrations
# ------------------------------------------------------------------------------

# --- Code Artifacts ---
@integrations.group(
    name="code-artifacts",
    help="""
    This command is used to create a CodeArtifacts integration, which will allow Fast Bakery to download package from
    your AWS CodeArtifacts private repositories.
    Once you have created this integrations, make sure you add all the pypi repositories hosed by this Code Artifacts
    instance to the Private PyPI Repositories integration.

    Example usage:
        outerbounds integrations code-artifacts create my-code-artifacts --domain my-domain --domain-owner 123456789012 --aws-region us-west-2 --target-role arn:aws:iam::123456789012:role/my-role
    """,
)
def code_artifacts():
    pass


@code_artifacts.command(help="Create an AWS CodeArtifacts integration")
@click.argument("name")
@click.option("--description", help="Description of the integration", default="")
@click.option("--domain", required=True, help="CodeArtifacts Domain")
@click.option(
    "--domain-owner", required=True, help="CodeArtifacts Domain Owner (AWS Account ID)"
)
@click.option("--aws-region", required=True, help="AWS Region")
@click.option("--target-role", help="Target IAM Role ARN")
@common_integration_options
def create(  # type: ignore[no-redef]
    name,
    description,
    domain,
    domain_owner,
    aws_region,
    target_role,
    perimeter,
    config_dir,
    profile,
    output,
):
    # Set use_target_role based on whether target_role is provided
    use_target_role = target_role is not None

    spec = {
        "domain_name": domain,
        "domain_owner": domain_owner,
        "aws_region": aws_region,
        "use_target_role": use_target_role,
    }
    if target_role:
        spec["target_role"] = target_role
    create_or_update_integration(
        IntegrationOperation.CREATE,
        name,
        "CODE_ARTIFACTS",
        description,
        spec,
        {},
        perimeter,
        config_dir,
        profile,
        output,
    )


@code_artifacts.command(help="Update an AWS CodeArtifacts integration")
@click.argument("name")
@click.option("--description", help="Description of the integration")
@click.option("--domain", help="CodeArtifacts Domain")
@click.option("--domain-owner", help="CodeArtifacts Domain Owner (AWS Account ID)")
@click.option("--aws-region", help="AWS Region")
@click.option("--target-role", help="Target IAM Role ARN")
@common_integration_options
def update(  # type: ignore[no-redef]
    name,
    description,
    domain,
    domain_owner,
    aws_region,
    target_role,
    perimeter,
    config_dir,
    profile,
    output,
):
    if not perimeter:
        perimeter = get_current_perimeter(config_dir, profile)

    url = f"{get_integration_api_url(config_dir, profile, perimeter)}/{name}"
    headers = get_auth_headers(config_dir, profile)
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    existing = res.json()

    spec = existing.get("integration_spec", {})
    if domain:
        spec["domain_name"] = domain
    if domain_owner:
        spec["domain_owner"] = domain_owner
    if aws_region:
        spec["aws_region"] = aws_region
    if target_role is not None:
        spec["target_role"] = target_role
        # Set use_target_role based on whether target_role is provided
        spec["use_target_role"] = True
    else:
        # If updating without target_role, set use_target_role to False
        spec["use_target_role"] = False

    if description is None:
        description = existing.get("integration_description", "")

    create_or_update_integration(
        IntegrationOperation.UPDATE,
        name,
        "CODE_ARTIFACTS",
        description,
        spec,
        {},
        perimeter,
        config_dir,
        profile,
        output,
    )


# --- Artifactory ---
@integrations.group(
    name="artifactory",
    help="""
    This command is used to create an Artifactory integration, which will allows Fast Bakery to download package from
    your Artifactory private repositories.
    Once you have created this integrations, make sure you add all the pypi and conda channels hosted by this Artifactory
    instance to the Private PyPI Repositories and Private Conda Channels integrations.

    Example usage:
        outerbounds integrations artifactory create --name my-artifactory --domain my-artifactory.com --reachable-from-control-plane --username my-username --password my-password
    """,
)
def artifactory():
    pass


@artifactory.command(help="Create an Artifactory integration")
@click.argument("name")
@click.option("--description", help="Description of the integration", default="")
@click.option("--domain", required=True, help="Artifactory Domain")
@click.option(
    "--reachable-from-control-plane/--not-reachable",
    default=True,
    help="Is reachable from control plane",
)
@click.option("--username", required=True, help="Username")
@click.option("--password", required=True, help="Password")
@common_integration_options
def create(  # type: ignore[no-redef]
    name,
    description,
    domain,
    reachable_from_control_plane,
    username,
    password,
    perimeter,
    config_dir,
    profile,
    output,
):
    spec = {
        "domain": domain,
        "is_reachable_from_control_plane": reachable_from_control_plane,
    }
    secrets = {
        "username": username,
        "password": password,
    }
    create_or_update_integration(
        IntegrationOperation.CREATE,
        name,
        "ARTIFACTORY",
        description,
        spec,
        secrets,
        perimeter,
        config_dir,
        profile,
        output,
    )


@artifactory.command(help="Update an Artifactory integration")
@click.argument("name")
@click.option("--description", help="Description of the integration")
@click.option("--domain", help="Artifactory Domain")
@click.option(
    "--reachable-from-control-plane/--not-reachable",
    default=None,
    help="Is reachable from control plane",
)
@click.option("--username", help="Username")
@click.option("--password", help="Password")
@common_integration_options
def update(  # type: ignore[no-redef]
    name,
    description,
    domain,
    reachable_from_control_plane,
    username,
    password,
    perimeter,
    config_dir,
    profile,
    output,
):
    if not perimeter:
        perimeter = get_current_perimeter(config_dir, profile)

    url = f"{get_integration_api_url(config_dir, profile, perimeter)}/{name}"
    headers = get_auth_headers(config_dir, profile)
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    existing = res.json()

    spec = existing.get("integration_spec", {})
    if domain:
        spec["domain"] = domain
    if reachable_from_control_plane is not None:
        spec["is_reachable_from_control_plane"] = reachable_from_control_plane
    secrets = {}
    if username:
        secrets["username"] = username
    if password:
        secrets["password"] = password
    if description is None:
        description = existing.get("integration_description", "")

    create_or_update_integration(
        IntegrationOperation.UPDATE,
        name,
        "ARTIFACTORY",
        description,
        spec,
        {},
        perimeter,
        config_dir,
        profile,
        output,
    )


# --- Azure Artifacts ---
@integrations.group(
    name="azure-artifacts",
    help="""
    This command is used to create an Azure Artifacts integration, which will allows Fast Bakery to download package from
    your Azure DevOps private repositories.
    Once you have created this integrations, make sure you add all the pypi and conda channels hosted by this Azure Artifacts
    instance to the Private PyPI Repositories integration.

    Example usage:
        outerbounds integrations azure-artifacts create --name my-azure-artifacts --organization my-organization --project-name my-project --username my-username --password my-password
    """,
)
def azure_artifacts():
    pass


@azure_artifacts.command(help="Create an Azure Artifacts integration")
@click.argument("name")
@click.option("--description", help="Description of the integration", default="")
@click.option("--organization", required=True, help="Azure DevOps Organization")
@click.option("--project-name", help="Azure DevOps Project Name (optional)")
@click.option("--username", required=True, help="Username/Email")
@click.option("--password", required=True, help="PAT/Password")
@common_integration_options
def create(  # type: ignore[no-redef]
    name,
    description,
    organization,
    project_name,
    username,
    password,
    perimeter,
    config_dir,
    profile,
    output,
):
    spec = {
        "organization": organization,
    }
    if project_name:
        spec["project_name"] = project_name

    secrets = {
        "username": username,
        "password": password,
    }
    create_or_update_integration(
        IntegrationOperation.CREATE,
        name,
        "AZURE_ARTIFACTS",
        description,
        spec,
        secrets,
        perimeter,
        config_dir,
        profile,
        output,
    )


@azure_artifacts.command(help="Update an Azure Artifacts integration")
@click.argument("name")
@click.option("--description", help="Description of the integration")
@click.option("--organization", help="Azure DevOps Organization")
@click.option("--project-name", help="Azure DevOps Project Name")
@click.option("--username", help="Username/Email")
@click.option("--password", help="PAT/Password")
@common_integration_options
def update(  # type: ignore[no-redef]
    name,
    description,
    organization,
    project_name,
    username,
    password,
    perimeter,
    config_dir,
    profile,
    output,
):
    if not perimeter:
        perimeter = get_current_perimeter(config_dir, profile)

    url = f"{get_integration_api_url(config_dir, profile, perimeter)}/{name}"
    headers = get_auth_headers(config_dir, profile)
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    existing = res.json()

    spec = existing.get("integration_spec", {})
    if organization:
        spec["organization"] = organization
    if project_name is not None:
        spec["project_name"] = project_name

    secrets = {}
    if username:
        secrets["username"] = username
    if password:
        secrets["password"] = password

    if description is None:
        description = existing.get("integration_description", "")

    create_or_update_integration(
        IntegrationOperation.UPDATE,
        name,
        "AZURE_ARTIFACTS",
        description,
        spec,
        secrets,
        perimeter,
        config_dir,
        profile,
        output,
    )


# --- GitLab Artifacts ---
@integrations.group(
    name="gitlab-artifacts",
    help="""
    This command is used to create a GitLab Artifacts integration, which will allows Fast Bakery to download package from
    your GitLab private repositories.
    Once you have created this integrations, make sure you add all the pypi repositories hosted by this GitLab
    instance to the Private PyPI Repositories integration.

    Example usage:
        outerbounds integrations gitlab-artifacts create --name my-gitlab-artifacts --gitlab-url https://gitlab.com --project-id 1234567890 --username my-username --password my-password
    """,
)
def gitlab_artifacts():
    pass


@gitlab_artifacts.command(help="Create a GitLab Artifacts integration")
@click.argument("name")
@click.option("--description", help="Description of the integration", default="")
@click.option("--gitlab-url", default="gitlab.com", help="GitLab Instance URL")
@click.option("--project-id", required=True, help="GitLab Project ID")
@click.option("--username", required=True, help="Username")
@click.option("--password", required=True, help="Access Token/Password")
@common_integration_options
def create(  # type: ignore[no-redef]
    name,
    description,
    gitlab_url,
    project_id,
    username,
    password,
    perimeter,
    config_dir,
    profile,
    output,
):
    spec = {
        "gitlab_url": gitlab_url,
        "project_id": project_id,
    }
    secrets = {
        "username": username,
        "password": password,
    }
    create_or_update_integration(
        IntegrationOperation.CREATE,
        name,
        "GITLAB_ARTIFACTS",
        description,
        spec,
        secrets,
        perimeter,
        config_dir,
        profile,
        output,
    )


@gitlab_artifacts.command(help="Update a GitLab Artifacts integration")
@click.argument("name")
@click.option("--description", help="Description of the integration")
@click.option("--gitlab-url", help="GitLab Instance URL")
@click.option("--project-id", help="GitLab Project ID")
@click.option("--username", help="Username")
@click.option("--password", help="Access Token/Password")
@common_integration_options
def update(  # type: ignore[no-redef]
    name,
    description,
    gitlab_url,
    project_id,
    username,
    password,
    perimeter,
    config_dir,
    profile,
    output,
):
    if not perimeter:
        perimeter = get_current_perimeter(config_dir, profile)

    url = f"{get_integration_api_url(config_dir, profile, perimeter)}/{name}"
    headers = get_auth_headers(config_dir, profile)
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    existing = res.json()

    spec = existing.get("integration_spec", {})
    if gitlab_url:
        spec["gitlab_url"] = gitlab_url
    if project_id:
        spec["project_id"] = project_id

    secrets = {}
    if username:
        secrets["username"] = username
    if password:
        secrets["password"] = password

    if description is None:
        description = existing.get("integration_description", "")

    create_or_update_integration(
        IntegrationOperation.UPDATE,
        name,
        "GITLAB_ARTIFACTS",
        description,
        spec,
        secrets,
        perimeter,
        config_dir,
        profile,
        output,
    )


# --- Container Registry ---
@integrations.group(
    name="container-registry",
    help="""
    This command is used to create a Container Registry integration, which allows Fast Bakery to pull container images from
    your private container registry. This means you can use private container images as the base image for your Fast Bakery images.

    Three authentication methods are supported:
    1. AWS ECR authentication using IAM roles which are assumable by the task role (--target-role-arn)
    2. AWS ECR authentication using the task's IAM role (--use-task-role)
    3. Username/password authentication for other registries (--username and --password)

    Example usage for AWS ECR with IAM role:
        outerbounds integrations container-registry create my-ecr-registry --registry-domain 123456789012.dkr.ecr.us-west-2.amazonaws.com --target-role-arn arn:aws:iam::123456789012:role/my-role

    Example usage for AWS ECR with task role:
        outerbounds integrations container-registry create my-ecr-registry --registry-domain 123456789012.dkr.ecr.us-west-2.amazonaws.com --use-task-role

    Example usage for Artifactory or other registries:
        outerbounds integrations container-registry create my-artifactory --registry-domain my-registry.com --username myuser --password mypass
    """,
)
def container_registry():
    pass


@container_registry.command(help="Create a Container Registry integration")
@click.argument("name")
@click.option("--description", help="Description of the integration", default="")
@click.option("--registry-domain", required=True, help="Registry Domain")
@click.option("--target-role-arn", help="Target Role ARN (for AWS ECR authentication)")
@click.option(
    "--use-task-role",
    is_flag=True,
    help="Use the task's IAM role for authentication (for AWS ECR)",
)
@click.option(
    "--username", help="Username for registry authentication (for non-ECR registries)"
)
@click.option(
    "--password", help="Password for registry authentication (for non-ECR registries)"
)
@common_integration_options
def create(  # type: ignore[no-redef]
    name,
    description,
    registry_domain,
    target_role_arn,
    use_task_role,
    username,
    password,
    perimeter,
    config_dir,
    profile,
    output,
):
    if use_task_role and (target_role_arn or username or password):
        click.secho(
            "Error: --use-task-role cannot be used with --target-role-arn, --username, or --password",
            fg="red",
            err=True,
        )
        sys.exit(1)

    spec = {
        "registry_domain": registry_domain,
    }

    if use_task_role:
        spec["use_task_role"] = True
    else:
        spec["use_task_role"] = False

    if target_role_arn:
        spec["target_role_arn"] = target_role_arn

    secrets = {}
    if username or password:
        if not username or not password:
            click.secho(
                "Error: Both --username and --password must be provided together",
                fg="red",
                err=True,
            )
            sys.exit(1)
        secrets = {
            "username": username,
            "password": password,
        }

    create_or_update_integration(
        IntegrationOperation.CREATE,
        name,
        "CONTAINER_REGISTRY",
        description,
        spec,
        secrets,
        perimeter,
        config_dir,
        profile,
        output,
    )


@container_registry.command(help="Update a Container Registry integration")
@click.argument("name")
@click.option("--description", help="Description of the integration")
@click.option("--registry-domain", help="Registry Domain")
@click.option("--target-role-arn", help="Target Role ARN (for AWS ECR authentication)")
@click.option(
    "--use-task-role",
    is_flag=True,
    help="Use the task's IAM role for authentication (for AWS ECR)",
)
@click.option(
    "--username", help="Username for registry authentication (for non-ECR registries)"
)
@click.option(
    "--password", help="Password for registry authentication (for non-ECR registries)"
)
@common_integration_options
def update(  # type: ignore[no-redef]
    name,
    description,
    registry_domain,
    target_role_arn,
    use_task_role,
    username,
    password,
    perimeter,
    config_dir,
    profile,
    output,
):
    if use_task_role and (target_role_arn or username or password):
        click.secho(
            "Error: --use-task-role cannot be used with --target-role-arn, --username, or --password",
            fg="red",
            err=True,
        )
        sys.exit(1)

    if not perimeter:
        perimeter = get_current_perimeter(config_dir, profile)

    url = f"{get_integration_api_url(config_dir, profile, perimeter)}/{name}"
    headers = get_auth_headers(config_dir, profile)
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    existing = res.json()

    spec = existing.get("integration_spec", {})
    if registry_domain:
        spec["registry_domain"] = registry_domain

    if use_task_role:
        spec["use_task_role"] = True
        spec.pop("target_role_arn", None)
    elif target_role_arn is not None:
        spec["target_role_arn"] = target_role_arn
        spec["use_task_role"] = False

    if description is None:
        description = existing.get("integration_description", "")

    secrets = {}
    if username or password:
        spec["use_task_role"] = False
        if not username or not password:
            click.secho(
                "Error: Both --username and --password must be provided together",
                fg="red",
                err=True,
            )
            sys.exit(1)
        secrets = {
            "username": username,
            "password": password,
        }

    create_or_update_integration(
        IntegrationOperation.UPDATE,
        name,
        "CONTAINER_REGISTRY",
        description,
        spec,
        secrets,
        perimeter,
        config_dir,
        profile,
        output,
    )


# ------------------------------------------------------------------------------
# Private Repositories Integrations
# ------------------------------------------------------------------------------


def find_integrations_by_type(
    config_dir: str, profile: str, perimeter: str, integration_type: str
) -> List[Dict[str, Any]]:
    """Finds integrations of a specific type."""
    url = get_integration_api_url(config_dir, profile, perimeter)
    headers = get_auth_headers(config_dir, profile)
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    data = res.json()
    items = data.get("resource_integrations", [])

    matches = []
    for item in items:
        if item.get("integration_type") == integration_type:
            matches.append(item)
    return matches


def get_integration(
    config_dir: str, profile: str, perimeter: str, name: str
) -> Dict[str, Any]:
    """Fetches full details of a specific integration."""
    url = f"{get_integration_api_url(config_dir, profile, perimeter)}/{name}"
    headers = get_auth_headers(config_dir, profile)
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()


def ensure_integration_exists(config_dir: str, profile: str, perimeter: str, name: str):
    """Ensures a specific integration exists."""
    url = f"{get_integration_api_url(config_dir, profile, perimeter)}/{name}"
    headers = get_auth_headers(config_dir, profile)
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise click.ClickException(
                f"Host integration '{name}' does not exist. Please create it first."
            )
        raise


# --- Private PyPI Repositories ---
@integrations.group(
    name="private-pypi-repositories",
    help="""
    This command is used to add a private pypi repository to the list of private repositories that are always checked when solving
    package dependencies. Each repository must be associated with an existing private service integration like Artifactory, GitLab,
    CodeArtifacts, Azure Artifacts, etc.

    Example usage:
        outerbounds integrations private-pypi add --repository-name my-pypi-repository --repository-host-integration-name my-artifactory --repository-is-default
        outerbounds integrations private-pypi remove --repository-name my-pypi-repository
    """,
)
def private_pypi_repositories():
    pass


@private_pypi_repositories.command(
    help="Add a repository to Private PyPI Repositories integration"
)
@click.option("--repository-name", required=True, help="Name of the repository")
@click.option(
    "--repository-host-integration-name",
    required=True,
    help="Name of the host integration (e.g., artifactory, code-artifacts)",
)
@click.option(
    "--repository-is-default",
    is_flag=True,
    default=False,
    help="Set as default repository",
)
@common_integration_options
def add(  # type: ignore[no-redef]
    repository_name,
    repository_host_integration_name,
    repository_is_default,
    perimeter,
    config_dir,
    profile,
    output,
):
    if not perimeter:
        perimeter = get_current_perimeter(config_dir, profile)

    integrations_found = find_integrations_by_type(
        config_dir, profile, perimeter, "PRIVATE_PYPI_REPOSITORIES"
    )

    if len(integrations_found) > 1:
        raise click.ClickException(
            "More than one private PyPI repositories integration found. Please contact Outerbounds support."
        )

    target_name = "default-private-pypi-repositories"
    current_repos = []
    description = ""
    operation = IntegrationOperation.CREATE

    if len(integrations_found) == 1:
        target_name = integrations_found[0].get("integration_name")
        existing = get_integration(config_dir, profile, perimeter, target_name)
        current_repos = existing.get("integration_spec", {}).get("repositories", [])
        description = existing.get("integration_description", "")
        operation = IntegrationOperation.UPDATE

    # Validate that the host integration exists
    ensure_integration_exists(
        config_dir, profile, perimeter, repository_host_integration_name
    )

    # Create new repository entry
    new_repo = {
        "repository_name": repository_name,
        "host_integration_name": repository_host_integration_name,
        "is_default": repository_is_default,
    }

    # Add or update repository in the list
    repo_map = {r["repository_name"]: r for r in current_repos}

    # If new repo is default, unset other defaults
    if repository_is_default:
        for r in repo_map.values():
            r["is_default"] = False

    repo_map[repository_name] = new_repo

    # Ensure default repo is at the top
    final_repos = []
    default_repo = None
    for r in repo_map.values():
        if r.get("is_default"):
            default_repo = r
        else:
            final_repos.append(r)

    if default_repo:
        final_repos.insert(0, default_repo)

    spec = {"repositories": final_repos}

    create_or_update_integration(
        operation,
        target_name,
        "PRIVATE_PYPI_REPOSITORIES",
        description,
        spec,
        {},
        perimeter,
        config_dir,
        profile,
        output,
    )


@private_pypi_repositories.command(
    help="Remove a repository from Private PyPI Repositories integration"
)
@click.option(
    "--repository-name", required=True, help="Name of the repository to remove"
)
@common_integration_options
def remove(repository_name, perimeter, config_dir, profile, output):  # type: ignore[no-redef]
    if not perimeter:
        perimeter = get_current_perimeter(config_dir, profile)

    integrations_found = find_integrations_by_type(
        config_dir, profile, perimeter, "PRIVATE_PYPI_REPOSITORIES"
    )

    if len(integrations_found) > 1:
        raise click.ClickException(
            "More than one private PyPI repository integration found. Please contact Outerbounds support."
        )

    if not integrations_found:
        raise click.ClickException("No private PyPI repository integration found.")

    target_name = integrations_found[0].get("integration_name")
    existing = get_integration(config_dir, profile, perimeter, target_name)
    current_repos = existing.get("integration_spec", {}).get("repositories", [])
    description = existing.get("integration_description", "")

    final_repos = [r for r in current_repos if r["repository_name"] != repository_name]

    if len(final_repos) == len(current_repos):
        click.secho(f"Repository '{repository_name}' not found.", fg="yellow", err=True)
        return

    spec = {"repositories": final_repos}

    create_or_update_integration(
        IntegrationOperation.UPDATE,
        target_name,
        "PRIVATE_PYPI_REPOSITORIES",
        description,
        spec,
        {},
        perimeter,
        config_dir,
        profile,
        output,
    )


# --- Private Conda Channels ---
@integrations.group(
    name="private-conda-channels",
    help="""
    This command is used to add a private conda channel to the list of private channels that are always checked when solving
    package dependencies. Each channel must be associated with an existing private service integration like Artifactory.

    Example usage:
        outerbounds integrations private-conda add --channel-name my-conda-channel --channel-host-integration-name my-artifactory --channel-is-default
        outerbounds integrations private-conda remove --channel-name my-conda-channel
    """,
)
def private_conda_channels():
    pass


@private_conda_channels.command(
    help="Add a channel to Private Conda Channels integration"
)
@click.option("--channel-name", required=True, help="Name of the channel")
@click.option(
    "--channel-host-integration-name",
    required=True,
    help="Name of the host integration (e.g., artifactory)",
)
@click.option("--channel-is-default", default=False, help="Set as default channel")
@common_integration_options
def add(  # type: ignore[no-redef]
    channel_name,
    channel_host_integration_name,
    channel_is_default,
    perimeter,
    config_dir,
    profile,
    output,
):
    if not perimeter:
        perimeter = get_current_perimeter(config_dir, profile)

    integrations_found = find_integrations_by_type(
        config_dir, profile, perimeter, "PRIVATE_CONDA_CHANNELS"
    )

    if len(integrations_found) > 1:
        raise click.ClickException(
            "More than one private Conda channel integration found. Please contact Outerbounds support."
        )

    target_name = "default-private-conda-channels"
    current_channels = []
    description = ""
    operation = IntegrationOperation.CREATE

    if len(integrations_found) == 1:
        target_name = integrations_found[0].get("integration_name")
        existing = get_integration(config_dir, profile, perimeter, target_name)
        current_channels = existing.get("integration_spec", {}).get("channels", [])
        description = existing.get("integration_description", "")
        operation = IntegrationOperation.UPDATE

    # Validate that the host integration exists
    ensure_integration_exists(
        config_dir, profile, perimeter, channel_host_integration_name
    )

    # Create new channel entry
    new_channel = {
        "repository_name": channel_name,
        "host_integration_name": channel_host_integration_name,
        "is_default": channel_is_default,
    }

    # Add or update channel in the list
    channel_map = {c["repository_name"]: c for c in current_channels}

    # If new channel is default, unset other defaults
    if channel_is_default:
        for c in channel_map.values():
            c["is_default"] = False

    channel_map[channel_name] = new_channel

    # Ensure default channel is at the top
    final_channels = []
    default_channel = None
    for c in channel_map.values():
        if c.get("is_default"):
            default_channel = c
        else:
            final_channels.append(c)

    if default_channel:
        final_channels.insert(0, default_channel)

    spec = {"channels": final_channels}

    create_or_update_integration(
        operation,
        target_name,
        "PRIVATE_CONDA_CHANNELS",
        description,
        spec,
        {},
        perimeter,
        config_dir,
        profile,
        output,
    )


@private_conda_channels.command(
    help="Remove a channel from Private Conda Channels integration"
)
@click.option("--channel-name", required=True, help="Name of the channel to remove")
@common_integration_options
def remove(channel_name, perimeter, config_dir, profile, output):  # type: ignore[no-redef]
    if not perimeter:
        perimeter = get_current_perimeter(config_dir, profile)

    integrations_found = find_integrations_by_type(
        config_dir, profile, perimeter, "PRIVATE_CONDA_CHANNELS"
    )

    if len(integrations_found) > 1:
        raise click.ClickException(
            "More than one private Conda channel integration found. Please contact Outerbounds support."
        )

    if not integrations_found:
        raise click.ClickException("No private Conda channel integration found.")

    target_name = integrations_found[0].get("integration_name")
    existing = get_integration(config_dir, profile, perimeter, target_name)
    current_channels = existing.get("integration_spec", {}).get("channels", [])
    description = existing.get("integration_description", "")

    final_channels = [
        c for c in current_channels if c["repository_name"] != channel_name
    ]

    if len(final_channels) == len(current_channels):
        click.secho(f"Channel '{channel_name}' not found.", fg="yellow", err=True)
        return

    spec = {"channels": final_channels}

    create_or_update_integration(
        IntegrationOperation.UPDATE,
        target_name,
        "PRIVATE_CONDA_CHANNELS",
        description,
        spec,
        {},
        perimeter,
        config_dir,
        profile,
        output,
    )


# --- Git PyPI Repository ---
@integrations.group(
    name="git-pypi-repository",
    help="""
    This command is used to create a Git PyPI Repository integration, which allows Fast Bakery to install Python packages
    directly from private Git repositories using pip's VCS support (e.g., pip install git+https://...).

    You can specify multiple repository URLs, which can be at different levels:
    - Service level: https://gitlab.com
    - Organization level: https://gitlab.com/outerbounds
    - Project level: https://gitlab.com/outerbounds/project1

    The credentials will be used to authenticate to these repositories during package installation.

    Example usage:
        outerbounds integrations git-pypi-repository create my-git-repos --repository-url https://gitlab.com/myorg --username myuser --password mytoken
    """,
)
def git_pypi_repository():
    pass


@git_pypi_repository.command(help="Create a Git PyPI Repository integration")
@click.argument("name")
@click.option("--description", help="Description of the integration", default="")
@click.option(
    "--repository-url",
    "-r",
    multiple=True,
    required=True,
    help="Git repository URL (can be specified multiple times for multiple repositories)",
)
@click.option("--username", required=True, help="Username for Git authentication")
@click.option("--password", required=True, help="Password/Token for Git authentication")
@common_integration_options
def create(  # type: ignore[no-redef]
    name,
    description,
    repository_url,
    username,
    password,
    perimeter,
    config_dir,
    profile,
    output,
):
    if not repository_url:
        raise click.ClickException("At least one repository URL is required")

    if not username or not password:
        raise click.ClickException("Username and password are required")

    spec = {
        "repository_urls": list(repository_url),
    }

    secrets = {
        "username": username,
        "password": password,
    }
    create_or_update_integration(
        IntegrationOperation.CREATE,
        name,
        "GIT_PYPI_REPOSITORY",
        description,
        spec,
        secrets,
        perimeter,
        config_dir,
        profile,
        output,
    )


@git_pypi_repository.command(help="Update a Git PyPI Repository integration")
@click.argument("name")
@click.option("--description", help="Description of the integration")
@click.option(
    "--repository-url",
    "-r",
    multiple=True,
    help="Git repository URL (can be specified multiple times for multiple repositories). Replaces existing URLs if provided.",
)
@click.option("--username", help="Username for Git authentication")
@click.option("--password", help="Password/Token for Git authentication")
@common_integration_options
def update(  # type: ignore[no-redef]
    name,
    description,
    repository_url,
    username,
    password,
    perimeter,
    config_dir,
    profile,
    output,
):
    if not perimeter:
        perimeter = get_current_perimeter(config_dir, profile)

    url = f"{get_integration_api_url(config_dir, profile, perimeter)}/{name}"
    headers = get_auth_headers(config_dir, profile)
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    existing = res.json()

    spec = existing.get("integration_spec", {})
    if repository_url:
        spec["repository_urls"] = list(repository_url)

    if description is None:
        description = existing.get("integration_description", "")

    secrets = {}
    if username:
        secrets["username"] = username
    if password:
        secrets["password"] = password

    create_or_update_integration(
        IntegrationOperation.UPDATE,
        name,
        "GIT_PYPI_REPOSITORY",
        description,
        spec,
        secrets,
        perimeter,
        config_dir,
        profile,
        output,
    )


# --- Custom Secret ---
@integrations.group(
    name="custom-secret",
    help="""
    This command is used to create a Custom Secret integration, which will create a custom secret with the keys and value
    pairs you provide. Once the secret is created, you can use the @secrets(sources=["outerbounds.<integration-name>"]) to
    set the secrets as environment variables within your flow.

    Example usage:
        outerbounds integrations custom-secret create --name my-custom-secret --description "My custom secret" --secret key=value
    """,
)
def custom_secret():
    pass


@custom_secret.command(help="Create a Custom Secret integration")
@click.argument("name")
@click.option("--description", help="Description of the integration", default="")
@click.option(
    "--secret",
    "-s",
    multiple=True,
    required=True,
    help="Secret Key-Value pair: 'key=value'",
)
@common_integration_options
def create(name, description, secret, perimeter, config_dir, profile, output):  # type: ignore[no-redef]
    spec = {}
    secrets = {}
    for s in secret:
        if "=" not in s:
            raise click.BadParameter("Secret must be in format 'key=value'")
        k, v = s.split("=", 1)
        secrets[k] = v

    create_or_update_integration(
        IntegrationOperation.CREATE,
        name,
        "CUSTOM_SECRET",
        description,
        spec,
        secrets,
        perimeter,
        config_dir,
        profile,
        output,
    )


@custom_secret.command(help="Update a Custom Secret integration")
@click.argument("name")
@click.option("--description", help="Description of the integration")
@click.option(
    "--secret",
    "-s",
    multiple=True,
    help="Secret Key-Value pair: 'key=value'. Merges with existing secrets if provided.",
)
@common_integration_options
def update(name, description, secret, perimeter, config_dir, profile, output):  # type: ignore[no-redef]
    if not perimeter:
        perimeter = get_current_perimeter(config_dir, profile)

    url = f"{get_integration_api_url(config_dir, profile, perimeter)}/{name}"
    headers = get_auth_headers(config_dir, profile)
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    existing = res.json()

    spec = existing.get("integration_spec", {})

    secrets = {}
    if secret:
        for s in secret:
            if "=" not in s:
                raise click.BadParameter("Secret must be in format 'key=value'")
            k, v = s.split("=", 1)
            secrets[k] = v

    if description is None:
        description = existing.get("integration_description", "")

    create_or_update_integration(
        IntegrationOperation.UPDATE,
        name,
        "CUSTOM_SECRET",
        description,
        spec,
        secrets,
        perimeter,
        config_dir,
        profile,
        output,
    )


cli.add_command(integrations, name="integrations")
