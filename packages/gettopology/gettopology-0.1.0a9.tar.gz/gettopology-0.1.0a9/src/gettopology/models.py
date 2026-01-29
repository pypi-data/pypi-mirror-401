"""Utility classes and models for data validation and topology representation."""

from __future__ import annotations

import re
from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator


def extract_vnet_name_from_id(resource_id: str) -> str | None:
    """Extract VNet name from Azure resource ID URI using regex.

    Format: /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/virtualNetworks/{vnet}

    Examples:
        /subscriptions/.../virtualNetworks/vnet-hub -> "vnet-hub"

    Args:
        resource_id: Azure resource ID URI

    Returns:
        VNet name or None if not found
    """
    if not resource_id:
        return None

    # Pattern: /virtualNetworks/{vnet_name} or /virtualNetworks/{vnet_name}/
    pattern = r'/virtualNetworks/([^/]+)'
    match = re.search(pattern, resource_id)
    return match.group(1) if match else None


def extract_subnet_name_from_id(resource_id: str) -> str | None:
    """Extract subnet name from Azure resource ID URI using regex.

    Format: /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/virtualNetworks/{vnet}/subnets/{subnet}

    Examples:
        /subscriptions/.../virtualNetworks/vnet-hub/subnets/subnet-api -> "subnet-api"

    Args:
        resource_id: Azure resource ID URI

    Returns:
        Subnet name or None if not found
    """
    if not resource_id:
        return None

    # Pattern: /subnets/{subnet_name} or /subnets/{subnet_name}/
    pattern = r'/subnets/([^/]+)'
    match = re.search(pattern, resource_id)
    return match.group(1) if match else None


def extract_subscription_id_from_id(resource_id: str) -> str | None:
    """Extract subscription ID from Azure resource ID URI using regex.

    Format: /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/virtualNetworks/{vnet}

    Examples:
        /subscriptions/dd4ceca7-a12c-4410-8d7c-281563beb7be/resourceGroups/rg/providers/...
        -> "dd4ceca7-a12c-4410-8d7c-281563beb7be"

    Args:
        resource_id: Azure resource ID URI

    Returns:
        Subscription ID or None if not found
    """
    if not resource_id:
        return None

    # Pattern: /subscriptions/{subscription_id}/
    pattern = r'/subscriptions/([^/]+)'
    match = re.search(pattern, resource_id)
    return match.group(1) if match else None


def extract_nsg_name_from_id(resource_id: str) -> str | None:
    """Extract NSG name from Azure resource ID URI using regex.

    Format: /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/networkSecurityGroups/{nsg}

    Examples:
        /subscriptions/.../networkSecurityGroups/nsg-subnetweb -> "nsg-subnetweb"

    Args:
        resource_id: Azure resource ID URI

    Returns:
        NSG name or None if not found
    """
    if not resource_id:
        return None

    # Pattern: /networkSecurityGroups/{nsg_name}
    pattern = r'/networkSecurityGroups/([^/]+)'
    match = re.search(pattern, resource_id)
    return match.group(1) if match else None


def extract_route_table_name_from_id(resource_id: str) -> str | None:
    """Extract Route Table name from Azure resource ID URI using regex.

    Format: /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/routeTables/{rt}

    Examples:
        /subscriptions/.../routeTables/rt-tunnel -> "rt-tunnel"

    Args:
        resource_id: Azure resource ID URI

    Returns:
        Route Table name or None if not found
    """
    if not resource_id:
        return None

    # Pattern: /routeTables/{route_table_name}
    pattern = r'/routeTables/([^/]+)'
    match = re.search(pattern, resource_id)
    return match.group(1) if match else None


def extract_private_endpoint_name_from_id(resource_id: str) -> str | None:
    """Extract Private Endpoint name from Azure resource ID URI using regex.

    Format: /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/privateEndpoints/{pe}

    Examples:
        /subscriptions/.../privateEndpoints/STORAGEPVT -> "STORAGEPVT"

    Args:
        resource_id: Azure resource ID URI

    Returns:
        Private Endpoint name or None if not found
    """
    if not resource_id:
        return None

    # Pattern: /privateEndpoints/{private_endpoint_name}
    pattern = r'/privateEndpoints/([^/]+)'
    match = re.search(pattern, resource_id)
    if match:
        return match.group(1)
    return None


def extract_nat_gateway_name_from_id(resource_id: str) -> str | None:
    """Extract NAT Gateway name from Azure resource ID URI using regex.

    Format: /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/natGateways/{nat}

    Examples:
        /subscriptions/.../natGateways/nat-gw -> "nat-gw"

    Args:
        resource_id: Azure resource ID URI

    Returns:
        NAT Gateway name or None if not found
    """
    if not resource_id:
        return None

    # Pattern: /natGateways/{nat_gateway_name}
    pattern = r'/natGateways/([^/]+)'
    match = re.search(pattern, resource_id)
    return match.group(1) if match else None


class SubscriptionInput:
    """Utility class for subscription ID validation.

    This class provides subscription ID pattern matching and normalization
    functionality. It does not use Pydantic as it's only used for utility functions.
    """

    SUBSCRIPTION_ID_PATTERN: ClassVar[str] = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"

    @staticmethod
    def normalize_subscription_ids(sub_ids: list[str]) -> tuple[list[str], list[str]]:
        """Trim whitespace and validate subscription IDs using regex pattern.

        Args:
            sub_ids: List of subscription ID strings to normalize and validate

        Returns:
            tuple: (valid_ids, invalid_ids)
        """
        valid = []
        invalid = []

        # Validate each subscription ID using regex
        for sub_id in sub_ids:
            trimmed = sub_id.strip()
            if not trimmed:  # Skip empty strings
                continue

            # Validate UUID format using regex
            if re.match(SubscriptionInput.SUBSCRIPTION_ID_PATTERN, trimmed):
                valid.append(trimmed)
            else:
                invalid.append(trimmed)

        return valid, invalid


class SubnetModel(BaseModel):
    """Model representing a subnet within a virtual network.

    Handles nested ARG structure where subnet properties are wrapped in a 'properties' object.
    """

    name: str = Field(..., description="Subnet name")
    address_prefix: str = Field(..., description="Subnet address prefix (CIDR) - first prefix for backward compatibility")
    address_prefixes: list[str] = Field(
        default_factory=list,
        description="Subnet address prefixes (CIDR) - can have multiple prefixes"
    )
    network_security_group_id: str | None = Field(
        None,
        description="Network Security Group resource ID (if attached)"
    )
    network_security_group_name: str | None = Field(
        None,
        description="Network Security Group name (extracted from resource ID)"
    )
    private_link_service_network_policies: Literal["Enabled", "Disabled"] = Field(
        "Enabled",
        description="Private Link Service network policies"
    )
    private_endpoint_network_policies: Literal["Enabled", "Disabled"] = Field(
        "Enabled",
        description="Private Endpoint network policies"
    )
    delegations: list[dict] = Field(default_factory=list, description="Subnet delegations")
    delegation_names: list[str] = Field(
        default_factory=list,
        description="Delegation service names (extracted from delegations)"
    )
    default_outbound_access: bool = Field(
        False,
        description="Default outbound access enabled"
    )
    route_table_id: str | None = Field(
        None,
        description="Route table resource ID (if attached)"
    )
    route_table_name: str | None = Field(
        None,
        description="Route table name (extracted from resource ID)"
    )
    nat_gateway_id: str | None = Field(
        None,
        description="NAT Gateway resource ID (if attached)"
    )
    nat_gateway_name: str | None = Field(
        None,
        description="NAT Gateway name (extracted from resource ID)"
    )
    private_endpoint_id: str | None = Field(
        None,
        description="Private Endpoint resource ID (if attached to this subnet)"
    )
    private_endpoint_name: str | None = Field(
        None,
        description="Private Endpoint name (extracted from resource ID)"
    )

    @model_validator(mode='before')
    @classmethod
    def extract_from_nested_structure(cls, data: Any) -> dict[str, Any]:
        """Extract subnet data from ARG's nested structure.

        ARG returns subnets with a 'properties' wrapper:
        {
            "name": "subnet-name",
            "id": "/subscriptions/.../subnets/subnet-name",
            "properties": {
                "addressPrefix": "10.0.0.0/24",
                "networkSecurityGroup": {"id": "/subscriptions/.../nsg-name"},
                "routeTable": {"id": "/subscriptions/.../rt-name"},
                ...
            }
        }
        """
        if isinstance(data, dict):
            # If we have a 'properties' wrapper, extract from it
            if 'properties' in data:
                props = data['properties']
                # Extract name from 'name' field or fallback to extracting from 'id' URI using regex
                subnet_id = data.get('id', '')
                subnet_name = data.get('name', '')
                if not subnet_name and subnet_id:
                    # Fallback: extract name from resource ID URI using regex
                    subnet_name = extract_subnet_name_from_id(subnet_id) or ''

                # Extract address prefixes - can be single addressPrefix or array addressPrefixes
                address_prefixes_list = props.get('addressPrefixes', [])
                if not address_prefixes_list:
                    # Fallback to single addressPrefix if addressPrefixes not found
                    single_prefix = props.get('addressPrefix', '')
                    if single_prefix:
                        address_prefixes_list = [single_prefix]

                # Ensure it's a list
                if not isinstance(address_prefixes_list, list):
                    address_prefixes_list = [address_prefixes_list] if address_prefixes_list else []

                result = {
                    'name': subnet_name,  # Just the subnet name, e.g., "subnet-api" (extracted from name field or resource ID URI)
                    'address_prefixes': address_prefixes_list,
                    # For backward compatibility, set address_prefix to first prefix
                    'address_prefix': address_prefixes_list[0] if address_prefixes_list else '',
                    'private_link_service_network_policies': props.get('privateLinkServiceNetworkPolicies', 'Enabled'),
                    'private_endpoint_network_policies': props.get('privateEndpointNetworkPolicies', 'Enabled'),
                    'delegations': props.get('delegations', []),
                    'default_outbound_access': props.get('defaultOutboundAccess', False),
                }

                # Extract NSG ID and name from nested object
                nsg = props.get('networkSecurityGroup')
                if isinstance(nsg, dict):
                    nsg_id = nsg.get('id')
                    result['network_security_group_id'] = nsg_id
                    result['network_security_group_name'] = extract_nsg_name_from_id(nsg_id) if nsg_id else None
                else:
                    result['network_security_group_id'] = None
                    result['network_security_group_name'] = None

                # Extract Route Table ID and name from nested object
                rt = props.get('routeTable')
                if isinstance(rt, dict):
                    rt_id = rt.get('id')
                    result['route_table_id'] = rt_id
                    result['route_table_name'] = extract_route_table_name_from_id(rt_id) if rt_id else None
                else:
                    result['route_table_id'] = None
                    result['route_table_name'] = None

                # Extract NAT Gateway ID and name from nested object
                nat_gw = props.get('natGateway')
                if isinstance(nat_gw, dict):
                    nat_gw_id = nat_gw.get('id')
                    result['nat_gateway_id'] = nat_gw_id
                    result['nat_gateway_name'] = extract_nat_gateway_name_from_id(nat_gw_id) if nat_gw_id else None
                else:
                    result['nat_gateway_id'] = None
                    result['nat_gateway_name'] = None

                # Extract Private Endpoint ID and name from privateEndpoints array
                # privateEndpoints is an array of objects with 'id' fields
                private_endpoints = props.get('privateEndpoints', [])
                if isinstance(private_endpoints, list) and len(private_endpoints) > 0:
                    # Get the first private endpoint (subnets can have multiple, but we'll show icon if any exist)
                    first_pe = private_endpoints[0]
                    if isinstance(first_pe, dict):
                        pe_id = first_pe.get('id')
                        result['private_endpoint_id'] = pe_id
                        result['private_endpoint_name'] = extract_private_endpoint_name_from_id(pe_id) if pe_id else None
                    else:
                        result['private_endpoint_id'] = None
                        result['private_endpoint_name'] = None
                else:
                    result['private_endpoint_id'] = None
                    result['private_endpoint_name'] = None

                # Extract delegation names from delegations array
                delegations = props.get('delegations', [])
                delegation_names = []
                for delegation in delegations:
                    if isinstance(delegation, dict):
                        # Try to get name from 'name' field first
                        delegation_name = delegation.get('name')
                        if not delegation_name:
                            # Fallback to 'serviceName' in properties
                            delegation_props = delegation.get('properties', {})
                            delegation_name = delegation_props.get('serviceName')
                        if delegation_name:
                            delegation_names.append(delegation_name)
                result['delegation_names'] = delegation_names

                return result
            else:
                # Already flattened or direct structure
                # Still need to extract names from IDs if they exist
                if isinstance(data, dict):
                    # Extract NSG name if NSG ID exists
                    if 'network_security_group_id' in data and data['network_security_group_id']:
                        data['network_security_group_name'] = extract_nsg_name_from_id(data['network_security_group_id'])
                    elif 'network_security_group_name' not in data:
                        data['network_security_group_name'] = None

                    # Extract Route Table name if Route Table ID exists
                    if 'route_table_id' in data and data['route_table_id']:
                        data['route_table_name'] = extract_route_table_name_from_id(data['route_table_id'])
                    elif 'route_table_name' not in data:
                        data['route_table_name'] = None

                    # Extract NAT Gateway name if NAT Gateway ID exists
                    if 'nat_gateway_id' in data and data['nat_gateway_id']:
                        data['nat_gateway_name'] = extract_nat_gateway_name_from_id(data['nat_gateway_id'])
                    elif 'nat_gateway_name' not in data:
                        data['nat_gateway_name'] = None

                    # Extract delegation names if delegations exist
                    if 'delegations' in data and isinstance(data['delegations'], list):
                        delegation_names = []
                        for delegation in data['delegations']:
                            if isinstance(delegation, dict):
                                delegation_name = delegation.get('name')
                                if not delegation_name:
                                    delegation_props = delegation.get('properties', {})
                                    delegation_name = delegation_props.get('serviceName')
                                if delegation_name:
                                    delegation_names.append(delegation_name)
                        data['delegation_names'] = delegation_names
                    elif 'delegation_names' not in data:
                        data['delegation_names'] = []

                return data
        return data

    model_config = ConfigDict(populate_by_name=True)


class VirtualNetworkModel(BaseModel):
    """Model representing a virtual network and its topology information.

    Handles nested ARG structure where VNet properties are wrapped in a 'properties' object.
    """

    name: str = Field(..., description="Virtual network name")
    address_space: list[str] = Field(
        ...,
        description="List of address prefixes (CIDR blocks)"
    )
    subnets: list[SubnetModel] = Field(default_factory=list, description="List of subnets")
    tenant_id: str = Field(..., description="Azure tenant ID")
    subscription_id: str = Field(..., description="Azure subscription ID")
    subscription_name: str | None = Field(None, description="Azure subscription name")
    resource_group_name: str = Field(..., description="Resource group name")
    location: str = Field(..., description="Azure region/location")
    private_endpoint_vnet_policies: Literal["Enabled", "Disabled"] = Field(
        "Disabled",
        description="Private endpoint VNet policies"
    )
    enable_ddos_protection: bool = Field(
        False,
        description="DDoS protection enabled"
    )
    peering_resource_ids: list[str] = Field(
        default_factory=list,
        description="List of peered virtual network resource IDs (full URIs)"
    )
    peering_names: list[str] = Field(
        default_factory=list,
        description="List of peered virtual network names (extracted from resource IDs)"
    )
    peering_local_flags: list[bool] = Field(
        default_factory=list,
        description="List of booleans indicating if each peering is local (same subscription) or cross-subscription"
    )
    peering_count: int = Field(0, description="Number of peerings")
    resource_id: str | None = Field(
        None,
        description="VNet resource ID (full Azure resource URI)"
    )
    virtual_network_gateways: list[dict] = Field(
        default_factory=list,
        description="List of Virtual Network Gateways in this VNet"
    )
    azure_firewalls: list[dict] = Field(
        default_factory=list,
        description="List of Azure Firewalls in this VNet"
    )

    @model_validator(mode='before')
    @classmethod
    def extract_from_nested_structure(cls, data: Any) -> dict[str, Any]:
        """Extract VNet data from ARG's nested structure.

        ARG returns VNets with a 'properties' wrapper:
        {
            "id": "/subscriptions/.../vnets/vnet-name",
            "name": "vnet-name",
            "tenantId": "...",
            "subscriptionId": "...",
            "resourceGroup": "rg-name",
            "location": "eastus",
            "tags": {...},
            "properties": {
                "addressSpace": {"addressPrefixes": ["10.0.0.0/16"]},
                "subnets": [...],
                "virtualNetworkPeerings": [...],
                "enableDdosProtection": false,
                "privateEndpointVNetPolicies": "Disabled"
            }
        }

        If data is already properly structured (e.g., from synthetic topology),
        skip extraction and return as-is.
        """
        if isinstance(data, dict):
            # Check if this is already a properly structured dict (not from ARG)
            # If 'subnets' exists and is a list of objects (not nested in 'properties'),
            # or if 'properties' doesn't exist, skip extraction
            if 'properties' not in data and ('subnets' in data or 'address_space' in data):
                # Already properly structured, return as-is
                return data

            # Check if subnets are already SubnetModel objects or properly structured
            if 'subnets' in data and isinstance(data['subnets'], list) and len(data['subnets']) > 0:
                # If first subnet is already a dict with 'name' at top level (not nested in 'properties'),
                # or is a SubnetModel instance, this is already structured
                first_subnet = data['subnets'][0]
                if isinstance(first_subnet, dict) and 'name' in first_subnet:
                    # Check if it's nested (ARG format) or flat (already structured)
                    if 'properties' not in first_subnet:
                        # Already structured, return as-is
                        return data
            # Extract top-level fields
            # Extract name from 'name' field or fallback to extracting from 'id' URI using regex
            vnet_id = data.get('id', '')
            vnet_name = data.get('name', '')
            if not vnet_name and vnet_id:
                # Fallback: extract name from resource ID URI using regex
                vnet_name = extract_vnet_name_from_id(vnet_id) or ''

            result = {
                'name': vnet_name,  # Just the VNet name, e.g., "vnet-hub" (extracted from name field or resource ID URI)
                'tenant_id': data.get('tenantId', ''),
                'subscription_id': data.get('subscriptionId', ''),
                'subscription_name': data.get('subscriptionName'),  # Added by collect_topology
                'resource_group_name': data.get('resourceGroup', ''),
                'location': data.get('location', ''),
                'resource_id': data.get('id'),  # Extract VNet resource ID from ARG response
            }

            # Extract from nested 'properties' object
            props = data.get('properties', {})

            # Extract address space
            address_space_obj = props.get('addressSpace', {})
            if isinstance(address_space_obj, dict):
                result['address_space'] = address_space_obj.get('addressPrefixes', [])
            else:
                result['address_space'] = []

            # Extract subnets (they also have nested structure, but SubnetModel handles that)
            result['subnets'] = props.get('subnets', [])

            # Extract peerings - get remoteVirtualNetwork.id from each peering
            # Extract VNet names from peering resource IDs using regex
            # Determine if each peering is local (same subscription) or cross-subscription
            peerings = props.get('virtualNetworkPeerings', [])
            peering_ids = []
            peering_names = []
            peering_local_flags = []

            # Get source VNet subscription ID for comparison
            source_subscription_id = data.get('subscriptionId', '')

            for peering in peerings:
                if isinstance(peering, dict):
                    peering_props = peering.get('properties', {})
                    remote_vnet = peering_props.get('remoteVirtualNetwork', {})
                    if isinstance(remote_vnet, dict):
                        remote_id = remote_vnet.get('id')
                        if remote_id:
                            peering_ids.append(remote_id)
                            # Extract VNet name from peering resource ID using regex
                            remote_name = extract_vnet_name_from_id(remote_id)
                            if remote_name:
                                peering_names.append(remote_name)

                            # Determine if peering is local (same subscription) or cross-subscription
                            remote_subscription_id = extract_subscription_id_from_id(remote_id)
                            is_local = (remote_subscription_id == source_subscription_id) if remote_subscription_id else False
                            peering_local_flags.append(is_local)

            result['peering_resource_ids'] = peering_ids
            result['peering_names'] = peering_names  # Just the VNet names for easier diagram generation
            result['peering_local_flags'] = peering_local_flags  # Local vs cross-subscription flags
            result['peering_count'] = len(peering_ids)

            # Extract other properties
            result['enable_ddos_protection'] = props.get('enableDdosProtection', False)
            result['private_endpoint_vnet_policies'] = props.get('privateEndpointVNetPolicies', 'Disabled')

            return result
        return data

    @computed_field  # type: ignore[prop-decorator]
    @property
    def gateway_type(self) -> Literal["ExpressRoute", "Vpn", "None"]:
        """Return gateway type based on actual gateway resources (with fallback)."""
        # Check actual gateway resources first
        if self.virtual_network_gateways:
            gateway_type = self.virtual_network_gateways[0].get('gateway_type', '')
            if gateway_type == 'ExpressRoute':
                return "ExpressRoute"
            elif gateway_type == 'Vpn':
                return "Vpn"

        # If we have resource_id, we attempted resource collection
        # Empty list means no gateways found, so return "None" (don't fallback to subnet)
        if self.resource_id is not None:
            return "None"

        # Fallback: Only use subnet check if we haven't attempted resource collection
        # (for backward compatibility with old data or synthetic topologies)
        return "None"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def expressroute(self) -> Literal["Yes", "No"]:
        """Check if ExpressRoute gateway exists."""
        # Check actual gateway resources first
        if self.gateway_type == "ExpressRoute":
            return "Yes"

        # If we have resource_id, we attempted resource collection
        # Empty gateway list means no ExpressRoute gateway found
        if self.resource_id is not None:
            return "No"

        # Fallback: Only use subnet check if we haven't attempted resource collection
        # (for backward compatibility with old data or synthetic topologies)
        subnet_names = [subnet.name for subnet in self.subnets]
        return "Yes" if "GatewaySubnet" in subnet_names else "No"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def vpn_gateway(self) -> Literal["Yes", "No"]:
        """Check if VPN gateway exists."""
        # Check actual gateway resources first
        if self.gateway_type == "Vpn":
            return "Yes"

        # If we have resource_id, we attempted resource collection
        # Empty gateway list means no VPN gateway found
        if self.resource_id is not None:
            return "No"

        # Fallback: Only use subnet check if we haven't attempted resource collection
        # (for backward compatibility with old data or synthetic topologies)
        subnet_names = [subnet.name for subnet in self.subnets]
        return "Yes" if "GatewaySubnet" in subnet_names else "No"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def firewall(self) -> Literal["Yes", "No"]:
        """Check if Azure Firewall exists."""
        # Check actual firewall resources first
        if self.azure_firewalls:
            return "Yes"

        # If we have resource_id, we attempted resource collection
        # Empty firewall list means no firewall found
        if self.resource_id is not None:
            return "No"

        # Fallback: Only use subnet check if we haven't attempted resource collection
        # (for backward compatibility with old data or synthetic topologies)
        subnet_names = [subnet.name for subnet in self.subnets]
        return "Yes" if "AzureFirewallSubnet" in subnet_names else "No"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def hub(self) -> bool:
        """Determine if this is a hub VNet (has ExpressRoute, VPN Gateway, or Firewall)."""
        return self.expressroute == "Yes" or self.vpn_gateway == "Yes" or self.firewall == "Yes"

    model_config = ConfigDict(populate_by_name=True)  # Allow both field names and aliases


class LocalNetworkGatewayModel(BaseModel):
    """Model representing a Local Network Gateway (on-premises representation)."""

    name: str = Field(..., description="Local Network Gateway name")
    resource_id: str = Field(..., description="Full Azure resource ID")
    subscription_id: str = Field(..., description="Azure subscription ID")
    resource_group_name: str = Field(..., description="Resource group name")
    location: str = Field(..., description="Azure region/location")
    provisioning_state: str | None = Field(None, description="Provisioning state (e.g., Succeeded, Failed)")
    resource_guid: str | None = Field(None, description="Resource GUID")
    gateway_ip_address: str | None = Field(None, description="On-premises gateway IP address")
    fqdn: str | None = Field(None, description="Fully Qualified Domain Name (if using FQDN instead of IP)")
    address_prefixes: list[str] = Field(
        default_factory=list,
        description="List of on-premises address prefixes (CIDR blocks). Empty when BGP is used."
    )
    bgp_settings: dict | None = Field(
        None,
        description="BGP settings (bgpPeeringAddress, peerWeight, asn) if BGP is enabled"
    )

    model_config = ConfigDict(populate_by_name=True)


class ConnectionModel(BaseModel):
    """Model representing a Connection (VPN or ExpressRoute connection)."""

    name: str = Field(..., description="Connection name")
    resource_id: str = Field(..., description="Full Azure resource ID")
    subscription_id: str = Field(..., description="Azure subscription ID")
    resource_group_name: str = Field(..., description="Resource group name")
    location: str = Field(..., description="Azure region/location")
    connection_type: Literal["IPsec", "ExpressRoute", "VPNClient", "Vnet2Vnet"] = Field(
        ...,
        description="Connection type (IPsec for S2S, ExpressRoute, VPNClient, Vnet2Vnet)"
    )
    connection_status: str | None = Field(None, description="Connection status (e.g., Connected, NotConnected, Disconnected)")
    connection_protocol: str | None = Field(None, description="Connection protocol (e.g., IKEv1, IKEv2) - for VPN connections")
    connection_mode: str | None = Field(None, description="Connection mode (e.g., Default, InitiatorOnly, ResponderOnly)")
    virtual_network_gateway_id: str | None = Field(
        None,
        description="Resource ID of the Virtual Network Gateway (local gateway)"
    )
    local_network_gateway_id: str | None = Field(
        None,
        description="Resource ID of the Local Network Gateway (for S2S connections)"
    )
    peer_id: str | None = Field(
        None,
        description="Resource ID of peer (ExpressRoute Circuit for ER, or Gateway for VNet-to-VNet)"
    )
    routing_weight: int | None = Field(None, description="Routing weight")
    shared_key: str | None = Field(None, description="Shared key (PSK) - may be None for security")
    authentication_type: str | None = Field(None, description="Authentication type (e.g., PSK, EAP)")
    enable_bgp: bool = Field(False, description="BGP enabled")
    use_policy_based_traffic_selectors: bool = Field(
        False,
        description="Use policy-based traffic selectors (vs route-based)"
    )
    ipsec_policies: list[dict] = Field(
        default_factory=list,
        description="IPsec policies (encryption, integrity, PFS group, etc.) - for VPN connections"
    )
    dpd_timeout_seconds: int | None = Field(None, description="Dead Peer Detection (DPD) timeout in seconds")
    ingress_bytes_transferred: int | None = Field(None, description="Ingress bytes transferred")
    egress_bytes_transferred: int | None = Field(None, description="Egress bytes transferred")

    model_config = ConfigDict(populate_by_name=True)


class TopologyModel(BaseModel):
    """Model representing the complete network topology."""

    virtual_networks: list[VirtualNetworkModel] = Field(
        default_factory=list,
        description="List of virtual networks in the topology"
    )
    collected_at: str | None = Field(None, description="Timestamp when topology was collected")

    model_config = ConfigDict(populate_by_name=True)
