"""Legend generation for diagram.

This module creates a legend box on the left side of the diagram showing:
- VNet types (Hub, Spoke, External)
- Connection types (Hub-to-Spoke, Spoke-to-Spoke, Hub-to-Hub, Cross-Tenant)
- Icons (Firewall, VPN Gateway, ExpressRoute, NSG, Route Table, etc.)
"""

from xml.etree.ElementTree import Element, SubElement

from gettopology.diagram.config import get_config

# Get global config instance
_config = get_config()


def create_legend(
    root: Element,
    cell_id_counter: int,
    legend_x: float,
    legend_y: float,
) -> tuple[int, float]:
    """Create a legend box on the left side of the diagram.

    Args:
        root: Root element to add legend to
        cell_id_counter: Starting cell ID counter
        legend_x: X position for legend (left edge)
        legend_y: Y position for legend (top edge)

    Returns:
        Tuple of (updated cell_id_counter, actual_legend_height)
    """
    legend_width = _config.legend_width
    legend_height = _config.legend_height
    legend_padding = _config.legend_padding
    legend_item_spacing = _config.legend_item_spacing
    legend_item_height = _config.legend_item_height

    # Create legend container group
    legend_group = SubElement(root, "mxCell")
    legend_group.set("id", str(cell_id_counter))
    legend_group.set("value", "Legend")
    legend_group.set("style", "swimlane;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#CCCCCC;strokeWidth=2;")
    legend_group.set("vertex", "1")
    legend_group.set("parent", "1")

    legend_geometry = SubElement(legend_group, "mxGeometry")
    legend_geometry.set("x", str(legend_x))
    legend_geometry.set("y", str(legend_y))
    legend_geometry.set("width", str(legend_width))
    legend_geometry.set("height", str(legend_height))
    legend_geometry.set("as", "geometry")

    cell_id_counter += 1

    # Calculate column widths for 3-column layout
    # Column 1: VNet Types, Column 2: Connection Types, Column 3: Icons (with 2 sub-columns)
    column_gap = _config.legend_column_gap
    available_width = legend_width - 2 * legend_padding - (2 * column_gap)  # Account for gaps between 3 columns
    column_width = available_width / 3

    # Column X positions
    col1_x = legend_x + legend_padding
    col2_x = col1_x + column_width + column_gap
    col3_x = col2_x + column_width + column_gap

    # Ensure content doesn't overflow: VNet boxes are configurable, labels start at configurable gap
    # Connection lines should be shorter to fit in column 2
    max_content_width = column_width - _config.legend_column_margin

    # Current Y position for legend items (start at top for all columns)
    current_y = legend_y + legend_padding

    # ========== COLUMN 1: VNet Types ==========
    col1_y = current_y
    section_title = SubElement(root, "mxCell")
    section_title.set("id", str(cell_id_counter))
    section_title.set("value", "VNet Types")
    section_title.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=1")
    section_title.set("vertex", "1")
    section_title.set("parent", "1")
    title_geom = SubElement(section_title, "mxGeometry")
    title_geom.set("x", str(col1_x))
    title_geom.set("y", str(col1_y))
    title_geom.set("width", str(column_width))
    title_geom.set("height", str(legend_item_height))
    title_geom.set("as", "geometry")
    cell_id_counter += 1
    col1_y += legend_item_height + legend_item_spacing

    # Hub (Blue Box)
    hub_box_x = col1_x
    hub_box_y = col1_y
    hub_box = SubElement(root, "mxCell")
    hub_box.set("id", str(cell_id_counter))
    hub_box.set("value", "")
    hub_box.set("style", f"rounded=0;whiteSpace=wrap;html=1;fillColor={_config.color_hub_fill};strokeColor={_config.color_hub_stroke};strokeWidth=2;")
    hub_box.set("vertex", "1")
    hub_box.set("parent", "1")
    hub_geom = SubElement(hub_box, "mxGeometry")
    hub_geom.set("x", str(hub_box_x))
    hub_geom.set("y", str(hub_box_y))
    hub_geom.set("width", str(_config.legend_vnet_box_width))
    hub_geom.set("height", str(_config.legend_vnet_box_height))
    hub_geom.set("as", "geometry")
    cell_id_counter += 1

    hub_label = SubElement(root, "mxCell")
    hub_label.set("id", str(cell_id_counter))
    hub_label.set("value", "Hub")
    hub_label.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;")
    hub_label.set("vertex", "1")
    hub_label.set("parent", "1")
    hub_label_geom = SubElement(hub_label, "mxGeometry")
    hub_label_geom.set("x", str(hub_box_x + _config.legend_vnet_box_to_label_gap))
    hub_label_geom.set("y", str(hub_box_y))
    hub_label_geom.set("width", str(max_content_width - _config.legend_vnet_box_to_label_gap))
    hub_label_geom.set("height", str(_config.legend_vnet_box_height))
    hub_label_geom.set("as", "geometry")
    cell_id_counter += 1
    col1_y += _config.legend_vnet_box_height + legend_item_spacing

    # Spoke (Orange Box)
    spoke_box_x = col1_x
    spoke_box_y = col1_y
    spoke_box = SubElement(root, "mxCell")
    spoke_box.set("id", str(cell_id_counter))
    spoke_box.set("value", "")
    spoke_box.set("style", f"rounded=0;whiteSpace=wrap;html=1;fillColor={_config.color_spoke_fill};strokeColor={_config.color_spoke_stroke};strokeWidth=2;")
    spoke_box.set("vertex", "1")
    spoke_box.set("parent", "1")
    spoke_geom = SubElement(spoke_box, "mxGeometry")
    spoke_geom.set("x", str(spoke_box_x))
    spoke_geom.set("y", str(spoke_box_y))
    spoke_geom.set("width", str(_config.legend_vnet_box_width))
    spoke_geom.set("height", str(_config.legend_vnet_box_height))
    spoke_geom.set("as", "geometry")
    cell_id_counter += 1

    spoke_label = SubElement(root, "mxCell")
    spoke_label.set("id", str(cell_id_counter))
    spoke_label.set("value", "Spoke")
    spoke_label.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;")
    spoke_label.set("vertex", "1")
    spoke_label.set("parent", "1")
    spoke_label_geom = SubElement(spoke_label, "mxGeometry")
    spoke_label_geom.set("x", str(spoke_box_x + _config.legend_vnet_box_to_label_gap))
    spoke_label_geom.set("y", str(spoke_box_y))
    spoke_label_geom.set("width", str(max_content_width - _config.legend_vnet_box_to_label_gap))
    spoke_label_geom.set("height", str(_config.legend_vnet_box_height))
    spoke_label_geom.set("as", "geometry")
    cell_id_counter += 1
    col1_y += _config.legend_vnet_box_height + legend_item_spacing

    # Stub/Orphan (Teal Box)
    stub_box_x = col1_x
    stub_box_y = col1_y
    stub_box = SubElement(root, "mxCell")
    stub_box.set("id", str(cell_id_counter))
    stub_box.set("value", "")
    stub_box.set("style", f"rounded=0;whiteSpace=wrap;html=1;fillColor={_config.color_stub_fill};strokeColor={_config.color_stub_stroke};strokeWidth=2;")
    stub_box.set("vertex", "1")
    stub_box.set("parent", "1")
    stub_geom = SubElement(stub_box, "mxGeometry")
    stub_geom.set("x", str(stub_box_x))
    stub_geom.set("y", str(stub_box_y))
    stub_geom.set("width", str(_config.legend_vnet_box_width))
    stub_geom.set("height", str(_config.legend_vnet_box_height))
    stub_geom.set("as", "geometry")
    cell_id_counter += 1

    stub_label = SubElement(root, "mxCell")
    stub_label.set("id", str(cell_id_counter))
    stub_label.set("value", "Stub/Orphan")
    stub_label.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;")
    stub_label.set("vertex", "1")
    stub_label.set("parent", "1")
    stub_label_geom = SubElement(stub_label, "mxGeometry")
    stub_label_geom.set("x", str(stub_box_x + _config.legend_vnet_box_to_label_gap))
    stub_label_geom.set("y", str(stub_box_y))
    stub_label_geom.set("width", str(max_content_width - _config.legend_vnet_box_to_label_gap))
    stub_label_geom.set("height", str(_config.legend_vnet_box_height))
    stub_label_geom.set("as", "geometry")
    cell_id_counter += 1
    col1_y += _config.legend_vnet_box_height + legend_item_spacing

    # External/Cross Tenant (Gray dashed box)
    external_box_x = col1_x
    external_box_y = col1_y
    external_box = SubElement(root, "mxCell")
    external_box.set("id", str(cell_id_counter))
    external_box.set("value", "")
    external_box.set("style", f"rounded=0;whiteSpace=wrap;html=1;fillColor={_config.color_external_fill};strokeColor={_config.color_external_stroke};strokeWidth=2;dashed=1;dashPattern=8 8;")
    external_box.set("vertex", "1")
    external_box.set("parent", "1")
    external_geom = SubElement(external_box, "mxGeometry")
    external_geom.set("x", str(external_box_x))
    external_geom.set("y", str(external_box_y))
    external_geom.set("width", str(_config.legend_vnet_box_width))
    external_geom.set("height", str(_config.legend_vnet_box_height))
    external_geom.set("as", "geometry")
    cell_id_counter += 1

    external_label = SubElement(root, "mxCell")
    external_label.set("id", str(cell_id_counter))
    external_label.set("value", "Cross Tenant Peer")
    external_label.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;")
    external_label.set("vertex", "1")
    external_label.set("parent", "1")
    external_label_geom = SubElement(external_label, "mxGeometry")
    external_label_geom.set("x", str(external_box_x + _config.legend_vnet_box_to_label_gap))
    external_label_geom.set("y", str(external_box_y))
    external_label_geom.set("width", str(max_content_width - _config.legend_vnet_box_to_label_gap))
    external_label_geom.set("height", str(_config.legend_vnet_box_height))
    external_label_geom.set("as", "geometry")
    cell_id_counter += 1

    # ========== COLUMN 2: Connection Types ==========
    col2_y = current_y
    section_title = SubElement(root, "mxCell")
    section_title.set("id", str(cell_id_counter))
    section_title.set("value", "Connection Types")
    section_title.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=1")
    section_title.set("vertex", "1")
    section_title.set("parent", "1")
    title_geom = SubElement(section_title, "mxGeometry")
    title_geom.set("x", str(col2_x))
    title_geom.set("y", str(col2_y))
    title_geom.set("width", str(column_width))
    title_geom.set("height", str(legend_item_height))
    title_geom.set("as", "geometry")
    cell_id_counter += 1
    col2_y += legend_item_height + legend_item_spacing

    # Create sample connection lines for legend
    # Need to create small invisible boxes as endpoints for edges
    # Make lines shorter to fit within column 2 width
    line_length = min(_config.legend_connection_line_length, max_content_width - _config.legend_connection_line_to_label_gap - 5)
    line_start_x = col2_x
    line_end_x = col2_x + line_length
    line_y = col2_y + (_config.legend_vnet_box_height / 2)  # Middle of item height

    # Helper function to create a connection line with invisible endpoints
    def create_legend_line(start_x, end_x, y_pos, style, line_id):
        source_id = line_id
        # Create invisible source box (completely transparent)
        source_box = SubElement(root, "mxCell")
        source_box.set("id", str(source_id))
        source_box.set("value", "")
        source_box.set("style", "points=[];outlineConnect=0;fillColor=none;strokeColor=none;opacity=0;")
        source_box.set("vertex", "1")
        source_box.set("parent", "1")
        source_geom = SubElement(source_box, "mxGeometry")
        source_geom.set("x", str(start_x))
        source_geom.set("y", str(y_pos - 1))
        source_geom.set("width", "1")
        source_geom.set("height", "1")
        source_geom.set("as", "geometry")
        line_id += 1

        target_id = line_id
        # Create invisible target box (completely transparent)
        target_box = SubElement(root, "mxCell")
        target_box.set("id", str(target_id))
        target_box.set("value", "")
        target_box.set("style", "points=[];outlineConnect=0;fillColor=none;strokeColor=none;opacity=0;")
        target_box.set("vertex", "1")
        target_box.set("parent", "1")
        target_geom = SubElement(target_box, "mxGeometry")
        target_geom.set("x", str(end_x))
        target_geom.set("y", str(y_pos - 1))
        target_geom.set("width", "1")
        target_geom.set("height", "1")
        target_geom.set("as", "geometry")
        line_id += 1

        # Create edge connecting the boxes
        edge = SubElement(root, "mxCell")
        edge.set("id", str(line_id))
        edge.set("value", "")
        edge.set("style", style)
        edge.set("edge", "1")
        edge.set("parent", "1")
        edge.set("source", str(source_id))  # Source box ID
        edge.set("target", str(target_id))  # Target box ID
        edge_geom = SubElement(edge, "mxGeometry")
        edge_geom.set("relative", "1")
        edge_geom.set("as", "geometry")
        line_id += 1

        return line_id

    # Maroon dashed line - Spoke to Spoke
    cell_id_counter = create_legend_line(
        line_start_x, line_end_x, line_y,
        f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor={_config.edge_color_hubless_spoke};strokeWidth=2;dashed=1;dashPattern=8 8;startArrow=block;endArrow=block;",
        cell_id_counter
    )

    spoke_to_spoke_label = SubElement(root, "mxCell")
    spoke_to_spoke_label.set("id", str(cell_id_counter))
    spoke_to_spoke_label.set("value", "Spoke to Spoke")
    spoke_to_spoke_label.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;")
    spoke_to_spoke_label.set("vertex", "1")
    spoke_to_spoke_label.set("parent", "1")
    spoke_to_spoke_label_geom = SubElement(spoke_to_spoke_label, "mxGeometry")
    spoke_to_spoke_label_geom.set("x", str(line_end_x + _config.legend_connection_line_to_label_gap))
    spoke_to_spoke_label_geom.set("y", str(col2_y))
    spoke_to_spoke_label_geom.set("width", str(max_content_width - (line_end_x - col2_x) - _config.legend_connection_line_to_label_gap))
    spoke_to_spoke_label_geom.set("height", str(_config.legend_vnet_box_height))
    spoke_to_spoke_label_geom.set("as", "geometry")
    cell_id_counter += 1
    col2_y += _config.legend_vnet_box_height + legend_item_spacing

    # Blue line - Hub to Spoke
    line_y = col2_y + (_config.legend_vnet_box_height / 2)
    cell_id_counter = create_legend_line(
        line_start_x, line_end_x, line_y,
        f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor={_config.color_hub_to_spoke};strokeWidth=2;startArrow=block;endArrow=block;",
        cell_id_counter
    )

    hub_to_spoke_label = SubElement(root, "mxCell")
    hub_to_spoke_label.set("id", str(cell_id_counter))
    hub_to_spoke_label.set("value", "Hub to Spoke")
    hub_to_spoke_label.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;")
    hub_to_spoke_label.set("vertex", "1")
    hub_to_spoke_label.set("parent", "1")
    hub_to_spoke_label_geom = SubElement(hub_to_spoke_label, "mxGeometry")
    hub_to_spoke_label_geom.set("x", str(line_end_x + _config.legend_connection_line_to_label_gap))
    hub_to_spoke_label_geom.set("y", str(col2_y))
    hub_to_spoke_label_geom.set("width", str(max_content_width - (line_end_x - col2_x) - _config.legend_connection_line_to_label_gap))
    hub_to_spoke_label_geom.set("height", str(_config.legend_vnet_box_height))
    hub_to_spoke_label_geom.set("as", "geometry")
    cell_id_counter += 1
    col2_y += _config.legend_vnet_box_height + legend_item_spacing

    # Green line - Hub to Hub
    line_y = col2_y + (_config.legend_vnet_box_height / 2)
    cell_id_counter = create_legend_line(
        line_start_x, line_end_x, line_y,
        f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor={_config.color_hub_to_hub};strokeWidth=2;startArrow=block;endArrow=block;",
        cell_id_counter
    )

    hub_to_hub_label = SubElement(root, "mxCell")
    hub_to_hub_label.set("id", str(cell_id_counter))
    hub_to_hub_label.set("value", "Hub to Hub")
    hub_to_hub_label.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;")
    hub_to_hub_label.set("vertex", "1")
    hub_to_hub_label.set("parent", "1")
    hub_to_hub_label_geom = SubElement(hub_to_hub_label, "mxGeometry")
    hub_to_hub_label_geom.set("x", str(line_end_x + _config.legend_connection_line_to_label_gap))
    hub_to_hub_label_geom.set("y", str(col2_y))
    hub_to_hub_label_geom.set("width", str(max_content_width - (line_end_x - col2_x) - _config.legend_connection_line_to_label_gap))
    hub_to_hub_label_geom.set("height", str(_config.legend_vnet_box_height))
    hub_to_hub_label_geom.set("as", "geometry")
    cell_id_counter += 1
    col2_y += _config.legend_vnet_box_height + legend_item_spacing

    # Gray line - Cross Tenant
    line_y = col2_y + (_config.legend_vnet_box_height / 2)
    cell_id_counter = create_legend_line(
        line_start_x, line_end_x, line_y,
        f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor={_config.edge_color_cross_tenant};strokeWidth=2;startArrow=block;endArrow=block;",
        cell_id_counter
    )

    cross_tenant_label = SubElement(root, "mxCell")
    cross_tenant_label.set("id", str(cell_id_counter))
    cross_tenant_label.set("value", "Cross Tenant")
    cross_tenant_label.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;")
    cross_tenant_label.set("vertex", "1")
    cross_tenant_label.set("parent", "1")
    cross_tenant_label_geom = SubElement(cross_tenant_label, "mxGeometry")
    cross_tenant_label_geom.set("x", str(line_end_x + _config.legend_connection_line_to_label_gap))
    cross_tenant_label_geom.set("y", str(col2_y))
    cross_tenant_label_geom.set("width", str(max_content_width - (line_end_x - col2_x) - _config.legend_connection_line_to_label_gap))
    cross_tenant_label_geom.set("height", str(_config.legend_vnet_box_height))
    cross_tenant_label_geom.set("as", "geometry")
    cell_id_counter += 1
    col2_y += _config.legend_vnet_box_height + legend_item_spacing

    # Green solid line - Hybrid Connected
    line_y = col2_y + (_config.legend_vnet_box_height / 2)
    cell_id_counter = create_legend_line(
        line_start_x, line_end_x, line_y,
        "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#28A745;strokeWidth=3;startArrow=block;endArrow=block;",
        cell_id_counter
    )

    hybrid_connected_label = SubElement(root, "mxCell")
    hybrid_connected_label.set("id", str(cell_id_counter))
    hybrid_connected_label.set("value", "Hybrid Connected")
    hybrid_connected_label.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;")
    hybrid_connected_label.set("vertex", "1")
    hybrid_connected_label.set("parent", "1")
    hybrid_connected_label_geom = SubElement(hybrid_connected_label, "mxGeometry")
    hybrid_connected_label_geom.set("x", str(line_end_x + _config.legend_connection_line_to_label_gap))
    hybrid_connected_label_geom.set("y", str(col2_y))
    hybrid_connected_label_geom.set("width", str(max_content_width - (line_end_x - col2_x) - _config.legend_connection_line_to_label_gap))
    hybrid_connected_label_geom.set("height", str(_config.legend_vnet_box_height))
    hybrid_connected_label_geom.set("as", "geometry")
    cell_id_counter += 1
    col2_y += _config.legend_vnet_box_height + legend_item_spacing

    # Red dotted line - Hybrid Not Connected
    line_y = col2_y + (_config.legend_vnet_box_height / 2)
    cell_id_counter = create_legend_line(
        line_start_x, line_end_x, line_y,
        "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#FF6B6B;strokeWidth=1;dashed=1;dashPattern=8 8;startArrow=block;endArrow=block;",
        cell_id_counter
    )

    hybrid_not_connected_label = SubElement(root, "mxCell")
    hybrid_not_connected_label.set("id", str(cell_id_counter))
    hybrid_not_connected_label.set("value", "Hybrid Not Connected")
    hybrid_not_connected_label.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;")
    hybrid_not_connected_label.set("vertex", "1")
    hybrid_not_connected_label.set("parent", "1")
    hybrid_not_connected_label_geom = SubElement(hybrid_not_connected_label, "mxGeometry")
    hybrid_not_connected_label_geom.set("x", str(line_end_x + _config.legend_connection_line_to_label_gap))
    hybrid_not_connected_label_geom.set("y", str(col2_y))
    hybrid_not_connected_label_geom.set("width", str(max_content_width - (line_end_x - col2_x) - _config.legend_connection_line_to_label_gap))
    hybrid_not_connected_label_geom.set("height", str(_config.legend_vnet_box_height))
    hybrid_not_connected_label_geom.set("as", "geometry")
    cell_id_counter += 1

    # ========== COLUMN 3: Icons ==========
    col3_y = current_y
    section_title = SubElement(root, "mxCell")
    section_title.set("id", str(cell_id_counter))
    section_title.set("value", "Icons")
    section_title.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontStyle=1")
    section_title.set("vertex", "1")
    section_title.set("parent", "1")
    title_geom = SubElement(section_title, "mxGeometry")
    title_geom.set("x", str(col3_x))
    title_geom.set("y", str(col3_y))
    title_geom.set("width", str(column_width))
    title_geom.set("height", str(legend_item_height))
    title_geom.set("as", "geometry")
    cell_id_counter += 1
    col3_y += legend_item_height + legend_item_spacing

    # Add icon legend items in 2 columns to save vertical space
    icons = [
        ("Firewall", _config.icon_firewall),
        ("Bastion", _config.icon_bastion),
        ("VPN Gateway", _config.icon_vpn_gateway),
        ("ExpressRoute", _config.icon_expressroute),
        ("NSG", _config.icon_nsg),
        ("Route Table", _config.icon_route_table),
        ("NAT", _config.icon_nat),
        ("Private Endpoint", _config.icon_private_endpoint),
        ("DDoS Protection", _config.icon_ddos),
    ]

    icon_size = _config.legend_icon_size
    icons_per_column = _config.legend_icons_per_sub_column
    icon_sub_column_gap = _config.legend_icon_sub_column_gap
    icon_sub_column_width = (max_content_width - icon_sub_column_gap) / 2  # Divide column 3 width between 2 sub-columns

    # Track Y position for each sub-column within column 3
    icon_sub_col1_x = col3_x
    icon_sub_col2_x = col3_x + icon_sub_column_width + icon_sub_column_gap
    icon_column_y_positions = [col3_y, col3_y]  # Start both sub-columns at same Y

    for index, (icon_name, icon_path) in enumerate(icons):
        # Determine which column (0 or 1)
        column = 0 if index < icons_per_column else 1
        index if column == 0 else index - icons_per_column

        # Calculate X position based on sub-column within column 3
        icon_x = icon_sub_col1_x if column == 0 else icon_sub_col2_x
        icon_y = icon_column_y_positions[column]

        # Icon image
        icon_cell = SubElement(root, "mxCell")
        icon_cell.set("id", str(cell_id_counter))
        icon_cell.set("value", "")
        icon_cell.set("style", f"shape=image;verticalLabelPosition=bottom;verticalAlign=top;imageAspect=0;aspect=fixed;image={icon_path};")
        icon_cell.set("vertex", "1")
        icon_cell.set("parent", "1")
        icon_geom = SubElement(icon_cell, "mxGeometry")
        icon_geom.set("x", str(icon_x))
        icon_geom.set("y", str(icon_y))
        icon_geom.set("width", str(icon_size))
        icon_geom.set("height", str(icon_size))
        icon_geom.set("as", "geometry")
        cell_id_counter += 1

        # Icon label
        icon_label = SubElement(root, "mxCell")
        icon_label.set("id", str(cell_id_counter))
        icon_label.set("value", icon_name)
        icon_label.set("style", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;")
        icon_label.set("vertex", "1")
        icon_label.set("parent", "1")
        icon_label_geom = SubElement(icon_label, "mxGeometry")
        icon_label_geom.set("x", str(icon_x + icon_size + _config.legend_icon_to_label_gap))
        icon_label_geom.set("y", str(icon_y))
        icon_label_geom.set("width", str(icon_sub_column_width - icon_size - _config.legend_icon_to_label_gap))
        icon_label_geom.set("height", str(icon_size))
        icon_label_geom.set("as", "geometry")
        cell_id_counter += 1

        # Update Y position for this sub-column
        icon_column_y_positions[column] += icon_size + legend_item_spacing

    # Update current_y to the maximum Y position across all columns
    current_y = max(col1_y, col2_y, max(icon_column_y_positions))

    # Calculate actual height needed and update legend box if needed
    actual_height = current_y - legend_y + legend_padding
    if actual_height > legend_height:
        # Update legend box height to fit content
        legend_geometry.set("height", str(actual_height))
    else:
        # Use configured height if content fits
        actual_height = legend_height

    return cell_id_counter, actual_height

