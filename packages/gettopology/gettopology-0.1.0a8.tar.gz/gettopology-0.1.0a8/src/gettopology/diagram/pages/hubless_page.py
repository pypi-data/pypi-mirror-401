"""Hubless spoke page generation for diagram.

Creates a separate page for hubless spoke groups (VNets that peer with each other but not with hubs).
"""

from xml.etree.ElementTree import Element, SubElement

from gettopology.diagram.config import get_config
from gettopology.diagram.elements.vnet_elements import calculate_vnet_height, create_vnet_group
from gettopology.diagram.layout import Zone, calculate_spoke_positions
from gettopology.diagram.legend import create_legend
from gettopology.models import VirtualNetworkModel

# Get global config instance
_config = get_config()

# Constants
CANVAS_PADDING = _config.canvas_padding
VNET_WIDTH = _config.vnet_width
VNET_SPACING_Y = _config.vnet_spacing_y
SPACING_BELOW_HUB = _config.spacing_below_hub


def create_hubless_page(
    mxfile: Element,
    hubless_groups: list[list[VirtualNetworkModel]],
    primary_subscription_id: str | None,
    hubless_spoke_names: set[str],
    create_peering_edge_func,
    cell_id_start: int,
) -> None:
    """Create hubless spoke page.

    Args:
        mxfile: Root mxfile element
        hubless_groups: List of hubless groups (each group is a list of VNets)
        primary_subscription_id: Primary subscription ID for styling
        hubless_spoke_names: Set of hubless spoke names (for edge styling)
        create_peering_edge_func: Function to create peering edges
        cell_id_start: Starting cell ID for this page
    """
    if not hubless_groups:
        return

    # Create diagram for hubless spokes
    hubless_diagram = SubElement(mxfile, "diagram")
    hubless_diagram.set("id", "topology-hubless")
    hubless_diagram.set("name", "Hubless Spokes")

    hubless_mxGraphModel = SubElement(hubless_diagram, "mxGraphModel")
    hubless_mxGraphModel.set("dx", str(_config.drawio_page_dx))
    hubless_mxGraphModel.set("dy", str(_config.drawio_page_dy))
    hubless_mxGraphModel.set("grid", "1")
    hubless_mxGraphModel.set("gridSize", str(_config.drawio_grid_size))
    hubless_mxGraphModel.set("guides", "1")
    hubless_mxGraphModel.set("tooltips", "1")
    hubless_mxGraphModel.set("connect", "1")
    hubless_mxGraphModel.set("arrows", "1")
    hubless_mxGraphModel.set("fold", "1")
    hubless_mxGraphModel.set("page", "1")
    hubless_mxGraphModel.set("pageWidth", str(_config.page_width))
    hubless_mxGraphModel.set("pageHeight", str(_config.page_height))
    hubless_mxGraphModel.set("math", "0")
    hubless_mxGraphModel.set("shadow", "0")

    hubless_root = SubElement(hubless_mxGraphModel, "root")

    # Add mxCell for root
    hubless_root_cell = SubElement(hubless_root, "mxCell")
    hubless_root_cell.set("id", "0")

    hubless_root_cell_layer = SubElement(hubless_root, "mxCell")
    hubless_root_cell_layer.set("id", "1")
    hubless_root_cell_layer.set("parent", "0")

    # Create legend for hubless page
    hubless_cell_id_counter = cell_id_start
    hubless_legend_x = _config.legend_x
    hubless_legend_y = CANVAS_PADDING
    hubless_cell_id_counter, actual_legend_height = create_legend(hubless_root, hubless_cell_id_counter, hubless_legend_x, hubless_legend_y)

    # Create mapping for hubless page
    hubless_vnet_name_to_main_id: dict[str, int] = {}
    hubless_hubless_spoke_positions: dict[str, tuple[float, float, float]] = {}
    hubless_all_vnet_positions: dict[str, tuple[float, float, float]] = {}
    hubless_hub_name_to_position: dict[str, tuple[float, float, float]] = {}
    hubless_edges_to_create: list = []

    # Create hubless group mappings (needed for edge connection logic)
    hubless_group_map: dict[str, int] = {}  # vnet_name -> group_index
    hubless_centers: dict[int, str] = {}  # group_index -> center_name

    # Calculate positions for hubless spokes on this page
    # Use same centering logic as hub/spoke layout
    # Use actual legend height to ensure no overlap
    legend_padding = _config.legend_padding
    legend_bottom_y = CANVAS_PADDING + actual_legend_height + legend_padding
    hubless_start_y = legend_bottom_y + _config.legend_to_diagram_spacing

    # Calculate legend area (same as orphan page)
    legend_area_right = _config.legend_x + _config.legend_width + _config.legend_padding

    # Calculate available width after legend
    available_width = _config.page_width - legend_area_right - CANVAS_PADDING

    # Center the hubless group in available space (same as hub/spoke centers hub)
    # Calculate canvas center in available space (after legend)
    canvas_center_x = legend_area_right + (available_width / 2)

    # Center the central spoke at canvas center (same as hub positioning)
    # center_x is the LEFT EDGE of the central spoke
    center_x = canvas_center_x - (VNET_WIDTH / 2)

    current_y: float = hubless_start_y
    for group_index, hubless_group in enumerate(hubless_groups):
        # Find center VNet: select the VNet with the most peerings WITHIN this hubless group
        # This ensures the most-connected VNet in the group becomes the center for cleaner layout
        hubless_group_names = {vnet.name for vnet in hubless_group}

        def count_internal_peerings(vnet: VirtualNetworkModel) -> int:
            """Count peerings that are within this hubless group."""
            return sum(1 for peer_name in vnet.peering_names if peer_name in hubless_group_names)

        # Select VNet with most internal peerings (within the group)
        # If tie, use total peering_count as tie-breaker, then alphabetical by name for consistency
        center_vnet = max(
            hubless_group,
            key=lambda v: (count_internal_peerings(v), v.peering_count, v.name)
        )
        center_name = center_vnet.name
        remaining_spokes = [v for v in hubless_group if v.name != center_name]

        # Store hubless group mappings (needed for edge connection logic)
        hubless_centers[group_index] = center_name
        for vnet in hubless_group:
            hubless_group_map[vnet.name] = group_index

        # Calculate center position (aligned from left after legend)
        center_height = calculate_vnet_height(center_vnet)
        center_y = current_y

        # Create center VNet (treat it like a hub)
        group_id, center_main_id, hubless_cell_id_counter = create_vnet_group(
            hubless_root, hubless_cell_id_counter, center_vnet, center_x, center_y,
            is_hub=False, primary_subscription_id=primary_subscription_id
        )
        hubless_vnet_name_to_main_id[center_name] = center_main_id
        hubless_hubless_spoke_positions[center_name] = (center_x, center_y, center_height)
        hubless_all_vnet_positions[center_name] = (center_x, center_y, center_height)
        hubless_hub_name_to_position[center_name] = (center_x, center_y, center_height)

        # Calculate center VNet's center X (center_x is the left edge)
        center_vnet_center_x = center_x + (VNET_WIDTH / 2)

        # Reuse the same hub/spoke layout logic by creating a temporary Zone
        # Treat central spoke as the "hub" and remaining spokes as regular spokes
        # IMPORTANT: calculate_spoke_positions expects zone_x to be the HUB CENTER (not left edge)
        # It calculates: left spoke center = hub_x - vnet_spacing_x, right spoke center = hub_x + vnet_spacing_x
        temp_zone = Zone(
            hub=center_vnet,  # Central spoke acts as hub
            hub_index=0,  # Not used by calculate_spoke_positions, but required by Zone
            spokes=remaining_spokes,
            zone_x=center_vnet_center_x,  # HUB CENTER X (required by calculate_spoke_positions)
            zone_y=center_y,  # Hub Y position (top edge)
            zone_bottom=0.0  # Not used by calculate_spoke_positions, but required by Zone
        )

        # Use the same calculate_spoke_positions function as hub/spoke
        left_spoke_positions = calculate_spoke_positions(temp_zone, is_left=True)
        right_spoke_positions = calculate_spoke_positions(temp_zone, is_left=False)

        # Create left spokes (same logic as hub/spoke)
        # x_position from calculate_spoke_positions is the SPOKE CENTER, convert to left edge for create_vnet_group
        for spoke, spoke_center_x, y_position in left_spoke_positions:
            spoke_height = calculate_vnet_height(spoke)
            spoke_x = spoke_center_x - (VNET_WIDTH / 2)  # Convert center to left edge
            group_id, spoke_main_id, hubless_cell_id_counter = create_vnet_group(
                hubless_root, hubless_cell_id_counter, spoke, spoke_x, y_position,
                is_hub=False, primary_subscription_id=primary_subscription_id
            )
            hubless_vnet_name_to_main_id[spoke.name] = spoke_main_id
            hubless_hubless_spoke_positions[spoke.name] = (spoke_x, y_position, spoke_height)
            hubless_all_vnet_positions[spoke.name] = (spoke_x, y_position, spoke_height)

            # Store edge from center to spoke (same as hub/spoke)
            # Pass center_x (left edge) and spoke_x (left edge) - waypoint calculation expects left edges
            peering_index = spoke.peering_names.index(center_name) if center_name in spoke.peering_names else -1
            is_local = spoke.peering_local_flags[peering_index] if peering_index >= 0 and peering_index < len(spoke.peering_local_flags) else True
            hubless_edges_to_create.append((
                center_main_id, spoke_main_id, is_local, False, False,
                center_x, spoke_x, center_y, y_position, center_height, spoke_height,
                center_name, spoke.name, False
            ))

        # Create right spokes (same logic as hub/spoke)
        # x_position from calculate_spoke_positions is the SPOKE CENTER, convert to left edge for create_vnet_group
        for spoke, spoke_center_x, y_position in right_spoke_positions:
            spoke_height = calculate_vnet_height(spoke)
            spoke_x = spoke_center_x - (VNET_WIDTH / 2)  # Convert center to left edge
            group_id, spoke_main_id, hubless_cell_id_counter = create_vnet_group(
                hubless_root, hubless_cell_id_counter, spoke, spoke_x, y_position,
                is_hub=False, primary_subscription_id=primary_subscription_id
            )
            hubless_vnet_name_to_main_id[spoke.name] = spoke_main_id
            hubless_hubless_spoke_positions[spoke.name] = (spoke_x, y_position, spoke_height)
            hubless_all_vnet_positions[spoke.name] = (spoke_x, y_position, spoke_height)

            # Store edge from center to spoke (same as hub/spoke)
            # Pass center_x (left edge) and spoke_x (left edge) - waypoint calculation expects left edges
            peering_index = spoke.peering_names.index(center_name) if center_name in spoke.peering_names else -1
            is_local = spoke.peering_local_flags[peering_index] if peering_index >= 0 and peering_index < len(spoke.peering_local_flags) else True
            hubless_edges_to_create.append((
                center_main_id, spoke_main_id, is_local, False, False,
                center_x, spoke_x, center_y, y_position, center_height, spoke_height,
                center_name, spoke.name, False
            ))

        # Store edges between spokes within this group
        # Extract spoke objects from position tuples
        all_spoke_positions = left_spoke_positions + right_spoke_positions
        spoke_positions_dict: dict[str, tuple[float, float, float]] = {}
        for spoke, _, _ in all_spoke_positions:
            spoke_positions_dict[spoke.name] = hubless_hubless_spoke_positions[spoke.name]

        # Track created edges to avoid duplicates (bidirectional)
        hubless_created_edges: set[tuple[str, str]] = set()

        for spoke, _, _ in all_spoke_positions:
            spoke_main_id = hubless_vnet_name_to_main_id[spoke.name]
            spoke_x, spoke_y, spoke_height = spoke_positions_dict[spoke.name]
            for peer_name in spoke.peering_names:
                # Skip if peer is the center (already handled above)
                if peer_name == center_name:
                    continue
                # Only create edge if peer is in this hubless group and on this page
                if peer_name in hubless_vnet_name_to_main_id and peer_name in spoke_positions_dict:
                    # Check if edge already created (bidirectional check)
                    edge_key: tuple[str, str] = tuple(sorted([spoke.name, peer_name]))  # type: ignore[arg-type]
                    if edge_key in hubless_created_edges:
                        continue
                    hubless_created_edges.add(edge_key)

                    peer_index = spoke.peering_names.index(peer_name)
                    is_local = spoke.peering_local_flags[peer_index] if peer_index < len(spoke.peering_local_flags) else True
                    peer_main_id = hubless_vnet_name_to_main_id[peer_name]
                    peer_x, peer_y, peer_height = spoke_positions_dict[peer_name]
                    hubless_edges_to_create.append((
                        spoke_main_id, peer_main_id, is_local, False, False,
                        spoke_x, peer_x, spoke_y, peer_y, spoke_height, peer_height,
                        spoke.name, peer_name, False
                    ))

        # Update current_y for next group
        # Calculate total height of this group from top of center to bottom of last spoke
        # Calculate spoke_start_y (where spokes begin below center)
        spoke_start_y = center_y + center_height + SPACING_BELOW_HUB
        max_spoke_height = 0.0
        if left_spoke_positions:
            last_left_spoke, _, last_left_y = left_spoke_positions[-1]
            last_left_height = calculate_vnet_height(last_left_spoke)
            max_spoke_height = max(max_spoke_height, last_left_y + last_left_height - spoke_start_y)
        if right_spoke_positions:
            last_right_spoke, _, last_right_y = right_spoke_positions[-1]
            last_right_height = calculate_vnet_height(last_right_spoke)
            max_spoke_height = max(max_spoke_height, last_right_y + last_right_height - spoke_start_y)

        # Total group height = center height + spacing below center + max spoke height
        # This ensures we account for the full vertical extent of the group
        total_group_height = center_height + SPACING_BELOW_HUB + max_spoke_height
        current_y += total_group_height + VNET_SPACING_Y * 2

    # Create edges for hubless page
    for edge_data in hubless_edges_to_create:
        source_id, target_id, is_local, source_is_hub, target_is_hub, source_x, target_x, source_y, target_y, source_height, target_height, source_name, target_name, is_cross_tenant = edge_data
        create_peering_edge_func(
            hubless_root, hubless_cell_id_counter, source_id, target_id, is_local,
            source_is_hub, target_is_hub, source_x, target_x, source_y, target_y,
            source_height, target_height, source_name, target_name,
            hubless_spoke_names, None, hubless_group_map, hubless_centers,
            is_cross_tenant, hubless_hub_name_to_position, hubless_all_vnet_positions
        )
        hubless_cell_id_counter += 1

