"""Hybrid connectivity page generation for diagram.

Creates a horizontal layout showing on-premises networks (left) connected to Azure VNets (right)
via VPN or ExpressRoute connections.
"""

from typing import Any

from xml.etree.ElementTree import Element, SubElement

from gettopology.diagram.config import get_config
from gettopology.diagram.elements.vnet_elements import calculate_vnet_height, create_vnet_group
from gettopology.diagram.legend import create_legend
from gettopology.models import ConnectionModel, LocalNetworkGatewayModel, TopologyModel, VirtualNetworkModel

# Get global config instance
_config = get_config()

# Constants
CANVAS_PADDING = _config.canvas_padding
VNET_WIDTH = _config.vnet_width
# LEGEND_HEIGHT is now returned from create_legend() - use actual_legend_height instead
LEGEND_PADDING = _config.legend_padding

# Hybrid connectivity layout constants
ONPREM_BOX_WIDTH = _config.hybrid_onprem_box_width
ONPREM_BOX_HEIGHT = _config.hybrid_onprem_box_height
ROUTER_ICON_SIZE = _config.hybrid_router_icon_size
CONTENT_START_Y = _config.hybrid_content_start_y
CONTENT_SPACING = _config.hybrid_content_spacing
CONTENT_BOTTOM_PADDING = _config.hybrid_content_bottom_padding
INFO_BOX_WIDTH = _config.hybrid_info_box_width
INFO_BOX_LINE_HEIGHT = _config.hybrid_info_box_line_height
INFO_BOX_PADDING = _config.hybrid_info_box_padding
INFO_BOX_OFFSET_Y = _config.hybrid_info_box_offset_y
VNET_SPACING_X = _config.vnet_spacing_x
SPACING_BELOW_HUB = _config.spacing_below_hub
SPACING_BETWEEN_SPOKES = _config.spacing_between_spokes
CONTENT_SPACING = _config.hybrid_content_spacing


def create_onprem_box(
    root: Element,
    cell_id: int,
    lng: LocalNetworkGatewayModel,
    connection: ConnectionModel,
    x: float,
    y: float,
    ) -> tuple[int, int]:
    """Create on-premises network box with router icon and details.

    Args:
        root: Root element to add the cell to
        cell_id: Starting cell ID
        lng: Local Network Gateway model
        connection: Connection model
        x: X position
        y: Y position

    Returns:
        tuple: (box_id, final_cell_id)
    """
    # Create group for on-premises box
    # Use spoke colors (orange) for on-premises/remote sites to match legend
    group_obj = SubElement(root, "object")
    group_obj.set("id", str(cell_id))
    group_cell = SubElement(group_obj, "mxCell")
    group_cell.set("value", "On-Premises Network")
    group_cell.set("style", f"swimlane;whiteSpace=wrap;html=1;fillColor={_config.color_spoke_fill};strokeColor={_config.color_spoke_stroke};strokeWidth=2;fontColor={_config.color_spoke_font};")
    group_cell.set("vertex", "1")
    group_cell.set("parent", "1")

    group_geometry = SubElement(group_cell, "mxGeometry")
    group_geometry.set("x", str(x))
    group_geometry.set("y", str(y))
    group_geometry.set("width", str(ONPREM_BOX_WIDTH))
    group_geometry.set("height", str(ONPREM_BOX_HEIGHT))
    group_geometry.set("as", "geometry")

    current_cell_id = cell_id + 1

    # Title bar height for swimlane is typically ~30px, so start content below it
    CONTENT_START_Y = 35  # Padding from top to avoid overlapping with title

    # Add router icon (top-left, below title)
    router_icon = SubElement(root, "mxCell")
    router_icon.set("id", str(current_cell_id))
    # Choose icon based on connection type
    if connection.connection_type == "ExpressRoute":
        icon_path = _config.icon_router_expressroute
    else:
        icon_path = _config.icon_router_vpn
    router_icon.set("style", f"shape=image;html=1;image={icon_path};")
    router_icon.set("vertex", "1")
    router_icon.set("parent", str(cell_id))

    router_geometry = SubElement(router_icon, "mxGeometry")
    router_geometry.set("x", "10")  # Relative to parent, not absolute
    router_geometry.set("y", str(CONTENT_START_Y))
    router_geometry.set("width", str(ROUTER_ICON_SIZE))
    router_geometry.set("height", str(ROUTER_ICON_SIZE))
    router_geometry.set("as", "geometry")

    current_cell_id += 1

    # Add connection name label
    name_label = SubElement(root, "mxCell")
    name_label.set("id", str(current_cell_id))
    name_label.set("value", f"<b>{connection.name}</b>")
    name_label.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=12;fontStyle=1")
    name_label.set("vertex", "1")
    name_label.set("parent", str(cell_id))

    name_label_height = 25
    name_geometry = SubElement(name_label, "mxGeometry")
    name_geometry.set("x", "50")  # Relative to parent, not absolute
    name_geometry.set("y", str(CONTENT_START_Y))
    name_geometry.set("width", str(ONPREM_BOX_WIDTH - 60))
    name_geometry.set("height", str(name_label_height))
    name_geometry.set("as", "geometry")

    current_cell_id += 1

    # Track current Y position for cumulative positioning
    current_y = CONTENT_START_Y + name_label_height + CONTENT_SPACING

    # Add gateway IP or FQDN
    gateway_info = []
    if lng.fqdn:
        gateway_info.append(f"FQDN: {lng.fqdn}")
    if lng.gateway_ip_address:
        gateway_info.append(f"IP: {lng.gateway_ip_address}")
    
    label_height = 20  # Standard height for all subsequent labels
    if gateway_info:
        gateway_label = SubElement(root, "mxCell")
        gateway_label.set("id", str(current_cell_id))
        gateway_label.set("value", gateway_info[0])
        gateway_label.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;")
        gateway_label.set("vertex", "1")
        gateway_label.set("parent", str(cell_id))

        gateway_geometry = SubElement(gateway_label, "mxGeometry")
        gateway_geometry.set("x", "10")  # Relative to parent, not absolute
        gateway_geometry.set("y", str(current_y))
        gateway_geometry.set("width", str(ONPREM_BOX_WIDTH - 20))
        gateway_geometry.set("height", str(label_height))
        gateway_geometry.set("as", "geometry")

        current_y += label_height + CONTENT_SPACING
        current_cell_id += 1

    # Add address prefixes
    if lng.address_prefixes:
        prefixes_text = ", ".join(lng.address_prefixes[:3])  # Show first 3
        if len(lng.address_prefixes) > 3:
            prefixes_text += f" (+{len(lng.address_prefixes) - 3} more)"
        prefixes_label = SubElement(root, "mxCell")
        prefixes_label.set("id", str(current_cell_id))
        prefixes_label.set("value", f"Prefixes: {prefixes_text}")
        prefixes_label.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=9;")
        prefixes_label.set("vertex", "1")
        prefixes_label.set("parent", str(cell_id))

        prefixes_geometry = SubElement(prefixes_label, "mxGeometry")
        prefixes_geometry.set("x", "10")  # Relative to parent, not absolute
        prefixes_geometry.set("y", str(current_y))
        prefixes_geometry.set("width", str(ONPREM_BOX_WIDTH - 20))
        prefixes_geometry.set("height", str(label_height))
        prefixes_geometry.set("as", "geometry")

        current_y += label_height + CONTENT_SPACING
        current_cell_id += 1

    # Add connection properties (IKE/PSK for VPN)
    if connection.connection_type == "IPsec":
        props = []
        if connection.connection_protocol:
            props.append(f"IKE: {connection.connection_protocol}")
        if connection.authentication_type:
            props.append(f"Auth: {connection.authentication_type}")
        if props:
            props_label = SubElement(root, "mxCell")
            props_label.set("id", str(current_cell_id))
            props_label.set("value", " | ".join(props))
            props_label.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=9;")
            props_label.set("vertex", "1")
            props_label.set("parent", str(cell_id))

            props_geometry = SubElement(props_label, "mxGeometry")
            props_geometry.set("x", "10")  # Relative to parent, not absolute
            props_geometry.set("y", str(current_y))
            props_geometry.set("width", str(ONPREM_BOX_WIDTH - 20))
            props_geometry.set("height", str(label_height))
            props_geometry.set("as", "geometry")

            current_y += label_height
            current_cell_id += 1

    # Calculate required box height: last element bottom + bottom padding
    # current_y is relative to parent, so we need to calculate from start
    content_height = current_y - CONTENT_START_Y + CONTENT_BOTTOM_PADDING
    # Update box height if needed (ensure minimum height)
    final_height = max(ONPREM_BOX_HEIGHT, content_height)
    group_geometry.set("height", str(final_height))

    return cell_id, current_cell_id


def create_connection_info_box(
    root: Element,
    cell_id: int,
    connection: ConnectionModel,
    x: float,
    y: float,
) -> int:
    """Create info box above connection line showing DPD timeout and IPsec policies.
    
    Args:
        root: Root element
        cell_id: Starting cell ID
        connection: Connection model
        x: X position (center of connection)
        y: Y position (above connection line)
        
    Returns:
        Final cell ID
    """
    # Build info text
    info_lines = []
    
    # Add DPD timeout if available
    if connection.dpd_timeout_seconds is not None:
        info_lines.append(f"DPD: {connection.dpd_timeout_seconds}s")
    
    # Add IPsec policies for IPsec connections
    if connection.connection_type == "IPsec" and connection.ipsec_policies:
        for policy in connection.ipsec_policies:
            policy_parts = []
            
            # Encryption
            if policy.get('ipsecEncryption'):
                policy_parts.append(f"Enc: {policy['ipsecEncryption']}")
            
            # Integrity
            if policy.get('ipsecIntegrity'):
                policy_parts.append(f"Int: {policy['ipsecIntegrity']}")
            
            # DH Group
            if policy.get('dhGroup'):
                policy_parts.append(f"DH: {policy['dhGroup']}")
            
            # PFS Group
            if policy.get('pfsGroup'):
                policy_parts.append(f"PFS: {policy['pfsGroup']}")
            
            # SA Lifetime
            if policy.get('saLifeTimeSeconds'):
                policy_parts.append(f"SA: {policy['saLifeTimeSeconds']}s")
            
            if policy_parts:
                info_lines.append(" | ".join(policy_parts))
    
    if not info_lines:
        return cell_id  # No info to display
    
    # Create info box
    info_text = "<br>".join(info_lines)
    info_box_height = len(info_lines) * INFO_BOX_LINE_HEIGHT + INFO_BOX_PADDING
    
    # Center the box horizontally
    info_box_x = x - (INFO_BOX_WIDTH / 2)
    
    info_box = SubElement(root, "mxCell")
    info_box.set("id", str(cell_id))
    info_box.set("value", info_text)
    info_box.set("style", "text;html=1;strokeColor=#666666;fillColor=#F5F5F5;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=1;fontSize=9;")
    info_box.set("vertex", "1")
    info_box.set("parent", "1")
    
    info_geometry = SubElement(info_box, "mxGeometry")
    info_geometry.set("x", str(info_box_x))
    info_geometry.set("y", str(y))
    info_geometry.set("width", str(INFO_BOX_WIDTH))
    info_geometry.set("height", str(info_box_height))
    info_geometry.set("as", "geometry")
    
    return cell_id + 1


def create_hybrid_connection_edge(
    root: Element,
    cell_id: int,
    source_id: int,
    target_id: int,
    connection: ConnectionModel,
    source_x: float,
    target_x: float,
    source_y: float,
    target_y: float,
    source_height: float,
    target_height: float,
) -> int:
    """Create edge between on-premises and Azure VNet using hub-to-spoke connection logic.

    Args:
        root: Root element
        cell_id: Starting cell ID
        source_id: On-premises box ID
        target_id: VNet main ID
        connection: Connection model
        source_x, source_y: On-premises position (center coordinates)
        target_x, target_y: VNet position (center coordinates)
        source_height, target_height: Heights

    Returns:
        Final cell ID
    """
    from gettopology.diagram.elements.edge_elements import build_edge_style
    from gettopology.diagram.connections.hub_to_spoke import create_hub_to_spoke_connection

    # Determine edge style based on connection status (not type)
    # Status determines color and pattern, type is shown as label
    # Only show green if explicitly "Connected", otherwise show red (for NotConnected, Disconnected, Unknown, None)
    is_connected = connection.connection_status == "Connected"
    
    if is_connected:
        # Connected: Green solid line (regardless of VPN or ExpressRoute)
        edge_color = "#28A745"  # Green for connected
        edge_style = build_edge_style(edge_color, "solid", "orthogonalEdgeStyle", _config)  # Solid, non-dotted
        edge_style = edge_style.replace("strokeWidth=2", "strokeWidth=3")  # Thicker for connected
    else:
        # NotConnected/Disconnected/Unknown/None: Red dashed line (regardless of VPN or ExpressRoute)
        edge_color = "#FF6B6B"  # Red for disconnected/unknown
        edge_style = build_edge_style(edge_color, "dashed", "orthogonalEdgeStyle", _config)  # Dashed
        edge_style = edge_style.replace("strokeWidth=2", "strokeWidth=1")  # Thinner for disconnected

    # Create edge with label
    # Note: For hub-to-spoke logic, VNet is the "hub" (source) and on-prem is the "spoke" (target)
    # So we swap source and target IDs to match the connection logic
    edge = SubElement(root, "mxCell")
    edge.set("id", str(cell_id))
    # Add connection type as edge label (IPsec or ExpressRoute)
    edge_label = connection.connection_type if connection.connection_type else ""
    edge.set("value", edge_label)
    edge.set("style", edge_style)
    edge.set("edge", "1")
    edge.set("parent", "1")
    # Swap: VNet (target_id) becomes source (hub), on-prem (source_id) becomes target (spoke)
    edge.set("source", str(target_id))  # VNet is the hub
    edge.set("target", str(source_id))  # On-prem is the spoke

    edge_geometry = SubElement(edge, "mxGeometry")
    edge_geometry.set("relative", "1")
    edge_geometry.set("as", "geometry")
    
    # Use hub-to-spoke connection logic for proper alignment
    # Convert center coordinates to left-edge coordinates for hub_to_spoke function
    # VNet (target) is the "hub", on-prem (source) is the "spoke"
    # The function expects left edges, so we need to convert
    ONPREM_BOX_WIDTH = _config.hybrid_onprem_box_width
    VNET_WIDTH = _config.vnet_width
    
    # Convert center coordinates to left edges
    onprem_left_x = source_x - (ONPREM_BOX_WIDTH / 2)
    onprem_top_y = source_y - (source_height / 2)
    vnet_left_x = target_x - (VNET_WIDTH / 2)
    vnet_top_y = target_y - (target_height / 2)
    
    # Use hub-to-spoke connection logic (VNet is hub, on-prem is spoke)
    # This ensures proper connection points: VNet bottom center → on-prem side middle
    create_hub_to_spoke_connection(
        root,
        edge_geometry,
        vnet_left_x,  # Hub (VNet) left edge
        onprem_left_x,  # Spoke (on-prem) left edge
        vnet_top_y,  # Hub (VNet) top edge
        onprem_top_y,  # Spoke (on-prem) top edge
        target_height,  # Hub (VNet) height
        source_height,  # Spoke (on-prem) height
    )

    return cell_id + 1


def create_hybrid_page(
    mxfile: Element,
    topology: TopologyModel,
    hybrid_data: dict[str, Any],
    primary_subscription_id: str | None,
    cell_id_start: int,
) -> None:
    """Create hybrid connectivity page.

    Args:
        mxfile: Root mxfile element
        topology: TopologyModel containing VNets
        hybrid_data: Hybrid connectivity data from collect_hybrid_connectivity
        primary_subscription_id: Primary subscription ID for styling
        cell_id_start: Starting cell ID for this page
    """
    connections = hybrid_data['connections']
    local_network_gateways = hybrid_data['local_network_gateways']
    vnet_to_connections = hybrid_data['vnet_to_connections']
    connection_to_local_gateway = hybrid_data['connection_to_local_gateway']

    # Filter to only VPN and ExpressRoute connections (exclude VNet-to-VNet)
    hybrid_connections = [
        conn for conn in connections
        if conn.connection_type in ["IPsec", "ExpressRoute"] and conn.local_network_gateway_id
    ]

    if not hybrid_connections:
        return  # No hybrid connections to show

    # Create diagram for hybrid connectivity
    hybrid_diagram = SubElement(mxfile, "diagram")
    hybrid_diagram.set("id", "topology-hybrid")
    hybrid_diagram.set("name", "Hybrid Connectivity")

    hybrid_mxGraphModel = SubElement(hybrid_diagram, "mxGraphModel")
    hybrid_mxGraphModel.set("dx", str(_config.drawio_page_dx))
    hybrid_mxGraphModel.set("dy", str(_config.drawio_page_dy))
    hybrid_mxGraphModel.set("grid", "1")
    hybrid_mxGraphModel.set("gridSize", str(_config.drawio_grid_size))
    hybrid_mxGraphModel.set("guides", "1")
    hybrid_mxGraphModel.set("tooltips", "1")
    hybrid_mxGraphModel.set("connect", "1")
    hybrid_mxGraphModel.set("arrows", "1")
    hybrid_mxGraphModel.set("fold", "1")
    hybrid_mxGraphModel.set("page", "1")
    hybrid_mxGraphModel.set("pageWidth", str(_config.page_width))
    hybrid_mxGraphModel.set("pageHeight", str(_config.page_height))
    hybrid_mxGraphModel.set("math", "0")
    hybrid_mxGraphModel.set("shadow", "0")

    hybrid_root = SubElement(hybrid_mxGraphModel, "root")

    # Add mxCell for root
    hybrid_root_cell = SubElement(hybrid_root, "mxCell")
    hybrid_root_cell.set("id", "0")

    hybrid_root_cell_layer = SubElement(hybrid_root, "mxCell")
    hybrid_root_cell_layer.set("id", "1")
    hybrid_root_cell_layer.set("parent", "0")

    # Create legend
    hybrid_cell_id_counter = cell_id_start
    legend_x = _config.legend_x
    legend_y = CANVAS_PADDING
    hybrid_cell_id_counter, actual_legend_height = create_legend(hybrid_root, hybrid_cell_id_counter, legend_x, legend_y)

    # Group connections by VNet and gateway (each gateway gets its own group)
    # Structure: [(vnet_name, gateway_id, gateway_type, [connections]), ...]
    gateway_groups: list[tuple[str, str, str, list[ConnectionModel]]] = []

    for vnet_name, vnet_conns in vnet_to_connections.items():
        # Filter to only hybrid connections (VPN/ExpressRoute with LNG)
        hybrid_conns = [
            c for c in vnet_conns
            if c.connection_type in ["IPsec", "ExpressRoute"] and c.local_network_gateway_id
        ]
        
        if not hybrid_conns:
            continue

        # Group by gateway (connections with same virtual_network_gateway_id)
        gateway_to_conns: dict[str, list[ConnectionModel]] = {}
        for conn in hybrid_conns:
            if conn.virtual_network_gateway_id:
                gw_id = conn.virtual_network_gateway_id
                if gw_id not in gateway_to_conns:
                    gateway_to_conns[gw_id] = []
                gateway_to_conns[gw_id].append(conn)

        # Create groups for each gateway (each gateway is a separate group)
        for gw_id, conns in gateway_to_conns.items():
            gateway_type = "ExpressRoute" if conns[0].connection_type == "ExpressRoute" else "VPN"
            gateway_groups.append((vnet_name, gw_id, gateway_type, conns))

    if not gateway_groups:
        return  # No valid hybrid connections

    # Sort groups: by VNet name, then by gateway type (ExpressRoute first), then by gateway ID
    gateway_groups.sort(key=lambda x: (x[0], 0 if x[2] == "ExpressRoute" else 1, x[1]))

    # Calculate starting Y position (below legend)
    # Use actual legend height to ensure no overlap
    start_y = legend_y + actual_legend_height + LEGEND_PADDING + 50
    current_y = start_y

    # Calculate legend area
    legend_area_right = _config.legend_x + _config.legend_width + _config.legend_padding
    
    # Calculate available width after legend
    available_width = _config.page_width - legend_area_right - CANVAS_PADDING
    
    # Center the gateway groups in available space
    canvas_center_x = legend_area_right + (available_width / 2)

    # Process each gateway group (each gateway is separate)
    for vnet_name, gateway_id, gateway_type, connections_list in gateway_groups:
        # Find VNet
        vnet = next((v for v in topology.virtual_networks if v.name == vnet_name), None)
        if not vnet:
            continue

        # Calculate VNet (hub) position - center horizontally
        vnet_height = calculate_vnet_height(vnet)
        vnet_x = canvas_center_x - (VNET_WIDTH / 2)  # Left edge of VNet
        vnet_y = current_y
        vnet_center_x = canvas_center_x  # Center X for spoke calculations

        # Create VNet box at center (acts as hub - has VPN/ExpressRoute gateway)
        # Use is_hub=True to get blue hub colors to match legend
        vnet_group_id, vnet_main_id, hybrid_cell_id_counter = create_vnet_group(
            hybrid_root,
            hybrid_cell_id_counter,
            vnet,
            vnet_x,
            vnet_y,
            is_hub=True,  # VPN/ExpressRoute gateways make this a hub - use blue colors
            primary_subscription_id=primary_subscription_id,
        )

        # Calculate on-premises box positions (like spokes, alternating left and right)
        # Split connections into left and right groups
        left_connections = []
        right_connections = []
        for idx, conn in enumerate(connections_list):
            if idx % 2 == 0:
                left_connections.append(conn)
            else:
                right_connections.append(conn)

        # Calculate starting Y position for on-prem boxes (below VNet)
        onprem_start_y = vnet_y + vnet_height + SPACING_BELOW_HUB

        # Create left on-premises boxes
        for idx, connection in enumerate(left_connections):
            lng = connection_to_local_gateway.get(connection.resource_id)
            if not lng:
                continue

            # Calculate position: left side, stacked vertically
            onprem_x = vnet_center_x - VNET_SPACING_X - (ONPREM_BOX_WIDTH / 2)  # Center the box
            onprem_y = onprem_start_y + (idx * (ONPREM_BOX_HEIGHT + SPACING_BETWEEN_SPOKES))

            # Create on-premises box
            onprem_box_id, hybrid_cell_id_counter = create_onprem_box(
                hybrid_root,
                hybrid_cell_id_counter,
                lng,
                connection,
                onprem_x,
                onprem_y,
            )

            # Create connection edge (from on-prem to VNet)
            hybrid_cell_id_counter = create_hybrid_connection_edge(
                hybrid_root,
                hybrid_cell_id_counter,
                onprem_box_id,
                vnet_main_id,
                connection,
                onprem_x + (ONPREM_BOX_WIDTH / 2),  # Center of on-prem box
                vnet_center_x,  # Center of VNet
                onprem_y + (ONPREM_BOX_HEIGHT / 2),  # Center Y of on-prem box
                vnet_y + (vnet_height / 2),  # Center Y of VNet
                ONPREM_BOX_HEIGHT,
                vnet_height,
            )

        # Create right on-premises boxes
        for idx, connection in enumerate(right_connections):
            lng = connection_to_local_gateway.get(connection.resource_id)
            if not lng:
                continue

            # Calculate position: right side, stacked vertically
            onprem_x = vnet_center_x + VNET_SPACING_X - (ONPREM_BOX_WIDTH / 2)  # Center the box
            onprem_y = onprem_start_y + (idx * (ONPREM_BOX_HEIGHT + SPACING_BETWEEN_SPOKES))

            # Create on-premises box
            onprem_box_id, hybrid_cell_id_counter = create_onprem_box(
                hybrid_root,
                hybrid_cell_id_counter,
                lng,
                connection,
                onprem_x,
                onprem_y,
            )

            # Create connection edge (from on-prem to VNet)
            hybrid_cell_id_counter = create_hybrid_connection_edge(
                hybrid_root,
                hybrid_cell_id_counter,
                onprem_box_id,
                vnet_main_id,
                connection,
                onprem_x + (ONPREM_BOX_WIDTH / 2),  # Center of on-prem box
                vnet_center_x,  # Center of VNet
                onprem_y + (ONPREM_BOX_HEIGHT / 2),  # Center Y of on-prem box
                vnet_y + (vnet_height / 2),  # Center Y of VNet
                ONPREM_BOX_HEIGHT,
                vnet_height,
            )

        # Calculate bottom of this group
        max_onprem_count = max(len(left_connections), len(right_connections))
        if max_onprem_count > 0:
            group_bottom = onprem_start_y + (max_onprem_count * (ONPREM_BOX_HEIGHT + SPACING_BETWEEN_SPOKES)) - SPACING_BETWEEN_SPOKES
        else:
            group_bottom = vnet_y + vnet_height
        
        # Move to next group (add spacing)
        current_y = group_bottom + _config.hybrid_vertical_spacing

    # Update page height if needed
    required_height = current_y + CANVAS_PADDING
    if required_height > _config.page_height:
        hybrid_mxGraphModel.set("pageHeight", str(int(required_height)))



