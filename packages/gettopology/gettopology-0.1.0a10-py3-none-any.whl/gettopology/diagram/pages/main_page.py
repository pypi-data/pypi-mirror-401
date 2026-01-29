"""Main page generation for diagram.

Creates the main page with hubs, spokes, and external VNets.
"""

from xml.etree.ElementTree import Element

from gettopology.diagram.config import get_config
from gettopology.diagram.elements.vnet_elements import (
    calculate_vnet_height,
    create_external_vnet_group,
    create_vnet_group,
)
from gettopology.diagram.layout import (
    Zone,
    calculate_external_zone_positions,
    calculate_spoke_positions,
)
from gettopology.diagram.legend import create_legend
from gettopology.models import TopologyModel

# Get global config instance
_config = get_config()

# Constants
CANVAS_PADDING = _config.canvas_padding
VNET_WIDTH = _config.vnet_width
VNET_MIN_HEIGHT = _config.vnet_min_height
EXTERNAL_SPACING_Y = _config.external_spacing_y
SPACING_BELOW_HUB = _config.spacing_below_hub
SPACING_BETWEEN_SPOKES = _config.spacing_between_spokes


def create_main_page(
    root: Element,
    topology: TopologyModel,
    zones: list[Zone],
    primary_subscription_id: str | None,
    hubless_spoke_names: set[str],
    stubs: list,
    hub_names: set[str],
    vnet_name_to_tenant_id: dict[str, str],
    hubless_group_map: dict[str, int],
    hubless_centers: dict[int, str],
    cell_id_counter: int,
    legend_x: float,
    create_peering_edge_func,
) -> tuple[
    int,  # cell_id_counter
    dict[str, int],  # vnet_name_to_main_id
    dict[str, tuple[float, float, float]],  # hub_name_to_position
    dict[str, tuple[float, float, float]],  # regular_spoke_positions
    dict[str, tuple[float, float, float]],  # hubless_spoke_positions
    dict[str, tuple[float, float, float]],  # all_vnet_positions
    list,  # edges_to_create
]:
    """Create main page with hubs, spokes, and external VNets.

    Returns updated state dictionaries and cell_id_counter.
    """
    # Initialize dictionaries
    vnet_name_to_main_id: dict[str, int] = {}
    hub_name_to_position: dict[str, tuple[float, float, float]] = {}
    regular_spoke_positions: dict[str, tuple[float, float, float]] = {}
    hubless_spoke_positions: dict[str, tuple[float, float, float]] = {}
    all_vnet_positions: dict[str, tuple[float, float, float]] = {}
    edges_to_create: list = []
    created_edges: set[tuple[int, int]] = set()

    def _add_edge_if_not_exists(
        source_id: int,
        target_id: int,
        is_local: bool,
        source_name: str,
        target_name: str,
        source_x: float | None = None,
        target_x: float | None = None,
        source_y: float | None = None,
        target_y: float | None = None,
        source_height: float | None = None,
        target_height: float | None = None,
    ) -> None:
        """Helper to add edge to list only if it doesn't already exist."""
        sorted_ids = sorted([source_id, target_id])
        edge_key: tuple[int, int] = (sorted_ids[0], sorted_ids[1])
        if edge_key not in created_edges:
            is_hubless_center = False
            if hubless_centers:
                is_hubless_center = source_name in hubless_centers.values()
            source_is_hub = (source_name in hub_names and source_name not in hubless_spoke_names) or is_hubless_center
            target_is_hub = target_name in hub_names and target_name not in hubless_spoke_names
            source_tenant_id = vnet_name_to_tenant_id.get(source_name)
            target_tenant_id = vnet_name_to_tenant_id.get(target_name)
            is_cross_tenant = (source_tenant_id is not None and target_tenant_id is not None and source_tenant_id != target_tenant_id) or (target_name not in vnet_name_to_tenant_id)
            edges_to_create.append((source_id, target_id, is_local, source_is_hub, target_is_hub, source_x, target_x, source_y, target_y, source_height, target_height, source_name, target_name, is_cross_tenant))
            created_edges.add(edge_key)

    # PHASE 1: Create all VNets first (for proper z-ordering, edges will be created after)
    # 1. Layout hub-spoke groups using calculated zones
    zone_bottoms: list[float] = []
    for zone in zones:
        hub_x = zone.zone_x
        hub_y_adjusted = zone.zone_y
        hub_height = calculate_vnet_height(zone.hub)

        # Draw hub
        group_id, hub_main_id, cell_id_counter = create_vnet_group(
            root, cell_id_counter, zone.hub, hub_x, hub_y_adjusted,
            is_hub=True, primary_subscription_id=primary_subscription_id
        )
        vnet_name_to_main_id[zone.hub.name] = hub_main_id
        hub_name_to_position[zone.hub.name] = (hub_x, hub_y_adjusted, hub_height)
        all_vnet_positions[zone.hub.name] = (hub_x, hub_y_adjusted, hub_height)

        # Calculate spoke positions using layout module
        left_spoke_positions = calculate_spoke_positions(zone, is_left=True)
        right_spoke_positions = calculate_spoke_positions(zone, is_left=False)

        # Create left spokes
        for spoke, x_position, y_position in left_spoke_positions:
            spoke_height = calculate_vnet_height(spoke)
            group_id, spoke_main_id, cell_id_counter = create_vnet_group(
                root, cell_id_counter, spoke, x_position, y_position,
                is_hub=False, primary_subscription_id=primary_subscription_id,
                hub_subscription_id=zone.hub.subscription_id
            )
            vnet_name_to_main_id[spoke.name] = spoke_main_id
            regular_spoke_positions[spoke.name] = (x_position, y_position, spoke_height)
            all_vnet_positions[spoke.name] = (x_position, y_position, spoke_height)

            # Store edge information
            peering_index = spoke.peering_names.index(zone.hub.name) if zone.hub.name in spoke.peering_names else -1
            is_local = spoke.peering_local_flags[peering_index] if peering_index >= 0 and peering_index < len(spoke.peering_local_flags) else True
            _add_edge_if_not_exists(
                hub_main_id, spoke_main_id, is_local, zone.hub.name, spoke.name,
                hub_x, x_position, hub_y_adjusted, y_position, hub_height, spoke_height
            )

        # Create right spokes
        for spoke, x_position, y_position in right_spoke_positions:
            spoke_height = calculate_vnet_height(spoke)
            group_id, spoke_main_id, cell_id_counter = create_vnet_group(
                root, cell_id_counter, spoke, x_position, y_position,
                is_hub=False, primary_subscription_id=primary_subscription_id,
                hub_subscription_id=zone.hub.subscription_id
            )
            vnet_name_to_main_id[spoke.name] = spoke_main_id
            regular_spoke_positions[spoke.name] = (x_position, y_position, spoke_height)
            all_vnet_positions[spoke.name] = (x_position, y_position, spoke_height)

            # Store edge information
            peering_index = spoke.peering_names.index(zone.hub.name) if zone.hub.name in spoke.peering_names else -1
            is_local = spoke.peering_local_flags[peering_index] if peering_index >= 0 and peering_index < len(spoke.peering_local_flags) else True
            _add_edge_if_not_exists(
                hub_main_id, spoke_main_id, is_local, zone.hub.name, spoke.name,
                hub_x, x_position, hub_y_adjusted, y_position, hub_height, spoke_height
            )

        # Track zone bottom
        max_spoke_count = max(len(left_spoke_positions), len(right_spoke_positions))
        if max_spoke_count > 0:
            total_spoke_height = sum(calculate_vnet_height(spoke) for spoke, _, _ in (left_spoke_positions + right_spoke_positions))
            zone_bottom = hub_y_adjusted + hub_height + total_spoke_height + (max_spoke_count * SPACING_BETWEEN_SPOKES) + SPACING_BELOW_HUB
        else:
            zone_bottom = hub_y_adjusted + hub_height + SPACING_BELOW_HUB
        zone_bottoms.append(zone_bottom)

    # 1b. Store edges between hubs if they peer with each other
    for i, zone1 in enumerate(zones):
        hub1_main_id = vnet_name_to_main_id[zone1.hub.name]
        hub1_x, hub1_y, hub1_height = hub_name_to_position[zone1.hub.name]
        hub1_center_y = hub1_y + (hub1_height / 2)
        for j, zone2 in enumerate(zones):
            if i < j and zone2.hub.name in zone1.hub.peering_names:
                hub2_main_id = vnet_name_to_main_id[zone2.hub.name]
                hub2_x, hub2_y, hub2_height = hub_name_to_position[zone2.hub.name]
                hub2_center_y = hub2_y + (hub2_height / 2)
                peering_index = zone1.hub.peering_names.index(zone2.hub.name)
                is_local = zone1.hub.peering_local_flags[peering_index] if peering_index < len(zone1.hub.peering_local_flags) else True
                # Pass coordinates so intermediate hub detection can work
                _add_edge_if_not_exists(hub1_main_id, hub2_main_id, is_local, zone1.hub.name, zone2.hub.name, hub1_x, hub2_x, hub1_center_y, hub2_center_y, hub1_height, hub2_height)

    # PHASE 1.5: Create external VNets using zone-based layout
    # Collect all external peerings
    external_vnets: dict[str, list[tuple[str, str]]] = {}
    for vnet in topology.virtual_networks:
        if vnet.name in hubless_spoke_names:
            continue
        if vnet.name in {s.name for s in stubs}:
            continue

        for i, peer_name in enumerate(vnet.peering_names):
            if peer_name in vnet_name_to_main_id:
                continue
            if peer_name in hubless_spoke_names:
                continue
            if peer_name in {s.name for s in stubs}:
                continue
            peering_resource_id = vnet.peering_resource_ids[i] if i < len(vnet.peering_resource_ids) else ""
            if peer_name not in external_vnets:
                external_vnets[peer_name] = []
            external_vnets[peer_name].append((peering_resource_id, vnet.name))

    # Filter external VNets for main page
    external_vnets_for_main_page: dict[str, list[tuple[str, str]]] = {}
    for external_vnet_name, peerings in external_vnets.items():
        peers_with_non_hubless = any(
            source_vnet_name not in hubless_spoke_names
            for _, source_vnet_name in peerings
        )
        if peers_with_non_hubless:
            external_vnets_for_main_page[external_vnet_name] = peerings

    # Calculate external zones for main page
    external_zones = calculate_external_zone_positions(
        external_vnets_for_main_page,
        zones,
        None,
        regular_spoke_positions,
        {},
        hub_name_to_position,
    )

    # Create legend
    legend_y = CANVAS_PADDING
    cell_id_counter, actual_legend_height = create_legend(root, cell_id_counter, legend_x, legend_y)

    # Create external VNets from zones
    zones_by_peer: dict[str, list] = {}
    for external_zone in external_zones:
        if external_zone.peer_vnet_name not in zones_by_peer:
            zones_by_peer[external_zone.peer_vnet_name] = []
        zones_by_peer[external_zone.peer_vnet_name].append(external_zone)

    # Process zones by peer, aligning left and right at same Y levels
    for peer_vnet_name, peer_zones in zones_by_peer.items():
        right_zone = None
        left_zone = None
        for zone in peer_zones:
            if hasattr(zone, 'is_right_zone'):
                if zone.is_right_zone:
                    right_zone = zone
                else:
                    left_zone = zone
            else:
                peer_center_x = None
                if peer_vnet_name in hub_name_to_position:
                    peer_x, _, _ = hub_name_to_position[peer_vnet_name]
                    peer_center_x = peer_x + (VNET_WIDTH / 2)
                elif peer_vnet_name in regular_spoke_positions:
                    peer_x, _, _ = regular_spoke_positions[peer_vnet_name]
                    peer_center_x = peer_x + (VNET_WIDTH / 2)
                elif peer_vnet_name in hubless_spoke_positions:
                    peer_x, _, _ = hubless_spoke_positions[peer_vnet_name]
                    peer_center_x = peer_x + (VNET_WIDTH / 2)

                if peer_center_x:
                    zone_center_x = zone.zone_x + (VNET_WIDTH / 2)
                    if zone_center_x > peer_center_x:
                        right_zone = zone
                    else:
                        left_zone = zone
                else:
                    if right_zone is None:
                        right_zone = zone
                    else:
                        left_zone = zone

        # Get peer VNet position
        if peer_vnet_name in hub_name_to_position:
            peer_x, peer_y, peer_height = hub_name_to_position[peer_vnet_name]
        elif peer_vnet_name in regular_spoke_positions:
            peer_x, peer_y, peer_height = regular_spoke_positions[peer_vnet_name]
        elif peer_vnet_name in hubless_spoke_positions:
            peer_x, peer_y, peer_height = hubless_spoke_positions[peer_vnet_name]
        else:
            continue

        external_start_y = peer_y - EXTERNAL_SPACING_Y - VNET_MIN_HEIGHT
        max_count = max(
            len(right_zone.external_vnet_names) if right_zone else 0,
            len(left_zone.external_vnet_names) if left_zone else 0
        )

        for level in range(max_count):
            level_y = external_start_y - level * (VNET_MIN_HEIGHT + EXTERNAL_SPACING_Y)

            if right_zone and level < len(right_zone.external_vnet_names):
                ext_idx = level
                external_vnet_name = right_zone.external_vnet_names[ext_idx]
                peering_resource_id = right_zone.peering_resource_ids[ext_idx]

                group_id, external_main_id, cell_id_counter = create_external_vnet_group(
                    root, cell_id_counter, external_vnet_name, peering_resource_id, right_zone.zone_x, level_y
                )
                vnet_name_to_main_id[external_vnet_name] = external_main_id

                if peer_vnet_name in vnet_name_to_main_id:
                    peer_main_id = vnet_name_to_main_id[peer_vnet_name]
                    peer_vnet = next((v for v in topology.virtual_networks if v.name == peer_vnet_name), None)

                    if peer_vnet and external_vnet_name in peer_vnet.peering_names:
                        peering_index = peer_vnet.peering_names.index(external_vnet_name)
                        is_local = peer_vnet.peering_local_flags[peering_index] if peering_index < len(peer_vnet.peering_local_flags) else False
                        external_height_val = VNET_MIN_HEIGHT

                        if peer_vnet_name in regular_spoke_positions:
                            peer_x, peer_y, peer_height = regular_spoke_positions[peer_vnet_name]
                            _add_edge_if_not_exists(
                                peer_main_id, external_main_id, is_local, peer_vnet_name, external_vnet_name,
                                float(peer_x), right_zone.zone_x, float(peer_y), level_y, float(peer_height), external_height_val
                            )
                        elif peer_vnet_name in hubless_spoke_positions:
                            peer_x, peer_y, peer_height = hubless_spoke_positions[peer_vnet_name]
                            _add_edge_if_not_exists(
                                peer_main_id, external_main_id, is_local, peer_vnet_name, external_vnet_name,
                                float(peer_x), right_zone.zone_x, float(peer_y), level_y, float(peer_height), external_height_val
                            )
                        elif peer_vnet_name in hub_name_to_position:
                            peer_x, peer_y, peer_height = hub_name_to_position[peer_vnet_name]
                            _add_edge_if_not_exists(
                                peer_main_id, external_main_id, is_local, peer_vnet_name, external_vnet_name,
                                float(peer_x), right_zone.zone_x, float(peer_y), level_y, float(peer_height), external_height_val
                            )

            if left_zone and level < len(left_zone.external_vnet_names):
                ext_idx = level
                external_vnet_name = left_zone.external_vnet_names[ext_idx]
                peering_resource_id = left_zone.peering_resource_ids[ext_idx]

                group_id, external_main_id, cell_id_counter = create_external_vnet_group(
                    root, cell_id_counter, external_vnet_name, peering_resource_id, left_zone.zone_x, level_y
                )
                vnet_name_to_main_id[external_vnet_name] = external_main_id

                if peer_vnet_name in vnet_name_to_main_id:
                    peer_main_id = vnet_name_to_main_id[peer_vnet_name]
                    peer_vnet = next((v for v in topology.virtual_networks if v.name == peer_vnet_name), None)

                    if peer_vnet and external_vnet_name in peer_vnet.peering_names:
                        peering_index = peer_vnet.peering_names.index(external_vnet_name)
                        is_local = peer_vnet.peering_local_flags[peering_index] if peering_index < len(peer_vnet.peering_local_flags) else False
                        external_height_val = VNET_MIN_HEIGHT

                        if peer_vnet_name in regular_spoke_positions:
                            peer_x, peer_y, peer_height = regular_spoke_positions[peer_vnet_name]
                            _add_edge_if_not_exists(
                                peer_main_id, external_main_id, is_local, peer_vnet_name, external_vnet_name,
                                float(peer_x), left_zone.zone_x, float(peer_y), level_y, float(peer_height), external_height_val
                            )
                        elif peer_vnet_name in hubless_spoke_positions:
                            peer_x, peer_y, peer_height = hubless_spoke_positions[peer_vnet_name]
                            _add_edge_if_not_exists(
                                peer_main_id, external_main_id, is_local, peer_vnet_name, external_vnet_name,
                                float(peer_x), left_zone.zone_x, float(peer_y), level_y, float(peer_height), external_height_val
                            )
                        elif peer_vnet_name in hub_name_to_position:
                            peer_x, peer_y, peer_height = hub_name_to_position[peer_vnet_name]
                            _add_edge_if_not_exists(
                                peer_main_id, external_main_id, is_local, peer_vnet_name, external_vnet_name,
                                float(peer_x), left_zone.zone_x, float(peer_y), level_y, float(peer_height), external_height_val
                            )

    # Handle single external VNet zones
    for external_zone in external_zones:
        if external_zone.peer_vnet_name in zones_by_peer and len(zones_by_peer[external_zone.peer_vnet_name]) > 1:
            continue

        peer_vnet_name = external_zone.peer_vnet_name
        peer_x_pos2: float
        peer_y_pos2: float
        peer_height_val2: float
        peer_x_pos2, peer_y_pos2, peer_height_val2 = 0.0, 0.0, float(VNET_MIN_HEIGHT)
        if peer_vnet_name in hub_name_to_position:
            peer_x_pos2, peer_y_pos2, peer_height_val2 = hub_name_to_position[peer_vnet_name]
        elif peer_vnet_name in regular_spoke_positions:
            peer_x_pos2, peer_y_pos2, peer_height_val2 = regular_spoke_positions[peer_vnet_name]
        elif peer_vnet_name in hubless_spoke_positions:
            peer_x_pos2, peer_y_pos2, peer_height_val2 = hubless_spoke_positions[peer_vnet_name]
        else:
            continue

        external_start_y = peer_y - EXTERNAL_SPACING_Y - VNET_MIN_HEIGHT

        for idx, external_vnet_name in enumerate(external_zone.external_vnet_names):
            peering_resource_id = external_zone.peering_resource_ids[idx]
            y_position = external_start_y - idx * (VNET_MIN_HEIGHT + EXTERNAL_SPACING_Y)
            x_position = external_zone.zone_x

            group_id, external_main_id, cell_id_counter = create_external_vnet_group(
                root, cell_id_counter, external_vnet_name, peering_resource_id, x_position, y_position
            )
            vnet_name_to_main_id[external_vnet_name] = external_main_id

            if peer_vnet_name in vnet_name_to_main_id:
                peer_main_id = vnet_name_to_main_id[peer_vnet_name]
                peer_vnet = next((v for v in topology.virtual_networks if v.name == peer_vnet_name), None)

                if peer_vnet and external_vnet_name in peer_vnet.peering_names:
                    peering_index = peer_vnet.peering_names.index(external_vnet_name)
                    is_local = peer_vnet.peering_local_flags[peering_index] if peering_index < len(peer_vnet.peering_local_flags) else False
                    external_height_val = VNET_MIN_HEIGHT

                    if peer_vnet_name in regular_spoke_positions:
                        peer_x, peer_y, peer_height = regular_spoke_positions[peer_vnet_name]
                        _add_edge_if_not_exists(
                            peer_main_id, external_main_id, is_local, peer_vnet_name, external_vnet_name,
                            float(peer_x), x_position, float(peer_y), y_position, float(peer_height), external_height_val
                        )
                    elif peer_vnet_name in hubless_spoke_positions:
                        peer_x, peer_y, peer_height = hubless_spoke_positions[peer_vnet_name]
                        _add_edge_if_not_exists(
                            peer_main_id, external_main_id, is_local, peer_vnet_name, external_vnet_name,
                            float(peer_x), x_position, float(peer_y), y_position, float(peer_height), external_height_val
                        )
                    elif peer_vnet_name in hub_name_to_position:
                        peer_x, peer_y, peer_height = hub_name_to_position[peer_vnet_name]
                        _add_edge_if_not_exists(
                            peer_main_id, external_main_id, is_local, peer_vnet_name, external_vnet_name,
                            float(peer_x), x_position, float(peer_y), y_position, float(peer_height), external_height_val
                        )

    # PHASE 2: Create all edges AFTER all VNets
    for vnet in topology.virtual_networks:
        for i, peer_name in enumerate(vnet.peering_names):
            if peer_name in vnet_name_to_main_id and vnet.name in vnet_name_to_main_id:
                is_local = vnet.peering_local_flags[i] if i < len(vnet.peering_local_flags) else True
                source_main_id = vnet_name_to_main_id[vnet.name]
                target_main_id = vnet_name_to_main_id[peer_name]
                source_is_hub = vnet.name in hub_names and vnet.name not in hubless_spoke_names
                target_is_hub = peer_name in hub_names and peer_name not in hubless_spoke_names
                vnet_name_to_tenant_id.get(vnet.name)
                vnet_name_to_tenant_id.get(peer_name)

                source_x, source_y, source_height = None, None, None
                target_x, target_y, target_height = None, None, None

                if vnet.name in hub_name_to_position:
                    source_x, source_y, source_height = hub_name_to_position[vnet.name]
                elif vnet.name in regular_spoke_positions:
                    source_x, source_y, source_height = regular_spoke_positions[vnet.name]
                elif vnet.name in hubless_spoke_positions:
                    source_x, source_y, source_height = hubless_spoke_positions[vnet.name]
                elif vnet.name in all_vnet_positions:
                    source_x, source_y, source_height = all_vnet_positions[vnet.name]

                if peer_name in hub_name_to_position:
                    target_x, target_y, target_height = hub_name_to_position[peer_name]
                elif peer_name in regular_spoke_positions:
                    target_x, target_y, target_height = regular_spoke_positions[peer_name]
                elif peer_name in hubless_spoke_positions:
                    target_x, target_y, target_height = hubless_spoke_positions[peer_name]
                elif peer_name in all_vnet_positions:
                    target_x, target_y, target_height = all_vnet_positions[peer_name]

                if source_is_hub and target_is_hub and source_y is not None and source_height is not None and target_y is not None and target_height is not None:
                    source_center_y = source_y + (source_height / 2)
                    target_center_y = target_y + (target_height / 2)
                    _add_edge_if_not_exists(source_main_id, target_main_id, is_local, vnet.name, peer_name, source_x, target_x, source_center_y, target_center_y, source_height, target_height)
                elif source_x is not None and target_x is not None and source_y is not None and target_y is not None and source_height is not None and target_height is not None:
                    _add_edge_if_not_exists(source_main_id, target_main_id, is_local, vnet.name, peer_name, source_x, target_x, source_y, target_y, source_height, target_height)
                else:
                    _add_edge_if_not_exists(source_main_id, target_main_id, is_local, vnet.name, peer_name)

    return (
        cell_id_counter,
        vnet_name_to_main_id,
        hub_name_to_position,
        regular_spoke_positions,
        hubless_spoke_positions,
        all_vnet_positions,
        edges_to_create,
    )

