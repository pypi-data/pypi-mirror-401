"""Azure authentication and credential management."""

import logging
import os
from typing import Any

from azure.core.exceptions import AzureError
from azure.identity import (
    AzureCliCredential,
    ClientSecretCredential,
    ManagedIdentityCredential
)
from dotenv import load_dotenv


def _load_env_file() -> None:
    """Load environment variables from .env file.

    load_dotenv() by default only searches the current working directory.
    We search multiple locations:
    1. Current working directory
    2. Project root (where this file is located, walking up to find .env)
    """

    # Try current working directory first (default behavior)
    result = load_dotenv(override=False)  # override=False: don't override existing env vars
    if result:
        logging.info("Loaded .env file from current working directory")
        return

    # If not found, try searching from the script's location up to project root
    from pathlib import Path

    # Start from the directory containing this file (azure_auth.py)
    current_file = Path(__file__).resolve()
    search_dir = current_file.parent  # src/gettopology/

    # Walk up to project root (look for pyproject.toml or .env)
    for _ in range(3):  # Max 3 levels up (src/gettopology -> src -> project root)
        env_file = search_dir / ".env"
        if env_file.exists():
            load_dotenv(env_file, override=False)
            logging.info(f"Loaded .env file from {env_file}")
            return
        search_dir = search_dir.parent

    logging.debug("No .env file found in current directory or project root")


def _get_service_principal_credentials(
    client_id: str | None = None,
    client_secret: str | None = None,
    tenant_id: str | None = None,
) -> tuple[str | None, str | None, str | None]:
    """Get Service Principal credentials from multiple sources.

    Priority:
    1. CLI arguments (passed as parameters)
    2. Environment variables (AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID)
    3. .env file (if python-dotenv is available)

    Args:
        client_id: Service Principal client ID from CLI (optional)
        client_secret: Service Principal client secret from CLI (optional)
        tenant_id: Azure tenant ID from CLI (optional)

    Returns:
        Tuple of (client_id, client_secret, tenant_id) from highest priority source
    """
    # Load .env file if available (only once)
    _load_env_file()

    # Priority: CLI args > env vars > .env file
    final_client_id = client_id or os.getenv("AZURE_CLIENT_ID")
    final_client_secret = client_secret or os.getenv("AZURE_CLIENT_SECRET")
    final_tenant_id = tenant_id or os.getenv("AZURE_TENANT_ID")

    return final_client_id, final_client_secret, final_tenant_id


def get_azure_credential(
    client_id: str | None = None,
    client_secret: str | None = None,
    tenant_id: str | None = None,
    ) -> Any:
    """Get Azure credentials using various authentication methods.

    Authentication order:
    1. Azure CLI (az login) - tried first
    2. Service Principal:
       a. CLI arguments (if provided)
       b. Environment variables (AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID)
       c. .env file (if python-dotenv is available)
    3. Managed Identity (if running in Azure)

    Args:
        client_id: Service Principal client ID from CLI (optional)
        client_secret: Service Principal client secret from CLI (optional)
        tenant_id: Azure tenant ID from CLI (optional)

    Returns:
        Azure credential object

    Raises:
        ValueError: If SPN credentials are incomplete
        AzureError: If authentication fails
    """
    # Step 1: Try Azure CLI first
    logging.info("Attempting Azure CLI authentication (az login)")
    try:
        credential: Any = AzureCliCredential()
        # Test the credential
        credential.get_token("https://management.azure.com/.default")
        logging.info("Azure CLI authentication successful")
        return credential
    except Exception as e:
        logging.warning(f"Azure CLI authentication failed: {e}")

    # Step 2: Try Service Principal (CLI -> env vars -> .env file)
    logging.info("Checking for Service Principal credentials (CLI args -> env vars -> .env file)")
    spn_client_id, spn_client_secret, spn_tenant_id = _get_service_principal_credentials(
        client_id=client_id,
        client_secret=client_secret,
        tenant_id=tenant_id,
    )

    if spn_client_id and spn_client_secret and spn_tenant_id:
        logging.info("Service Principal credentials found. Attempting Service Principal authentication")
        try:
            credential = ClientSecretCredential(
                tenant_id=spn_tenant_id,
                client_id=spn_client_id,
                client_secret=spn_client_secret,
                additionally_allowed_tenants=["*"],  # Allow access to any tenant the SP can access
            )
            # Test the credential by getting a token
            credential.get_token("https://management.azure.com/.default")
            logging.info("Service Principal authentication successful")
            return credential
        except Exception as e:
            logging.warning(f"Service Principal authentication failed: {e}")
    elif any([spn_client_id, spn_client_secret, spn_tenant_id]):
        # Partial credentials provided - this is an error
        missing = []
        if not spn_client_id:
            missing.append("client_id")
        if not spn_client_secret:
            missing.append("client_secret")
        if not spn_tenant_id:
            missing.append("tenant_id")
        logging.warning(f"Incomplete Service Principal credentials. Missing: {', '.join(missing)}")
        raise ValueError(
            f"Incomplete Service Principal credentials. Missing: {', '.join(missing)}"
        )
    else:
        # No Service Principal credentials found
        logging.info("No Service Principal credentials found (checked CLI args, env vars, and .env file)")

    # Step 3: Try Managed Identity
    logging.info("Attempting Managed Identity authentication")
    try:
        credential = ManagedIdentityCredential()
        # Test the credential
        credential.get_token("https://management.azure.com/.default")
        logging.info("Managed Identity authentication successful")
        return credential
    except Exception as e:
        logging.warning(f"Managed Identity authentication failed: {e}")

    # All methods failed
    logging.error("All authentication methods failed")
    raise AzureError(
        "Failed to authenticate. Please run 'az login', provide Service Principal credentials "
        "(via CLI args, environment variables, or .env file), or ensure Managed Identity is available."
    )

