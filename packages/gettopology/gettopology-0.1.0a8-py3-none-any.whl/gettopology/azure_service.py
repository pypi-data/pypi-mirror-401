"""Azure service operations for querying subscriptions and network resources."""

import json
import logging
import subprocess
import time
from collections.abc import Callable
from datetime import datetime
from functools import wraps
from typing import Any, TypeVar

from azure.core.exceptions import AzureError, ServiceResponseError
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest

from gettopology.models import (
    ConnectionModel,
    LocalNetworkGatewayModel,
    TopologyModel,
    VirtualNetworkModel,
)

T = TypeVar('T')


def retry_with_backoff(
    max_retries: int = 2,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    retryable_exceptions: tuple[type[Exception], ...] = (ServiceResponseError, ConnectionError, TimeoutError),
):
    """Decorator to retry function calls with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts (default: 2, so 3 total attempts)
        initial_delay: Initial delay in seconds before first retry (default: 1.0)
        backoff_factor: Multiplier for delay between retries (default: 2.0)
        retryable_exceptions: Tuple of exception types to retry on

    Returns:
        Decorated function that retries on specified exceptions
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries + 1):  # +1 for initial attempt
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        logging.warning(
                            f"Attempt {attempt + 1}/{max_retries + 1} failed for {func.__name__}: {e}. "
                            f"Retrying in {delay:.1f} seconds..."
                        )
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        logging.error(
                            f"All {max_retries + 1} attempts failed for {func.__name__}: {e}"
                        )
                except Exception:
                    # Don't retry on non-retryable exceptions
                    raise

            # If we get here, all retries failed
            raise last_exception  # type: ignore

        return wrapper
    return decorator


def _get_subscriptions_via_cli() -> list[str]:
    """Get all subscription IDs via Azure CLI (supports multi-tenant).

    This is a fallback method that uses 'az account list --all' to get subscriptions
    across all tenants that the user has authenticated to.

    Returns:
        List of subscription IDs, or empty list if Azure CLI is not available
    """
    try:
        result = subprocess.run(
            ["az", "account", "list", "--all", "--output", "json"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False
        )
        if result.returncode == 0:
            accounts = json.loads(result.stdout)
            subscription_ids = [acc.get("id") for acc in accounts if acc.get("id")]
            if subscription_ids:
                logging.debug(f"Found {len(subscription_ids)} subscription(s) via Azure CLI across all tenants")
            return subscription_ids
        return []
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError, Exception) as e:
        logging.debug(f"Could not get subscriptions via Azure CLI: {e}")
        return []


def get_all_subscription_ids(credential: Any) -> list[str]:
    """Get all subscription IDs accessible to the authenticated user/service principal.

    Tries multiple methods in order:
    1. SubscriptionClient (default tenant)
    2. Azure CLI fallback (if available, for multi-tenant)
    3. Individual subscription queries (if specific subscriptions are known)

    Args:
        credential: Azure credential object from azure_auth.get_azure_credential()

    Returns:
        List of subscription IDs (UUIDs)

    Raises:
        AzureError: If unable to query subscriptions
    """
    try:
        # Use SubscriptionClient to list all accessible subscriptions
        subscription_client = SubscriptionClient(credential=credential)

        @retry_with_backoff(max_retries=2)
        def _list_subscriptions():
            return list(subscription_client.subscriptions.list())

        subscriptions = _list_subscriptions()
        subscription_ids = [sub.subscription_id for sub in subscriptions]

        if not subscription_ids:
            logging.warning("No subscriptions found via SubscriptionClient, trying Azure CLI fallback...")
            # Fallback to Azure CLI for multi-tenant support (if available)
            cli_subscriptions = _get_subscriptions_via_cli()
            if cli_subscriptions:
                subscription_ids = cli_subscriptions
                logging.info(f"Found {len(subscription_ids)}:{subscription_ids} accessible subscription(s) via Azure CLI (multi-tenant)")
                return subscription_ids
            logging.warning("No subscriptions found for the authenticated account")
            return []

        # logging.info(f"Found {len(subscription_ids)}:{subscription_ids} accessible subscription(s) in the Tenant")
        return subscription_ids

    except AzureError as e:
        logging.warning(f"SubscriptionClient failed: {e}, trying Azure CLI fallback...")
        # Fallback to Azure CLI for multi-tenant support (if available)
        cli_subscriptions = _get_subscriptions_via_cli()
        if cli_subscriptions:
            logging.info(f"Found {len(cli_subscriptions)} subscription(s) via Azure CLI (multi-tenant)")
            return cli_subscriptions
        logging.error(f"Failed to retrieve subscriptions: {e}")
        raise
    except Exception as e:
        logging.warning(f"Unexpected error with SubscriptionClient: {e}, trying Azure CLI fallback...")
        # Fallback to Azure CLI for multi-tenant support (if available)
        cli_subscriptions = _get_subscriptions_via_cli()
        if cli_subscriptions:
            logging.info(f"Found {len(cli_subscriptions)} subscription(s) via Azure CLI (multi-tenant)")
            return cli_subscriptions
        logging.error(f"Unexpected error retrieving subscriptions: {e}")
        raise AzureError(f"Failed to retrieve subscriptions: {e}") from e


def get_subscription_name(subscription_id: str, credential: Any) -> str | None:
    """Get subscription name from subscription ID.

    Args:
        subscription_id: Subscription ID (UUID)
        credential: Azure credential object

    Returns:
        Subscription name if found, None otherwise

    Raises:
        AzureError: If unable to query subscription
    """
    try:
        subscription_client = SubscriptionClient(credential=credential)

        @retry_with_backoff(max_retries=2)
        def _get_subscription():
            return subscription_client.subscriptions.get(subscription_id)

        subscription = _get_subscription()
        return subscription.display_name if subscription else None
    except AzureError as e:
        logging.warning(f"Failed to get subscription name for {subscription_id}: {e}")
        return None
    except Exception as e:
        logging.warning(f"Unexpected error getting subscription name for {subscription_id}: {e}")
        return None


def get_subscription_names(subscription_ids: list[str], credential: Any) -> dict[str, str]:
    """Get subscription names for multiple subscription IDs.

    Args:
        subscription_ids: List of subscription IDs
        credential: Azure credential object

    Returns:
        Dictionary mapping subscription_id -> subscription_name
    """
    subscription_names: dict[str, str] = {}

    # Get all subscriptions at once for efficiency
    try:
        subscription_client = SubscriptionClient(credential=credential)

        @retry_with_backoff(max_retries=2)
        def _list_subscriptions():
            return list(subscription_client.subscriptions.list())

        subscriptions = _list_subscriptions()

        # Build a map of subscription_id -> display_name
        for sub in subscriptions:
            if sub.subscription_id in subscription_ids:
                subscription_names[sub.subscription_id] = sub.display_name

        # Fill in None for any subscriptions not found
        for sub_id in subscription_ids:
            if sub_id not in subscription_names:
                subscription_names[sub_id] = None  # type: ignore

        return subscription_names

    except AzureError as e:
        logging.warning(f"Failed to get subscription names: {e}")
        # Return empty dict, subscription_name will be None
        return {}
    except Exception as e:
        logging.warning(f"Unexpected error getting subscription names: {e}")
        return {}


def validate_subscription_access(
    subscription_ids: list[str],
    credential: Any,
    ) -> tuple[list[str], list[str]]:
    """Validate that subscription IDs exist and are accessible to the authenticated user/service principal.

    This function validates subscriptions directly by attempting to access each one,
    rather than fetching all subscriptions first. This is more efficient when
    explicit subscriptions are provided via -s or -f flags.

    Args:
        subscription_ids: List of subscription IDs to validate
        credential: Azure credential object from azure_auth.get_azure_credential()

    Returns:
        tuple: (accessible_subscription_ids, inaccessible_subscription_ids)

    Raises:
        AzureError: If unable to query subscriptions
    """
    try:
        accessible = []
        inaccessible = []

        subscription_client = SubscriptionClient(credential=credential)

        # Validate each subscription directly by attempting to access it
        # This avoids fetching all subscriptions when explicit ones are provided
        for sub_id in subscription_ids:
            try:
                @retry_with_backoff(max_retries=2)
                def _get_subscription():
                    return subscription_client.subscriptions.get(sub_id)

                # Try to get subscription details - this validates access
                _get_subscription()
                accessible.append(sub_id)
            except AzureError as e:
                # Subscription not accessible or doesn't exist
                error_msg = str(e).lower()
                error_code = getattr(e, 'status_code', None) or getattr(e, 'error_code', None)

                # Log detailed error for debugging
                logging.debug(f"Error accessing subscription {sub_id}: {e} (code: {error_code})")

                # Check if it's a tenant-related error (subscription in different tenant)
                if any(keyword in error_msg for keyword in ["tenant", "invalidauthenticationtokentenant"]):
                    # Try Azure CLI as last resort (if available) - might show subscription exists but in different tenant
                    cli_subscriptions = _get_subscriptions_via_cli()
                    if sub_id in cli_subscriptions:
                        # Subscription exists but is in a different tenant
                        logging.warning(
                            f"Subscription {sub_id} exists but is in a different tenant. "
                            f"Azure CLI and Service Principal authentication can only access one tenant at a time."
                        )
                    else:
                        logging.warning(
                            f"Subscription {sub_id} may be in a different tenant or does not exist. "
                            f"Error: {str(e)[:200]}..."
                        )
                        logging.debug(f"Full error details: {e}")
                else:
                    # Other error (permissions, not found, etc.)
                    logging.debug(f"Subscription {sub_id} not accessible: {e}")

                inaccessible.append(sub_id)
            except Exception as e:
                # Unexpected error - treat as inaccessible
                logging.warning(f"Error checking subscription {sub_id}: {e}")
                inaccessible.append(sub_id)

        # Don't log here - let the caller handle logging based on context
        # This avoids duplicate log messages

        return accessible, inaccessible

    except AzureError as e:
        logging.error(f"Failed to validate subscription access: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error validating subscription access: {e}")
        raise AzureError(f"Failed to validate subscription access: {e}") from e


def check_subscription_roles(
    subscription_ids: list[str],
    credential: Any,
    ) -> tuple[list[str], list[str]]:
    """Check if the authenticated user/service principal has at least Reader role on subscriptions.

    This function verifies permissions by attempting to read subscription details.
    If successful, the principal has at least Reader role (or Contributor/Owner).

    Args:
        subscription_ids: List of subscription IDs to check
        credential: Azure credential object from azure_auth.get_azure_credential()

    Returns:
        tuple: (subscriptions_with_reader_role: list[str], subscriptions_without_reader_role: list[str])

    Raises:
        AzureError: If unable to check roles
    """
    subscriptions_with_role: list[str] = []
    subscriptions_without_role: list[str] = []

    try:
        # Use SubscriptionClient to check if we can read subscription details
        # This requires Reader role or above
        subscription_client = SubscriptionClient(credential=credential)

        for subscription_id in subscription_ids:
            try:
                @retry_with_backoff(max_retries=2)
                def _get_subscription():
                    return subscription_client.subscriptions.get(subscription_id)

                # Try to get subscription details - this requires Reader role or above
                # If this succeeds, we have at least Reader role
                _get_subscription()

                # Success - we have at least Reader role
                subscriptions_with_role.append(subscription_id)
                # logging.info(f"Subscription {subscription_id}: Has at least Reader role")

            except AzureError as e:
                # If we can't read subscription, we likely don't have Reader role
                # or the subscription doesn't exist
                subscriptions_without_role.append(subscription_id)
                logging.warning(
                    f"Subscription {subscription_id}: Does not have Reader role or above. Error: {e}"
                )
            except Exception as e:
                logging.warning(f"Unexpected error checking roles for subscription {subscription_id}: {e}")
                subscriptions_without_role.append(subscription_id)

        return subscriptions_with_role, subscriptions_without_role

    except Exception as e:
        logging.error(f"Failed to check subscription roles: {e}")
        raise AzureError(f"Failed to check subscription roles: {e}") from e


def get_vnets(
    vnet_names: list[str] | None = None,
    subscription_ids: list[str] | None = None,
    credential: Any = None,
    ) -> list[str]:
    """Get virtual network names from Azure.

    Optimization strategy:
    - Always uses Azure Resource Graph (ARG) for VNet discovery/validation
      (single query across all subscriptions is much faster than iterating with NetworkManagementClient)
    - If vnet_names provided: ARG query filters by names, validates they exist
    - If vnet_names not provided: ARG query returns all VNets

    Args:
        vnet_names: List of VNet names to validate (optional). If provided, validates they exist.
        subscription_ids: List of subscription IDs to search in
        credential: Azure credential object (required)

    Returns:
        List of VNet names:
        - If vnet_names provided: Returns only the VNets that exist (drops non-existent ones)
        - If vnet_names is None: Returns all VNets found in the specified subscriptions

    Raises:
        ValueError: If credential is required but not provided
        AzureError: If Azure API calls fail
    """
    if credential is None:
        raise ValueError("credential is required")

    # If no subscription_ids provided, get all subscriptions
    if not subscription_ids:
        if vnet_names is not None:
            logging.info("No subscriptions provided, getting all accessible subscriptions for VNet validation")
        else:
            logging.info("No subscriptions provided, getting all accessible subscriptions to list all VNets")
        subscription_ids = get_all_subscription_ids(credential)
        if not subscription_ids:
            logging.warning("No subscriptions found")
            return []

    # Optimization: Always use ARG for VNet discovery/validation
    # ARG is faster than NetworkManagementClient because it's a single query across all subscriptions
    # vs iterating each subscription with NetworkManagementClient
    if vnet_names is not None:
        # VNet names provided: Use ARG to validate (single query, filter by names)
        return _get_vnets_via_arg(vnet_names, subscription_ids, credential)
    else:
        # No VNet names provided: Use ARG to get all VNets (single query)
        return _get_all_vnets_via_arg(subscription_ids, credential)


def _get_vnets_via_arg(
    vnet_names: list[str],
    subscription_ids: list[str],
    credential: Any,
    ) -> list[str]:
    """Validate specific VNet names using Azure Resource Graph.

    This is optimized for when VNet names are provided. ARG allows a single
    query across all subscriptions to validate VNets, which is much faster
    than iterating with NetworkManagementClient (which requires subscription ID per call).

    Args:
        vnet_names: List of VNet names to validate
        subscription_ids: List of subscription IDs to search in
        credential: Azure credential object

    Returns:
        List of validated VNet names that exist in the subscriptions
    """
    vnet_names_set = set(vnet_names)
    found_vnets: list[str] = []

    try:
        resource_graph_client = ResourceGraphClient(credential)

        # Build ARG query to find VNets by name across all subscriptions
        # Query returns: name, subscriptionId, resourceGroup, id
        # Use 'or' conditions for name matching (KQL syntax for ARG)
        name_conditions = " or ".join([f"name == '{name}'" for name in vnet_names])
        query = f"""
        Resources
        | where type == 'microsoft.network/virtualnetworks'
        | where {name_conditions}
        | project name, subscriptionId, resourceGroup, id
        """

        query_request = QueryRequest(
            subscriptions=subscription_ids,
            query=query
        )

        @retry_with_backoff(max_retries=2)
        def _query_resources():
            return resource_graph_client.resources(query_request)

        response = _query_resources()

        if response.data:
            for vnet_data in response.data:
                vnet_name = vnet_data.get('name')
                if vnet_name and vnet_name in vnet_names_set and vnet_name not in found_vnets:
                    found_vnets.append(vnet_name)

        # Log missing VNets at INFO level
        missing_vnets = [vnet for vnet in vnet_names if vnet not in found_vnets]
        if missing_vnets:
            logging.info(
                f"VNet name(s) not found in specified subscriptions: {', '.join(missing_vnets)}"
            )

        if found_vnets:
            logging.info(
                f"Found {len(found_vnets)} VNet(s) in specified subscriptions (via ARG): {', '.join(found_vnets)}"
            )
        else:
            logging.warning(
                f"None of the provided VNet names found in subscriptions: {', '.join(vnet_names)}"
            )

        return found_vnets

    except AzureError as e:
        logging.error(f"Failed to query virtual networks via ARG: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error querying virtual networks via ARG: {e}")
        raise AzureError(f"Failed to query virtual networks via ARG: {e}") from e


def _get_all_vnets_via_arg(
    subscription_ids: list[str],
    credential: Any,
    ) -> list[str]:
    """Get all VNet names using Azure Resource Graph.

    This is optimized for when no VNet names are provided. ARG allows a single
    query across all subscriptions, which is much faster than iterating with
    NetworkManagementClient (which requires subscription ID per call).

    Args:
        subscription_ids: List of subscription IDs to search in
        credential: Azure credential object

    Returns:
        List of all VNet names found in the subscriptions
    """
    all_vnets: list[str] = []

    try:
        resource_graph_client = ResourceGraphClient(credential)

        # Build ARG query to get all VNets across all subscriptions in a single query
        query = """
        Resources
        | where type == 'microsoft.network/virtualnetworks'
        | project name, subscriptionId, resourceGroup, id
        """

        query_request = QueryRequest(
            subscriptions=subscription_ids,
            query=query
        )

        @retry_with_backoff(max_retries=2)
        def _query_all_vnets():
            return resource_graph_client.resources(query_request)

        response = _query_all_vnets()

        if response.data:
            for vnet_data in response.data:
                vnet_name = vnet_data.get('name')
                if vnet_name and vnet_name not in all_vnets:
                    all_vnets.append(vnet_name)

        if all_vnets:
            logging.info(
                f"Found {len(all_vnets)} VNet(s) across {len(subscription_ids)} subscription(s) (via ARG)"
            )
        else:
            logging.warning("No virtual networks found in specified subscriptions")

        return all_vnets

    except AzureError as e:
        logging.error(f"Failed to query virtual networks via ARG: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error querying virtual networks via ARG: {e}")
        raise AzureError(f"Failed to query virtual networks via ARG: {e}") from e


def collect_gateway_and_firewall_resources(
    vnet_resource_ids: list[str],
    subscription_ids: list[str],
    credential: Any,
    vnet_name_to_resource_id: dict[str, str] | None = None,
    vnet_metadata: dict[str, dict] | None = None,
    ) -> dict[str, dict]:
    """Collect Virtual Network Gateways and Azure Firewalls for given VNets.

    Queries Azure Resource Graph for gateways and firewalls, then matches them
    to VNets by extracting VNet ID from their subnet configurations.

    Note on ExpressRoute:
    - virtualNetworkGateways with gatewayType="ExpressRoute" are ExpressRoute gateways
    - Additional ExpressRoute resources: Microsoft.Network/expressRouteCircuits
      and Microsoft.Network/expressRouteGateways may also exist
    - Currently only querying virtualNetworkGateways (covers both ExpressRoute and VPN)
    - TODO: Consider adding expressRouteCircuits/expressRouteGateways if needed

    Args:
        vnet_resource_ids: List of VNet resource IDs to collect gateways/firewalls for
        subscription_ids: List of subscription IDs to search in
        credential: Azure credential object

    Returns:
        Dictionary mapping VNet resource ID -> {
            'gateways': [
                {
                    'name': 'gw-name',
                    'gateway_type': 'ExpressRoute' | 'Vpn',
                    'subnet_id': '/subscriptions/.../subnets/GatewaySubnet',
                    'sku': {...},
                    'resource_id': '/subscriptions/.../virtualNetworkGateways/gw-name'
                }
            ],
            'firewalls': [
                {
                    'name': 'fw-name',
                    'subnet_id': '/subscriptions/.../subnets/AzureFirewallSubnet',
                    'resource_id': '/subscriptions/.../azureFirewalls/fw-name'
                }
            ]
        }
    """
    result: dict[str, dict] = {}

    # Initialize result dict for all VNets
    for vnet_id in vnet_resource_ids:
        result[vnet_id] = {'gateways': [], 'firewalls': []}

    logging.debug(f"Initialized gateway/firewall collection for {len(vnet_resource_ids)} VNet(s)")
    logging.debug(f"VNet resource IDs: {vnet_resource_ids[:3]}...")

    if not vnet_resource_ids:
        return result

    try:
        resource_graph_client = ResourceGraphClient(credential)

        # Query for Virtual Network Gateways
        # Note: virtualNetworkGateways can be ExpressRoute or VPN (check gatewayType property)
        gateway_query = """
        Resources
        | where type  =~ 'microsoft.network/virtualnetworkgateways'
        | project
            name,
            subscriptionId,
            resourceGroup,
            id,
            properties.gatewayType,
            properties.ipConfigurations,
            properties.sku
        """

        gateway_query_request = QueryRequest(
            subscriptions=subscription_ids,
            query=gateway_query
        )

        @retry_with_backoff(max_retries=2)
        def _query_gateways():
            return resource_graph_client.resources(gateway_query_request)

        gateway_response = _query_gateways()

        # Log gateway query results
        if gateway_response.data:
            logging.info(f"Found {len(gateway_response.data)} virtual network gateway(s) via ARG query")
        else:
            logging.info("No virtual network gateways found via ARG query")

        # Process gateway results
        if gateway_response.data:
            for gw_data in gateway_response.data:
                try:
                    gw_id = gw_data.get('id', '')
                    gw_name = gw_data.get('name', '')

                    # Extract gatewayType from ARG response
                    # When ARG projects properties.gatewayType, it returns it as "properties_gatewayType" (with underscore)
                    # Azure returns "Vpn" or "ExpressRoute" with exact casing
                    gw_type = gw_data.get('properties_gatewayType', '')
                    if gw_type:
                        gw_type = gw_type.strip()
                    else:
                        # Log warning if gatewayType is missing - this shouldn't happen if ARG query is correct
                        logging.warning(f"Gateway {gw_name}: gatewayType not found in ARG response. Available keys: {list(gw_data.keys())}")

                    properties = gw_data.get('properties', {})

                    # ARG projects properties.ipConfigurations as "properties_ipConfigurations"
                    ip_configs = gw_data.get('properties_ipConfigurations', [])
                    if not ip_configs:
                        # Fallback to nested structure if not flattened
                        ip_configs = properties.get('ipConfigurations', [])

                    # ARG projects properties.sku as "properties_sku"
                    sku = gw_data.get('properties_sku', {})
                    if not sku:
                        # Fallback to nested structure if not flattened
                        sku = properties.get('sku', {})

                    logging.debug(f"Processing gateway: {gw_name} (type: {gw_type or 'MISSING'}, id: {gw_id})")
                    logging.debug(f"  IP configurations: {len(ip_configs) if isinstance(ip_configs, list) else 'not a list'}")

                    # Extract subnet ID from first IP configuration
                    # Structure: ipConfigurations[0].properties.subnet.id
                    # Example: /subscriptions/.../virtualNetworks/{vnet}/subnets/GatewaySubnet
                    subnet_id = None
                    if ip_configs and isinstance(ip_configs, list) and len(ip_configs) > 0:
                        first_ip_config = ip_configs[0]
                        if isinstance(first_ip_config, dict):
                            # Try nested structure first: properties.subnet.id
                            subnet_id = first_ip_config.get('properties', {}).get('subnet', {}).get('id')
                            if not subnet_id:
                                # Fallback: Try direct access if not nested
                                subnet_id = first_ip_config.get('subnet', {}).get('id')
                            # Additional fallback: Check if subnet is a direct string ID
                            if not subnet_id and 'subnet' in first_ip_config:
                                subnet_obj = first_ip_config.get('subnet')
                                if isinstance(subnet_obj, str):
                                    subnet_id = subnet_obj
                                elif isinstance(subnet_obj, dict):
                                    subnet_id = subnet_obj.get('id')

                    if subnet_id:
                        logging.debug(f"  Extracted subnet ID: {subnet_id}")
                        # Extract VNet ID from subnet ID using string split
                        # Format: /subscriptions/.../virtualNetworks/{vnet}/subnets/{subnet}
                        # Remove /subnets/{subnet} to get VNet ID
                        if '/subnets/' in subnet_id:
                            extracted_vnet_id: str | None = subnet_id.rsplit('/subnets/', 1)[0]
                        else:
                            logging.debug(f"Gateway {gw_name}: Subnet ID format unexpected: {subnet_id}")
                            extracted_vnet_id = None

                        if extracted_vnet_id:
                            logging.info(f"Gateway {gw_name}: Extracted VNet ID from subnet: {extracted_vnet_id}")
                            # Extract VNet name from subnet ID for name-based matching
                            from gettopology.models import extract_vnet_name_from_id
                            vnet_name_from_subnet = extract_vnet_name_from_id(subnet_id)

                            # Normalize VNet ID (remove trailing slash if present, lowercase for comparison)
                            vnet_id_normalized = extracted_vnet_id.rstrip('/').lower()

                            # Try exact match first (by resource ID)
                            matched = False
                            for vnet_id_key in result.keys():
                                vnet_id_key_normalized = vnet_id_key.rstrip('/').lower()
                                if vnet_id_key_normalized == vnet_id_normalized:
                                    result[vnet_id_key]['gateways'].append({
                                        'name': gw_name,
                                        'gateway_type': gw_type,
                                        'subnet_id': subnet_id,
                                        'sku': sku,
                                        'resource_id': gw_id
                                    })
                                    logging.info(f"✓ Matched gateway {gw_name} ({gw_type}) to VNet {vnet_id_key} by resource ID (normalized from {extracted_vnet_id})")
                                    matched = True
                                    break

                            # Fallback: Try matching by VNet name
                            if not matched and vnet_name_from_subnet and vnet_name_to_resource_id:
                                if vnet_name_from_subnet in vnet_name_to_resource_id:
                                    matched_resource_id = vnet_name_to_resource_id[vnet_name_from_subnet]
                                    if matched_resource_id in result:
                                        result[matched_resource_id]['gateways'].append({
                                            'name': gw_name,
                                            'gateway_type': gw_type,
                                            'subnet_id': subnet_id,
                                            'sku': sku,
                                            'resource_id': gw_id
                                        })
                                        logging.info(f"✓ Matched gateway {gw_name} ({gw_type}) to VNet {matched_resource_id} by name '{vnet_name_from_subnet}' (extracted from subnet {subnet_id})")
                                        matched = True

                            if not matched:
                                logging.warning(f"✗ Gateway {gw_name}: VNet {extracted_vnet_id} (name: {vnet_name_from_subnet}) not found in collected VNets")
                                logging.warning(f"  Looking for: {extracted_vnet_id} (normalized: {vnet_id_normalized})")
                                logging.warning(f"  Available VNet IDs ({len(result.keys())} total):")
                                for key in list(result.keys())[:10]:
                                    logging.warning(f"    - {key} (normalized: {key.rstrip('/').lower()})")
                        else:
                            logging.debug(f"Gateway {gw_name}: Could not extract VNet ID from subnet {subnet_id}")
                    else:
                        logging.debug(f"Gateway {gw_name}: No subnet ID found in IP configurations, using fallback matching")
                        logging.debug(f"  IP config structure: {ip_configs}")
                        if ip_configs and isinstance(ip_configs, list) and len(ip_configs) > 0:
                            logging.debug(f"  First IP config keys: {list(ip_configs[0].keys()) if isinstance(ip_configs[0], dict) else 'not a dict'}")

                        # Fallback: Try to match by resource group and subscription
                        # Extract resource group and subscription from gateway ID
                        # Format: /subscriptions/{sub}/resourceGroups/{rg}/providers/.../gateways/{name}
                        if gw_id and vnet_metadata:
                            try:
                                import re
                                # Extract subscription and resource group from gateway ID
                                sub_match = re.search(r'/subscriptions/([^/]+)', gw_id)
                                rg_match = re.search(r'/resourceGroups/([^/]+)', gw_id)
                                if sub_match and rg_match:
                                    gw_subscription = sub_match.group(1)
                                    gw_resource_group = rg_match.group(1)
                                    logging.debug(f"  Gateway resource group: {gw_resource_group}, subscription: {gw_subscription}")

                                    # Try to match to VNets in the same resource group and subscription
                                    for vnet_id_key, vnet_info in vnet_metadata.items():
                                        if (vnet_info.get('resource_group') == gw_resource_group and
                                            vnet_info.get('subscription_id') == gw_subscription):
                                            # Found a VNet in the same resource group and subscription
                                            # This is a reasonable match (gateways are typically in same RG as VNet)
                                            result[vnet_id_key]['gateways'].append({
                                                'name': gw_name,
                                                'gateway_type': gw_type,
                                                'subnet_id': None,  # Couldn't extract from IP configs
                                                'sku': sku,
                                                'resource_id': gw_id
                                            })
                                            logging.info(f"✓ Matched gateway {gw_name} ({gw_type}) to VNet {vnet_id_key} by resource group '{gw_resource_group}' and subscription (fallback match)")
                                            break
                            except Exception as e:
                                logging.debug(f"  Failed to match gateway by resource group: {e}")
                except Exception as e:
                    logging.debug(f"Failed to process gateway {gw_data.get('name', 'unknown')}: {e}")
                    continue

        # Query for Azure Firewalls
        firewall_query = """
        Resources
        | where type =~ 'microsoft.network/azurefirewalls'
        | project
            name,
            subscriptionId,
            resourceGroup,
            id,
            properties.ipConfigurations[0].properties.subnet.id,
            properties.sku
        """

        firewall_query_request = QueryRequest(
            subscriptions=subscription_ids,
            query=firewall_query
        )

        @retry_with_backoff(max_retries=2)
        def _query_firewalls():
            return resource_graph_client.resources(firewall_query_request)

        firewall_response = _query_firewalls()

        # Process firewall results
        if firewall_response.data:
            for fw_data in firewall_response.data:
                try:
                    fw_id = fw_data.get('id', '')
                    fw_name = fw_data.get('name', '')
                    # Try to get subnet ID directly from projected field (ARG may flatten nested paths)
                    subnet_id = fw_data.get('properties.ipConfigurations[0].properties.subnet.id') or fw_data.get('properties_ipConfigurations_0_properties_subnet_id')
                    sku = fw_data.get('properties', {}).get('sku', {}) if isinstance(fw_data.get('properties'), dict) else {}

                    # Fallback: Extract from nested properties structure if direct access didn't work
                    if not subnet_id:
                        fw_properties = fw_data.get('properties', {})
                        if isinstance(fw_properties, dict):
                            ip_configs = fw_properties.get('ipConfigurations', [])
                            if ip_configs and isinstance(ip_configs, list) and len(ip_configs) > 0:
                                first_ip_config = ip_configs[0]
                                if isinstance(first_ip_config, dict):
                                    ip_config_props = first_ip_config.get('properties', {})
                                    if ip_config_props:
                                        subnet_obj = ip_config_props.get('subnet')
                                        if isinstance(subnet_obj, dict):
                                            subnet_id = subnet_obj.get('id')
                                        elif isinstance(subnet_obj, str):
                                            subnet_id = subnet_obj

                    if not subnet_id:
                        logging.warning(f"Firewall {fw_name}: No subnet ID found")
                        continue

                    # Extract VNet ID from subnet ID
                    if '/subnets/' in subnet_id:
                        vnet_id = subnet_id.rsplit('/subnets/', 1)[0]
                    else:
                        logging.warning(f"Firewall {fw_name}: Subnet ID format unexpected: {subnet_id}")
                        continue

                    # Extract VNet name from subnet ID for name-based matching
                    from gettopology.models import extract_vnet_name_from_id
                    vnet_name_from_subnet = extract_vnet_name_from_id(subnet_id)

                    # Normalize VNet ID (remove trailing slash if present, lowercase for comparison)
                    vnet_id_normalized = vnet_id.rstrip('/').lower()

                    # Try exact match first (by resource ID)
                    matched = False
                    for vnet_id_key in result.keys():
                        vnet_id_key_normalized = vnet_id_key.rstrip('/').lower()
                        if vnet_id_key_normalized == vnet_id_normalized:
                            result[vnet_id_key]['firewalls'].append({
                                'name': fw_name,
                                'subnet_id': subnet_id,
                                'sku': sku,
                                'resource_id': fw_id
                            })
                            matched = True
                            break

                    # Fallback: Try matching by VNet name
                    if not matched and vnet_name_from_subnet and vnet_name_to_resource_id:
                        if vnet_name_from_subnet in vnet_name_to_resource_id:
                            matched_resource_id = vnet_name_to_resource_id[vnet_name_from_subnet]
                            if matched_resource_id in result:
                                result[matched_resource_id]['firewalls'].append({
                                    'name': fw_name,
                                    'subnet_id': subnet_id,
                                    'sku': sku,
                                    'resource_id': fw_id
                                })
                                matched = True

                    if not matched:
                        logging.warning(f"Firewall {fw_name}: VNet {vnet_id} (name: {vnet_name_from_subnet}) not found in collected VNets")
                except Exception as e:
                    logging.error(f"Failed to process firewall {fw_data.get('name', 'unknown')}: {e}", exc_info=True)
                    continue

        return result

    except AzureError as e:
        logging.warning(f"Failed to collect gateway/firewall resources via ARG: {e}")
        # Return empty result dict (backward compatibility)
        return result
    except Exception as e:
        logging.warning(f"Unexpected error collecting gateway/firewall resources: {e}")
        # Return empty result dict (backward compatibility)
        return result


def query_route_table_routes(
    route_table_ids: list[str],
    subscription_ids: list[str],
    credential: Any,
    ) -> dict[str, list[dict]]:
    """Query route table routes from Azure Resource Graph.

    Args:
        route_table_ids: List of route table resource IDs
        subscription_ids: List of subscription IDs
        credential: Azure credential object

    Returns:
        Dictionary mapping route table ID -> list of route dicts
        Each route dict contains: name, addressPrefix, nextHopType, nextHopIpAddress
    """
    result: dict[str, list[dict]] = {}

    for rt_id in route_table_ids:
        result[rt_id] = []

    if not route_table_ids:
        return result

    try:
        resource_graph_client = ResourceGraphClient(credential)

        # Extract route table names from IDs
        rt_names = []
        for rt_id in route_table_ids:
            parts = rt_id.split('/routeTables/')
            if len(parts) == 2:
                rt_names.append(parts[1])

        if not rt_names:
            return result

        name_conditions = " or ".join([f"name == '{name}'" for name in rt_names])
        query = f"""
        Resources
        | where type == "microsoft.network/routetables"
        | where {name_conditions}
        | project name, id, properties.routes
        """

        query_request = QueryRequest(
            subscriptions=subscription_ids,
            query=query
        )

        @retry_with_backoff(max_retries=2)
        def _query_route_tables():
            return resource_graph_client.resources(query_request)

        response = _query_route_tables()

        if response.data:
            for rt_data in response.data:
                rt_id = rt_data.get('id', '')
                if rt_id not in route_table_ids:
                    continue

                routes = rt_data.get('properties_routes', [])
                if not routes:
                    props = rt_data.get('properties', {})
                    routes = props.get('routes', [])

                route_list = []
                if isinstance(routes, list):
                    for route in routes:
                        if isinstance(route, dict):
                            route_props = route.get('properties', {})
                            if not route_props:
                                route_props = route

                            route_dict = {
                                'name': route.get('name', ''),
                                'addressPrefix': route_props.get('addressPrefix', ''),
                                'nextHopType': route_props.get('nextHopType', ''),
                                'nextHopIpAddress': route_props.get('nextHopIpAddress', '') or '—',
                            }
                            route_list.append(route_dict)

                result[rt_id] = route_list

        return result
    except Exception as e:
        logging.warning(f"Failed to query route table routes: {e}")
        return result


def collect_topology(
    vnet_names: list[str],
    subscription_ids: list[str],
    credential: Any,
    ) -> TopologyModel:
    """Collect complete topology data for virtual networks.

    Queries Azure Resource Graph to get full VNet details including subnets,
    peerings, and all properties, then parses them into TopologyModel.

    Args:
        vnet_names: List of VNet names to collect topology for
        subscription_ids: List of subscription IDs to search in
        credential: Azure credential object

    Returns:
        TopologyModel containing all virtual networks with their complete topology

    Raises:
        ValueError: If credential is required but not provided
        AzureError: If Azure API calls fail
    """
    if credential is None:
        raise ValueError("credential is required")

    if not subscription_ids:
        raise ValueError("subscription_ids cannot be empty")

    if not vnet_names:
        logging.warning("No VNet names provided, returning empty topology")
        return TopologyModel(
            virtual_networks=[],
            collected_at=datetime.utcnow().isoformat()
        )

    try:
        resource_graph_client = ResourceGraphClient(credential)

        # Build ARG query to get full VNet details
        # Query all properties without filtering to get complete nested structure
        name_conditions = " or ".join([f"name == '{name}'" for name in vnet_names])
        query = f"""
        Resources
        | where type == 'microsoft.network/virtualnetworks'
        | where {name_conditions}
        """

        query_request = QueryRequest(
            subscriptions=subscription_ids,
            query=query
        )

        logging.info(f"Collecting topology data for {len(vnet_names)} VNet(s) via ARG...")

        @retry_with_backoff(max_retries=2)
        def _query_topology():
            return resource_graph_client.resources(query_request)

        response = _query_topology()

        # Get subscription names for all unique subscription IDs
        unique_subscription_ids = list(set(subscription_ids))
        subscription_names_map = get_subscription_names(unique_subscription_ids, credential)

        virtual_networks: list[VirtualNetworkModel] = []

        if response.data:
            for vnet_data in response.data:
                try:
                    # Add subscription_name to vnet_data before parsing
                    vnet_subscription_id = vnet_data.get('subscriptionId', '')
                    if vnet_subscription_id in subscription_names_map:
                        vnet_data['subscriptionName'] = subscription_names_map[vnet_subscription_id]

                    # Parse ARG response into VirtualNetworkModel
                    # The model's @model_validator will handle nested structure extraction
                    vnet = VirtualNetworkModel(**vnet_data)
                    virtual_networks.append(vnet)
                    logging.debug(f"Collected topology for VNet: {vnet.name}")
                except Exception as e:
                    logging.warning(f"Failed to parse VNet data for {vnet_data.get('name', 'unknown')}: {e}")
                    continue

        # Collect gateway and firewall resources for VNets
        try:
            vnet_resource_ids = [vnet.resource_id for vnet in virtual_networks if vnet.resource_id]
            # Create mapping of VNet name to resource_id for name-based matching
            vnet_name_to_resource_id = {vnet.name: vnet.resource_id for vnet in virtual_networks if vnet.resource_id}
            # Create mapping of VNet resource_id to resource_group and subscription for fallback matching
            vnet_metadata = {}
            for vnet in virtual_networks:
                if vnet.resource_id:
                    vnet_metadata[vnet.resource_id] = {
                        'resource_group': vnet.resource_group_name,
                        'subscription_id': vnet.subscription_id,
                        'name': vnet.name
                    }
            logging.debug(f"Collecting gateway/firewall resources for {len(vnet_resource_ids)} VNet(s) with resource IDs")
            if vnet_resource_ids:
                gateway_firewall_data = collect_gateway_and_firewall_resources(
                    vnet_resource_ids,
                    subscription_ids,
                    credential,
                    vnet_name_to_resource_id,  # Pass name mapping for fallback matching
                    vnet_metadata  # Pass VNet metadata for resource group matching
                )

                # Attach gateway/firewall data to each VNet
                # Use model_copy() to update fields (Pydantic v2 safe way)
                updated_vnets = []
                for vnet in virtual_networks:
                    if vnet.resource_id:
                        # Try exact match first
                        if vnet.resource_id in gateway_firewall_data:
                            fw_data = gateway_firewall_data[vnet.resource_id].get('firewalls', [])
                            gw_data = gateway_firewall_data[vnet.resource_id].get('gateways', [])
                            updated_vnet = vnet.model_copy(update={
                                'virtual_network_gateways': gw_data,
                                'azure_firewalls': fw_data
                            })
                            updated_vnets.append(updated_vnet)
                        else:
                            # Try normalized match (case-insensitive, trailing slash)
                            vnet_id_normalized = vnet.resource_id.rstrip('/').lower()
                            matched = False
                            for key in gateway_firewall_data.keys():
                                key_normalized = key.rstrip('/').lower()
                                if key_normalized == vnet_id_normalized:
                                    fw_data = gateway_firewall_data[key].get('firewalls', [])
                                    gw_data = gateway_firewall_data[key].get('gateways', [])
                                    updated_vnet = vnet.model_copy(update={
                                        'virtual_network_gateways': gw_data,
                                        'azure_firewalls': fw_data
                                    })
                                    updated_vnets.append(updated_vnet)
                                    matched = True
                                    break
                            if not matched:
                                updated_vnets.append(vnet)
                    else:
                        updated_vnets.append(vnet)
                virtual_networks = updated_vnets
        except Exception as e:
            # If gateway/firewall collection fails, log but don't fail entire collection
            # VNets will still work with fallback subnet-based detection
            logging.warning(f"Failed to collect gateway/firewall resources: {e}")

        logging.info(f"Successfully collected topology for {len(virtual_networks)} VNet(s)")

        return TopologyModel(
            virtual_networks=virtual_networks,
            collected_at=datetime.utcnow().isoformat()
        )

    except AzureError as e:
        logging.error(f"Failed to collect topology via ARG: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error collecting topology: {e}")
        raise AzureError(f"Failed to collect topology: {e}") from e


def collect_connections(
    subscription_ids: list[str],
    credential: Any,
    ) -> list[ConnectionModel]:
    """Collect all Connections (VPN and ExpressRoute) using Azure Resource Graph.

    Args:
        subscription_ids: List of subscription IDs to search in
        credential: Azure credential object

    Returns:
        List of ConnectionModel objects
    """
    connections: list[ConnectionModel] = []

    try:
        resource_graph_client = ResourceGraphClient(credential)

        # Query for Connections
        # Note: ARG flattens nested properties with underscores
        # properties.virtualNetworkGateway1.id becomes properties_virtualNetworkGateway1_id
        # Some fields may be missing depending on connection type
        connection_query = """
        Resources
        | where type =~ 'microsoft.network/connections'
        | project
            name,
            subscriptionId,
            resourceGroup,
            location,
            id,
            properties.connectionType,
            properties.connectionStatus,
            properties.connectionProtocol,
            properties.connectionMode,
            properties.virtualNetworkGateway1,
            properties.localNetworkGateway2,
            properties.peer,
            properties.routingWeight,
            properties.sharedKey,
            properties.authenticationType,
            properties.enableBgp,
            properties.usePolicyBasedTrafficSelectors,
            properties.ipsecPolicies,
            properties.dpdTimeoutSeconds,
            properties.ingressBytesTransferred,
            properties.egressBytesTransferred
        """

        query_request = QueryRequest(
            subscriptions=subscription_ids,
            query=connection_query
        )

        @retry_with_backoff(max_retries=2)
        def _query_connections():
            return resource_graph_client.resources(query_request)

        response = _query_connections()

        if response.data:
            logging.info(f"Found {len(response.data)} connection(s) via ARG query")
            for conn_data in response.data:
                try:
                    # ARG returns properties with underscores (e.g., properties_connectionType)
                    # For nested objects like virtualNetworkGateway1, we need to extract the id field
                    vnet_gw1 = conn_data.get('properties_virtualNetworkGateway1', {})
                    vnet_gateway_id = vnet_gw1.get('id') if isinstance(vnet_gw1, dict) else None
                    
                    lng_gw2 = conn_data.get('properties_localNetworkGateway2', {})
                    local_gateway_id = lng_gw2.get('id') if isinstance(lng_gw2, dict) else None
                    
                    peer_obj = conn_data.get('properties_peer', {})
                    peer_id = peer_obj.get('id') if isinstance(peer_obj, dict) else None

                    # IPsec policies may be an array or None
                    ipsec_policies = conn_data.get('properties_ipsecPolicies', [])
                    if not isinstance(ipsec_policies, list):
                        ipsec_policies = []

                    connection = ConnectionModel(
                        name=conn_data.get('name', ''),
                        resource_id=conn_data.get('id', ''),
                        subscription_id=conn_data.get('subscriptionId', ''),
                        resource_group_name=conn_data.get('resourceGroup', ''),
                        location=conn_data.get('location', ''),
                        connection_type=conn_data.get('properties_connectionType', 'IPsec'),
                        connection_status=conn_data.get('properties_connectionStatus'),
                        connection_protocol=conn_data.get('properties_connectionProtocol'),
                        connection_mode=conn_data.get('properties_connectionMode'),
                        virtual_network_gateway_id=vnet_gateway_id,
                        local_network_gateway_id=local_gateway_id,
                        peer_id=peer_id,
                        routing_weight=conn_data.get('properties_routingWeight'),
                        shared_key=conn_data.get('properties_sharedKey'),  # May be None for security
                        authentication_type=conn_data.get('properties_authenticationType'),
                        enable_bgp=conn_data.get('properties_enableBgp', False),
                        use_policy_based_traffic_selectors=conn_data.get('properties_usePolicyBasedTrafficSelectors', False),
                        ipsec_policies=ipsec_policies,
                        dpd_timeout_seconds=conn_data.get('properties_dpdTimeoutSeconds'),
                        ingress_bytes_transferred=conn_data.get('properties_ingressBytesTransferred'),
                        egress_bytes_transferred=conn_data.get('properties_egressBytesTransferred'),
                    )
                    connections.append(connection)
                except Exception as e:
                    logging.warning(f"Failed to parse connection data for {conn_data.get('name', 'unknown')}: {e}")
                    logging.debug(f"Connection data keys: {list(conn_data.keys())}")
                    continue
        else:
            logging.info("No connections found via ARG query")

        return connections

    except AzureError as e:
        logging.error(f"Failed to query connections via ARG: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error collecting connections: {e}")
        raise AzureError(f"Failed to collect connections: {e}") from e


def collect_local_network_gateways(
    subscription_ids: list[str],
    credential: Any,
    ) -> list[LocalNetworkGatewayModel]:
    """Collect all Local Network Gateways using Azure Resource Graph.

    Args:
        subscription_ids: List of subscription IDs to search in
        credential: Azure credential object

    Returns:
        List of LocalNetworkGatewayModel objects
    """
    local_gateways: list[LocalNetworkGatewayModel] = []

    try:
        resource_graph_client = ResourceGraphClient(credential)

        # Query for Local Network Gateways
        lng_query = """
        Resources
        | where type == 'microsoft.network/localnetworkgateways'
        | project
            name,
            subscriptionId,
            resourceGroup,
            location,
            id,
            properties.provisioningState,
            properties.resourceGuid,
            properties.gatewayIpAddress,
            properties.fqdn,
            properties.localNetworkAddressSpace.addressPrefixes,
            properties.bgpSettings
        """

        query_request = QueryRequest(
            subscriptions=subscription_ids,
            query=lng_query
        )

        @retry_with_backoff(max_retries=2)
        def _query_local_gateways():
            return resource_graph_client.resources(query_request)

        response = _query_local_gateways()

        if response.data:
            logging.info(f"Found {len(response.data)} local network gateway(s) via ARG query")
            for lng_data in response.data:
                try:
                    # ARG returns properties with underscores
                    address_prefixes = lng_data.get('properties_localNetworkAddressSpace_addressPrefixes', [])
                    if not isinstance(address_prefixes, list):
                        address_prefixes = []

                    # BGP settings may be an object or None
                    bgp_settings = lng_data.get('properties_bgpSettings')
                    if not isinstance(bgp_settings, dict):
                        bgp_settings = None

                    # FQDN may be empty string or None
                    fqdn = lng_data.get('properties_fqdn')
                    if fqdn == '':
                        fqdn = None

                    local_gateway = LocalNetworkGatewayModel(
                        name=lng_data.get('name', ''),
                        resource_id=lng_data.get('id', ''),
                        subscription_id=lng_data.get('subscriptionId', ''),
                        resource_group_name=lng_data.get('resourceGroup', ''),
                        location=lng_data.get('location', ''),
                        provisioning_state=lng_data.get('properties_provisioningState'),
                        resource_guid=lng_data.get('properties_resourceGuid'),
                        gateway_ip_address=lng_data.get('properties_gatewayIpAddress'),
                        fqdn=fqdn,
                        address_prefixes=address_prefixes,
                        bgp_settings=bgp_settings,
                    )
                    local_gateways.append(local_gateway)
                except Exception as e:
                    logging.warning(f"Failed to parse local network gateway data for {lng_data.get('name', 'unknown')}: {e}")
                    continue
        else:
            logging.info("No local network gateways found via ARG query")

        return local_gateways

    except AzureError as e:
        logging.error(f"Failed to query local network gateways via ARG: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error collecting local network gateways: {e}")
        raise AzureError(f"Failed to collect local network gateways: {e}") from e


def collect_hybrid_connectivity(
    topology: TopologyModel,
    subscription_ids: list[str],
    credential: Any,
    ) -> dict[str, Any]:
    """Collect and correlate hybrid connectivity data (Connections and Local Network Gateways).

    Correlates connections and local network gateways with existing VNets and Gateways from topology.

    Args:
        topology: TopologyModel containing VNets and gateways
        subscription_ids: List of subscription IDs to search in
        credential: Azure credential object

    Returns:
        Dictionary with correlated hybrid connectivity data:
        {
            'connections': [ConnectionModel, ...],
            'local_network_gateways': [LocalNetworkGatewayModel, ...],
            'vnet_to_connections': {vnet_name: [ConnectionModel, ...]},
            'gateway_to_connections': {gateway_resource_id: [ConnectionModel, ...]},
            'connection_to_local_gateway': {connection_resource_id: LocalNetworkGatewayModel},
            'connection_to_peer_gateway': {connection_resource_id: VirtualNetworkGateway dict}
        }
    """
    logging.info("Collecting hybrid connectivity data (Connections and Local Network Gateways)...")

    # Collect connections and local network gateways
    connections = collect_connections(subscription_ids, credential)
    local_network_gateways = collect_local_network_gateways(subscription_ids, credential)

    # Helper function to normalize resource IDs for matching (case-insensitive, strip trailing slashes)
    def normalize_resource_id(resource_id: str | None) -> str | None:
        if not resource_id:
            return None
        return resource_id.rstrip('/').lower()

    # Create mappings for correlation (with normalized IDs for better matching)
    local_gateway_by_id: dict[str, LocalNetworkGatewayModel] = {}
    local_gateway_by_normalized_id: dict[str, LocalNetworkGatewayModel] = {}
    for lng in local_network_gateways:
        if lng.resource_id:
            local_gateway_by_id[lng.resource_id] = lng
            normalized = normalize_resource_id(lng.resource_id)
            if normalized:
                local_gateway_by_normalized_id[normalized] = lng

    vnet_by_resource_id = {vnet.resource_id: vnet for vnet in topology.virtual_networks if vnet.resource_id}
    gateway_by_resource_id: dict[str, dict] = {}
    gateway_by_normalized_id: dict[str, dict] = {}
    gateway_to_vnet: dict[str, str] = {}  # Map gateway resource_id -> vnet_name

    # Build gateway mapping from VNets
    for vnet in topology.virtual_networks:
        for gateway in vnet.virtual_network_gateways:
            gw_resource_id = gateway.get('resource_id')
            if gw_resource_id:
                gateway_by_resource_id[gw_resource_id] = gateway
                normalized = normalize_resource_id(gw_resource_id)
                if normalized:
                    gateway_by_normalized_id[normalized] = gateway
                    gateway_to_vnet[gw_resource_id] = vnet.name
                    # Also map normalized ID to VNet
                    if normalized:
                        gateway_to_vnet[normalized] = vnet.name

    # Correlate connections with VNets and Gateways
    vnet_to_connections: dict[str, list[ConnectionModel]] = {}
    gateway_to_connections: dict[str, list[ConnectionModel]] = {}
    connection_to_local_gateway: dict[str, LocalNetworkGatewayModel] = {}
    connection_to_peer_gateway: dict[str, dict] = {}

    for connection in connections:
        # Find VNet from gateway (try exact match first, then normalized)
        vnet_name = None
        if connection.virtual_network_gateway_id:
            # Try exact match first
            vnet_name = gateway_to_vnet.get(connection.virtual_network_gateway_id)
            
            # If not found, try normalized match
            if not vnet_name:
                normalized_gw_id = normalize_resource_id(connection.virtual_network_gateway_id)
                if normalized_gw_id:
                    vnet_name = gateway_to_vnet.get(normalized_gw_id)
                    # Also update the gateway mapping if we found it via normalized ID
                    if normalized_gw_id in gateway_by_normalized_id:
                        gateway_by_resource_id[connection.virtual_network_gateway_id] = gateway_by_normalized_id[normalized_gw_id]

        # Map connection to VNet
        if vnet_name:
            if vnet_name not in vnet_to_connections:
                vnet_to_connections[vnet_name] = []
            vnet_to_connections[vnet_name].append(connection)

        # Map connection to gateway (exact or normalized match)
        if connection.virtual_network_gateway_id:
            gateway = gateway_by_resource_id.get(connection.virtual_network_gateway_id)
            if not gateway:
                normalized_gw_id = normalize_resource_id(connection.virtual_network_gateway_id)
                if normalized_gw_id:
                    gateway = gateway_by_normalized_id.get(normalized_gw_id)
            
            if gateway:
                # Use normalized ID as key for consistency
                normalized_key = normalize_resource_id(connection.virtual_network_gateway_id) or connection.virtual_network_gateway_id
                if normalized_key not in gateway_to_connections:
                    gateway_to_connections[normalized_key] = []
                gateway_to_connections[normalized_key].append(connection)

        # Map connection to local network gateway (for S2S VPN)
        if connection.local_network_gateway_id:
            # Try exact match first
            local_gateway = local_gateway_by_id.get(connection.local_network_gateway_id)
            # If not found, try normalized match
            if not local_gateway:
                normalized_lng_id = normalize_resource_id(connection.local_network_gateway_id)
                if normalized_lng_id:
                    local_gateway = local_gateway_by_normalized_id.get(normalized_lng_id)
            
            if local_gateway:
                connection_to_local_gateway[connection.resource_id] = local_gateway

        # Map connection to peer gateway (for VNet-to-VNet) or ExpressRoute Circuit
        if connection.peer_id:
            # Check if it's an ExpressRoute Circuit (not a gateway)
            if 'expressRouteCircuits' in connection.peer_id.lower():
                # ExpressRoute Circuit - no gateway correlation needed
                pass
            else:
                # Try to find peer gateway
                peer_gateway = gateway_by_resource_id.get(connection.peer_id)
                if not peer_gateway:
                    normalized_peer_id = normalize_resource_id(connection.peer_id)
                    if normalized_peer_id:
                        peer_gateway = gateway_by_normalized_id.get(normalized_peer_id)
                
                if peer_gateway:
                    connection_to_peer_gateway[connection.resource_id] = peer_gateway

    # Calculate correlation statistics
    correlated_connections = sum(len(conns) for conns in vnet_to_connections.values())
    uncorrelated_connections = len(connections) - correlated_connections
    connections_with_lng = len(connection_to_local_gateway)
    connections_with_peer = len(connection_to_peer_gateway)

    result = {
        'connections': connections,
        'local_network_gateways': local_network_gateways,
        'vnet_to_connections': vnet_to_connections,
        'gateway_to_connections': gateway_to_connections,
        'connection_to_local_gateway': connection_to_local_gateway,
        'connection_to_peer_gateway': connection_to_peer_gateway,
    }

    logging.info(
        f"Hybrid connectivity collected: {len(connections)} connection(s), "
        f"{len(local_network_gateways)} local network gateway(s)"
    )
    logging.info(
        f"Correlation stats: {correlated_connections} connection(s) correlated with VNets, "
        f"{uncorrelated_connections} uncorrelated, {connections_with_lng} with Local Network Gateway, "
        f"{connections_with_peer} with peer gateway/circuit"
    )

    # Log uncorrelated connections for debugging
    if uncorrelated_connections > 0:
        uncorrelated = [
            conn for conn in connections
            if not any(conn.resource_id in [c.resource_id for c in conns] for conns in vnet_to_connections.values())
        ]
        for conn in uncorrelated:
            logging.debug(
                f"Uncorrelated connection: {conn.name} "
                f"(Gateway ID: {conn.virtual_network_gateway_id})"
            )

    return result
