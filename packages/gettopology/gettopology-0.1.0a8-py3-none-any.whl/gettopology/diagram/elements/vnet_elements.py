"""VNet element creation functions for diagram generation."""

from xml.etree.ElementTree import Element, SubElement

from gettopology.diagram.config import get_config
from gettopology.models import VirtualNetworkModel

# Get global config instance
_config = get_config()


def calculate_vnet_height(vnet: VirtualNetworkModel) -> float:
    """Calculate the actual height of a VNet box including subnets.

    Args:
        vnet: VirtualNetworkModel to calculate height for

    Returns:
        Calculated height in pixels
    """
    subnet_padding_top = _config.subnet_padding_top
    subnet_height = _config.subnet_height
    subnet_spacing = _config.subnet_spacing
    subnet_padding_bottom = _config.subnet_padding_bottom
    min_vnet_height = max(_config.vnet_height_base, _config.vnet_min_height)

    if vnet.subnets:
        total_subnet_height = len(vnet.subnets) * (subnet_height + subnet_spacing) - subnet_spacing
        return subnet_padding_top + total_subnet_height + subnet_padding_bottom
    return min_vnet_height


def create_vnet_group(
    root: Element,
    cell_id: int,
    vnet: VirtualNetworkModel,
    x: float,
    y: float,
    width: float | None = None,
    height: float | None = None,
    is_hub: bool = False,
    is_stub: bool = False,
    primary_subscription_id: str | None = None,
    hub_subscription_id: str | None = None,
) -> tuple[int, int, int]:
    """Create a VNet group (object + mxCell) with metadata.

    Uses zone-based layout approach: creates a group container with the VNet box inside.

    Args:
        root: Root element to add the cell to
        cell_id: Starting cell ID (will be incremented for group and main)
        vnet: VirtualNetworkModel to represent
        x: X position
        y: Y position
        width: Shape width
        height: Shape height
        is_hub: Whether this is a hub VNet
        is_stub: Whether this is a stub/orphan VNet (no peerings)

    Returns:
        tuple: (group_id, main_id, final_cell_id) - IDs for connecting edges (use main_id), and final cell_id for next VNet
    """
    # Use config defaults if not provided
    if width is None:
        width = _config.vnet_width
    if height is None:
        height = _config.vnet_height_base

    # Build label text with proper HTML line breaks
    # Format: Subscription: Name / Resource Group (on first line, combined to save space)
    #         VNet name (on second line)
    #         Address space (on third line)
    label_parts = []
    # Combine subscription and resource group on first line to save space
    if vnet.subscription_name:
        sub_line = f"Sub: {vnet.subscription_name}"
    else:
        sub_line = f"Sub: {vnet.subscription_id[:8]}..."
    if vnet.resource_group_name:
        sub_line += f" / RG: {vnet.resource_group_name}"
    label_parts.append(sub_line)
    label_parts.append(vnet.name)
    if vnet.address_space:
        # Just show address space without "Address Space:" prefix
        label_parts.append(', '.join(vnet.address_space))
    else:
        label_parts.append("No address space")

    # Use HTML <br> tags for line breaks (html=1 in style enables HTML rendering)
    label = "<br>".join(label_parts)

    # Styling: Hubs are blue, stubs are teal, spokes are orange
    if is_hub:
        # Hub style: Azure blue
        style = f"shape=rectangle;rounded=0;whiteSpace=wrap;html=1;strokeColor={_config.color_hub_stroke};fontColor={_config.color_hub_font};fillColor={_config.color_hub_fill};align=left;strokeWidth=2;"
    elif is_stub:
        # Stub/Orphan style: Teal
        style = f"shape=rectangle;rounded=0;whiteSpace=wrap;html=1;strokeColor={_config.color_stub_stroke};fontColor={_config.color_stub_font};fillColor={_config.color_stub_fill};align=left;strokeWidth=2;"
    else:
        # Spoke style: Orange
        style = f"shape=rectangle;rounded=0;whiteSpace=wrap;html=1;strokeColor={_config.color_spoke_stroke};fontColor={_config.color_spoke_font};fillColor={_config.color_spoke_fill};align=left;strokeWidth=2;"

    # Create group object with metadata (empty label for group)
    group_id = cell_id
    group_obj = SubElement(root, "object")
    group_obj.set("id", str(group_id))
    group_obj.set("label", "")  # Groups have empty labels
    group_obj.set("subscription_name", vnet.subscription_name or "")
    group_obj.set("subscription_id", vnet.subscription_id)
    group_obj.set("resource_group_name", vnet.resource_group_name)
    group_obj.set("resource_id", vnet.name)  # Using name as resource identifier

    # Create group mxCell (container)
    group_cell = SubElement(group_obj, "mxCell")
    group_cell.set("style", "group")
    group_cell.set("vertex", "1")
    group_cell.set("connectable", "0")
    group_cell.set("parent", "1")

    # Calculate group height - will be updated if subnets are added
    group_height = height
    group_geometry = SubElement(group_cell, "mxGeometry")
    group_geometry.set("x", str(x))
    group_geometry.set("y", str(y))
    group_geometry.set("width", str(width))
    group_geometry.set("height", str(group_height))
    group_geometry.set("as", "geometry")

    # Store reference to group_geometry for later height update
    # (We'll update it after adding subnets if needed)

    # Create main VNet box as child of group
    main_id = cell_id + 1
    main_obj = SubElement(root, "object")
    main_obj.set("id", str(main_id))
    main_obj.set("label", "")  # Object label is empty, text goes in mxCell value
    main_obj.set("subscription_name", vnet.subscription_name or "")
    main_obj.set("subscription_id", vnet.subscription_id)
    main_obj.set("resource_group_name", vnet.resource_group_name)
    main_obj.set("resource_id", vnet.name)

    # Calculate VNet box height - ensure it's tall enough for label text
    # Label has 3 lines, so minimum height should accommodate that
    min_vnet_height = max(height, _config.vnet_min_height)

    # Create main VNet mxCell with value attribute for text content
    # The label will be positioned at top-left (x=0, y=0) with proper padding
    main_cell = SubElement(main_obj, "mxCell")
    main_cell.set("value", label)  # Text content goes in value attribute
    # Add vertical alignment to top and horizontal alignment to left
    label_spacing_top = _config.label_spacing_top
    label_spacing_left = _config.label_spacing_left
    style_with_align = style.replace("align=left;", f"align=left;verticalAlign=top;spacingTop={label_spacing_top};spacingLeft={label_spacing_left};")
    main_cell.set("style", style_with_align)
    main_cell.set("vertex", "1")
    main_cell.set("connectable", "1")  # Make main VNet box connectable for edges (edges connect to this, not subnets)
    main_cell.set("parent", str(group_id))

    main_geometry = SubElement(main_cell, "mxGeometry")
    main_geometry.set("x", "0")
    main_geometry.set("y", "0")
    main_geometry.set("width", str(width))
    # Start with min height, will expand if subnets are added
    main_geometry.set("height", str(min_vnet_height))
    main_geometry.set("as", "geometry")

    # Add VNet icon (top-right corner)
    icon_id = cell_id + 2
    icon_size = _config.icon_vnet_size
    icon_margin = _config.icon_margin_right
    icon_spacing = _config.icon_spacing
    icon_y = 3  # Top margin: 3px from top

    # Start from right edge and work left for icons
    current_icon_x = width - (icon_margin + icon_size)  # Right margin: icon_margin + icon_size

    vnet_icon = SubElement(root, "mxCell")
    vnet_icon.set("id", str(icon_id))
    vnet_icon.set("style", f"shape=image;html=1;image={_config.icon_vnet};")
    vnet_icon.set("vertex", "1")
    vnet_icon.set("parent", str(main_id))

    icon_geometry = SubElement(vnet_icon, "mxGeometry")
    icon_geometry.set("x", str(current_icon_x))
    icon_geometry.set("y", str(icon_y))
    icon_geometry.set("width", str(icon_size))
    icon_geometry.set("height", str(icon_size))
    icon_geometry.set("as", "geometry")

    current_cell_id = icon_id + 1

    # Add DDoS Protection icon (if DDoS protection is enabled, to the left of VNet icon)
    if vnet.enable_ddos_protection:
        current_icon_x -= (icon_size + icon_spacing)  # Move left
        ddos_icon_id = current_cell_id
        ddos_icon = SubElement(root, "mxCell")
        ddos_icon.set("id", str(ddos_icon_id))
        ddos_icon.set("style", f"shape=image;html=1;image={_config.icon_ddos};")
        ddos_icon.set("vertex", "1")
        ddos_icon.set("parent", str(main_id))

        ddos_icon_geometry = SubElement(ddos_icon, "mxGeometry")
        ddos_icon_geometry.set("x", str(current_icon_x))
        ddos_icon_geometry.set("y", str(icon_y))
        ddos_icon_geometry.set("width", str(icon_size))
        ddos_icon_geometry.set("height", str(icon_size))
        ddos_icon_geometry.set("as", "geometry")

        current_cell_id += 1  # Increment for DDoS icon

    # Add subnets inside VNet box (below the VNet label, inside the box)
    # Ensure subnets start below the label text area
    subnet_width = width - _config.subnet_width_offset  # Slightly narrower than VNet box

    for subnet_index, subnet in enumerate(vnet.subnets):
        subnet_y = _config.subnet_padding_top + (subnet_index * (_config.subnet_height + _config.subnet_spacing))

        # Create subnet box
        subnet_id = current_cell_id
        subnet_cell = SubElement(root, "mxCell")
        subnet_cell.set("id", str(subnet_id))
        subnet_cell.set("value", f"{subnet.name}<br>{subnet.address_prefix}")
        subnet_cell.set("style", f"shape=rectangle;rounded=0;whiteSpace=wrap;html=1;strokeColor={_config.color_subnet_stroke};fontColor={_config.color_subnet_font};fillColor={_config.color_subnet_fill};align=left;strokeWidth=1;")
        subnet_cell.set("vertex", "1")
        subnet_cell.set("connectable", "0")  # Subnets should NOT be connectable - edges connect to main VNet box perimeter
        subnet_cell.set("parent", str(main_id))

        subnet_geometry = SubElement(subnet_cell, "mxGeometry")
        subnet_geometry.set("x", str(_config.subnet_padding_left))  # Padding from left
        subnet_geometry.set("y", str(subnet_y))
        subnet_geometry.set("width", str(subnet_width))
        subnet_geometry.set("height", str(_config.subnet_height))
        subnet_geometry.set("as", "geometry")

        current_cell_id += 1  # Increment for subnet box

        # Add icons to subnet box (top-right corner)
        # Icons are positioned from right to left: Subnet (always), Route Table (if exists), NSG (if exists),
        # Firewall (if AzureFirewallSubnet), Bastion (if AzureBastionSubnet), VPN (if GatewaySubnet with VPN),
        # ExpressRoute (if GatewaySubnet with ER), NAT Gateway (if NAT Gateway exists on subnet),
        # Private Endpoint (if Private Endpoint exists on subnet)
        icon_size = _config.icon_subnet_size
        icon_height = _config.icon_subnet_height
        icon_spacing = _config.icon_spacing
        icon_y = subnet_y + 2  # Top margin: 2px from top

        # Start from right edge and work left
        current_icon_x = subnet_width - (icon_size + 2)  # Right margin: 2px margin + icon width

        # Add subnet icon (always present, rightmost)
        subnet_icon_id = current_cell_id
        subnet_icon = SubElement(root, "mxCell")
        subnet_icon.set("id", str(subnet_icon_id))
        subnet_icon.set("style", f"shape=image;html=1;image={_config.icon_subnet};")
        subnet_icon.set("vertex", "1")
        subnet_icon.set("parent", str(main_id))

        subnet_icon_geometry = SubElement(subnet_icon, "mxGeometry")
        subnet_icon_geometry.set("x", str(current_icon_x))
        subnet_icon_geometry.set("y", str(icon_y))
        subnet_icon_geometry.set("width", str(icon_size))
        subnet_icon_geometry.set("height", str(icon_height))
        subnet_icon_geometry.set("as", "geometry")

        current_cell_id += 1  # Increment for subnet icon

        # Add Route Table/UDR icon (if route table exists)
        if subnet.route_table_name:
            current_icon_x -= (icon_size + icon_spacing)  # Move left
            route_icon_id = current_cell_id
            route_icon = SubElement(root, "mxCell")
            route_icon.set("id", str(route_icon_id))
            route_icon.set("style", f"shape=image;html=1;image={_config.icon_route_table};")
            route_icon.set("vertex", "1")
            route_icon.set("parent", str(main_id))

            route_icon_geometry = SubElement(route_icon, "mxGeometry")
            route_icon_geometry.set("x", str(current_icon_x))
            route_icon_geometry.set("y", str(icon_y))
            route_icon_geometry.set("width", str(icon_size))
            route_icon_geometry.set("height", str(icon_height))
            route_icon_geometry.set("as", "geometry")

            current_cell_id += 1  # Increment for route table icon

        # Add NSG icon (if NSG exists)
        if subnet.network_security_group_name:
            current_icon_x -= (icon_size + icon_spacing)  # Move left
            nsg_icon_id = current_cell_id
            nsg_icon = SubElement(root, "mxCell")
            nsg_icon.set("id", str(nsg_icon_id))
            nsg_icon.set("style", f"shape=image;html=1;image={_config.icon_nsg};")
            nsg_icon.set("vertex", "1")
            nsg_icon.set("parent", str(main_id))

            nsg_icon_geometry = SubElement(nsg_icon, "mxGeometry")
            nsg_icon_geometry.set("x", str(current_icon_x))
            nsg_icon_geometry.set("y", str(icon_y))
            nsg_icon_geometry.set("width", str(icon_size))
            nsg_icon_geometry.set("height", str(icon_height))
            nsg_icon_geometry.set("as", "geometry")

            current_cell_id += 1  # Increment for NSG icon

        # Add Firewall icon (if AzureFirewallSubnet and firewall exists)
        if subnet.name == "AzureFirewallSubnet" and vnet.firewall == "Yes":
            current_icon_x -= (icon_size + icon_spacing)  # Move left
            fw_icon_id = current_cell_id
            fw_icon = SubElement(root, "mxCell")
            fw_icon.set("id", str(fw_icon_id))
            fw_icon.set("style", f"shape=image;html=1;image={_config.icon_firewall};")
            fw_icon.set("vertex", "1")
            fw_icon.set("parent", str(main_id))

            fw_icon_geometry = SubElement(fw_icon, "mxGeometry")
            fw_icon_geometry.set("x", str(current_icon_x))
            fw_icon_geometry.set("y", str(icon_y))
            fw_icon_geometry.set("width", str(icon_size))
            fw_icon_geometry.set("height", str(icon_height))
            fw_icon_geometry.set("as", "geometry")

            current_cell_id += 1  # Increment for firewall icon

        # Add Bastion icon (if AzureBastionSubnet)
        if subnet.name == "AzureBastionSubnet":
            current_icon_x -= (icon_size + icon_spacing)  # Move left
            bastion_icon_id = current_cell_id
            bastion_icon = SubElement(root, "mxCell")
            bastion_icon.set("id", str(bastion_icon_id))
            bastion_icon.set("style", f"shape=image;html=1;image={_config.icon_bastion};")
            bastion_icon.set("vertex", "1")
            bastion_icon.set("parent", str(main_id))

            bastion_icon_geometry = SubElement(bastion_icon, "mxGeometry")
            bastion_icon_geometry.set("x", str(current_icon_x))
            bastion_icon_geometry.set("y", str(icon_y))
            bastion_icon_geometry.set("width", str(icon_size))
            bastion_icon_geometry.set("height", str(icon_height))
            bastion_icon_geometry.set("as", "geometry")

            current_cell_id += 1  # Increment for bastion icon

        # Add VPN Gateway icon (if GatewaySubnet with VPN gateway)
        if subnet.name == "GatewaySubnet" and vnet.gateway_type == "Vpn":
            current_icon_x -= (icon_size + icon_spacing)  # Move left
            vpn_icon_id = current_cell_id
            vpn_icon = SubElement(root, "mxCell")
            vpn_icon.set("id", str(vpn_icon_id))
            vpn_icon.set("style", f"shape=image;html=1;image={_config.icon_vpn_gateway};")
            vpn_icon.set("vertex", "1")
            vpn_icon.set("parent", str(main_id))

            vpn_icon_geometry = SubElement(vpn_icon, "mxGeometry")
            vpn_icon_geometry.set("x", str(current_icon_x))
            vpn_icon_geometry.set("y", str(icon_y))
            vpn_icon_geometry.set("width", str(icon_size))
            vpn_icon_geometry.set("height", str(icon_height))
            vpn_icon_geometry.set("as", "geometry")

            current_cell_id += 1  # Increment for VPN icon

        # Add ExpressRoute icon (if GatewaySubnet with ExpressRoute gateway)
        if subnet.name == "GatewaySubnet" and vnet.gateway_type == "ExpressRoute":
            current_icon_x -= (icon_size + icon_spacing)  # Move left
            er_icon_id = current_cell_id
            er_icon = SubElement(root, "mxCell")
            er_icon.set("id", str(er_icon_id))
            er_icon.set("style", f"shape=image;html=1;image={_config.icon_expressroute};")
            er_icon.set("vertex", "1")
            er_icon.set("parent", str(main_id))

            er_icon_geometry = SubElement(er_icon, "mxGeometry")
            er_icon_geometry.set("x", str(current_icon_x))
            er_icon_geometry.set("y", str(icon_y))
            er_icon_geometry.set("width", str(icon_size))
            er_icon_geometry.set("height", str(icon_height))
            er_icon_geometry.set("as", "geometry")

            current_cell_id += 1  # Increment for ExpressRoute icon

        # Add NAT Gateway icon (if NAT Gateway exists on subnet)
        if subnet.nat_gateway_name:
            current_icon_x -= (icon_size + icon_spacing)  # Move left
            nat_icon_id = current_cell_id
            nat_icon = SubElement(root, "mxCell")
            nat_icon.set("id", str(nat_icon_id))
            nat_icon.set("style", f"shape=image;html=1;image={_config.icon_nat};")
            nat_icon.set("vertex", "1")
            nat_icon.set("parent", str(main_id))

            nat_icon_geometry = SubElement(nat_icon, "mxGeometry")
            nat_icon_geometry.set("x", str(current_icon_x))
            nat_icon_geometry.set("y", str(icon_y))
            nat_icon_geometry.set("width", str(icon_size))
            nat_icon_geometry.set("height", str(icon_height))
            nat_icon_geometry.set("as", "geometry")

            current_cell_id += 1  # Increment for NAT Gateway icon

        # Add Private Endpoint icon (if Private Endpoint exists on subnet)
        if subnet.private_endpoint_name:
            current_icon_x -= (icon_size + icon_spacing)  # Move left
            pe_icon_id = current_cell_id
            pe_icon = SubElement(root, "mxCell")
            pe_icon.set("id", str(pe_icon_id))
            pe_icon.set("style", f"shape=image;html=1;image={_config.icon_private_endpoint};")
            pe_icon.set("vertex", "1")
            pe_icon.set("parent", str(main_id))

            pe_icon_geometry = SubElement(pe_icon, "mxGeometry")
            pe_icon_geometry.set("x", str(current_icon_x))
            pe_icon_geometry.set("y", str(icon_y))
            pe_icon_geometry.set("width", str(icon_size))
            pe_icon_geometry.set("height", str(icon_height))
            pe_icon_geometry.set("as", "geometry")

            current_cell_id += 1  # Increment for Private Endpoint icon

    # Update group height to accommodate subnets (if any)
    if vnet.subnets:
        total_subnet_height = len(vnet.subnets) * (_config.subnet_height + _config.subnet_spacing) - _config.subnet_spacing
        new_group_height = _config.subnet_padding_top + total_subnet_height + _config.subnet_padding_bottom
        group_geometry.set("height", str(new_group_height))
        # Expand main VNet box to accommodate subnets, but label stays at top (y=0)
        main_geometry.set("height", str(new_group_height))

    return (group_id, main_id, current_cell_id)


def extract_resource_group_from_id(resource_id: str) -> str | None:
    """Extract resource group name from Azure resource ID URI using regex.

    Format: /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/virtualNetworks/{vnet}

    Args:
        resource_id: Azure resource ID URI

    Returns:
        Resource group name or None if not found
    """
    import re
    if not resource_id:
        return None

    # Pattern: /resourceGroups/{resource_group_name}/
    pattern = r'/resourceGroups/([^/]+)'
    match = re.search(pattern, resource_id)
    return match.group(1) if match else None


def create_external_vnet_group(
    root: Element,
    cell_id: int,
    vnet_name: str,
    peering_resource_id: str,
    x: float,
    y: float,
    width: float | None = None,
    height: float | None = None,
) -> tuple[int, int, int]:
    """Create an external VNet group (VNet that is peered but not in the topology).

    External VNets are styled differently to indicate they're not fully collected.

    Args:
        root: Root element to add the cell to
        cell_id: Starting cell ID
        vnet_name: Name of the external VNet
        peering_resource_id: Full resource ID of the external VNet
        x: X position
        y: Y position
        width: Shape width (defaults to config value)
        height: Shape height (defaults to config value)

    Returns:
        tuple: (group_id, main_id, final_cell_id) - IDs for connecting edges (use main_id), and final cell_id for next VNet
    """
    # Use config defaults if not provided
    if width is None:
        width = _config.vnet_width
    if height is None:
        height = _config.vnet_height_base
    """Create an external VNet group (VNet that is peered but not in the topology).

    External VNets are styled differently to indicate they're not fully collected.

    Args:
        root: Root element to add the cell to
        cell_id: Starting cell ID
        vnet_name: Name of the external VNet
        peering_resource_id: Full resource ID of the external VNet
        x: X position
        y: Y position
        width: Shape width
        height: Shape height

    Returns:
        tuple: (group_id, main_id, final_cell_id) - IDs for connecting edges (use main_id), and final cell_id for next VNet
    """
    from gettopology.models import extract_subscription_id_from_id

    # Extract subscription ID and resource group from resource ID
    subscription_id = extract_subscription_id_from_id(peering_resource_id) or "Unknown"
    resource_group = extract_resource_group_from_id(peering_resource_id) or "Unknown"

    # Build label for external VNet (minimal info since we don't have full details)
    label_parts = []
    # Combine subscription and resource group on first line to save space
    sub_line = f"Sub: {subscription_id[:8]}..."
    if resource_group and resource_group != "Unknown":
        sub_line += f" / RG: {resource_group}"
    label_parts.append(sub_line)
    label_parts.append(vnet_name)
    label_parts.append("(External - Cross Subscription Peering)")

    label = "<br>".join(label_parts)

    # External VNet style: Gray/dashed border to indicate it's not fully collected
    style = f"shape=rectangle;rounded=0;whiteSpace=wrap;html=1;strokeColor={_config.color_external_stroke};fontColor={_config.color_external_font};fillColor={_config.color_external_fill};align=left;strokeWidth=2;dashed=1;dashPattern=4 4;"

    # Create group object with metadata
    group_id = cell_id
    group_obj = SubElement(root, "object")
    group_obj.set("id", str(group_id))
    group_obj.set("label", "")
    group_obj.set("subscription_id", subscription_id)
    group_obj.set("resource_group_name", resource_group)
    group_obj.set("resource_id", peering_resource_id)
    group_obj.set("is_external", "true")

    # Create group mxCell
    group_cell = SubElement(group_obj, "mxCell")
    group_cell.set("style", "group")
    group_cell.set("vertex", "1")
    group_cell.set("connectable", "0")
    group_cell.set("parent", "1")

    min_vnet_height = max(height, _config.vnet_min_height)
    group_geometry = SubElement(group_cell, "mxGeometry")
    group_geometry.set("x", str(x))
    group_geometry.set("y", str(y))
    group_geometry.set("width", str(width))
    group_geometry.set("height", str(min_vnet_height))
    group_geometry.set("as", "geometry")

    # Create main VNet box
    main_id = cell_id + 1
    main_obj = SubElement(root, "object")
    main_obj.set("id", str(main_id))
    main_obj.set("label", "")
    main_obj.set("subscription_id", subscription_id)
    main_obj.set("resource_group_name", resource_group)
    main_obj.set("resource_id", peering_resource_id)
    main_obj.set("is_external", "true")

    main_cell = SubElement(main_obj, "mxCell")
    main_cell.set("value", label)
    label_spacing_top = _config.label_spacing_top
    label_spacing_left = _config.label_spacing_left
    style_with_align = style.replace("align=left;", f"align=left;verticalAlign=top;spacingTop={label_spacing_top};spacingLeft={label_spacing_left};")
    main_cell.set("style", style_with_align)
    main_cell.set("vertex", "1")
    main_cell.set("connectable", "1")  # Make external VNet box connectable for edges
    main_cell.set("parent", str(group_id))

    main_geometry = SubElement(main_cell, "mxGeometry")
    main_geometry.set("x", "0")
    main_geometry.set("y", "0")
    main_geometry.set("width", str(width))
    main_geometry.set("height", str(min_vnet_height))
    main_geometry.set("as", "geometry")

    # Add VNet icon
    icon_id = cell_id + 2
    icon_size = _config.icon_vnet_size
    icon_margin = _config.icon_margin_right
    icon_x = width - (icon_margin + icon_size)
    icon_y = 3

    vnet_icon = SubElement(root, "mxCell")
    vnet_icon.set("id", str(icon_id))
    vnet_icon.set("style", f"shape=image;html=1;image={_config.icon_vnet};")
    vnet_icon.set("vertex", "1")
    vnet_icon.set("parent", str(main_id))

    icon_geometry = SubElement(vnet_icon, "mxGeometry")
    icon_geometry.set("x", str(icon_x))
    icon_geometry.set("y", str(icon_y))
    icon_geometry.set("width", str(icon_size))
    icon_geometry.set("height", str(icon_size))
    icon_geometry.set("as", "geometry")

    # External VNets use: group (cell_id) + main (cell_id+1) + icon (cell_id+2)
    final_cell_id = cell_id + 3
    return (group_id, main_id, final_cell_id)

