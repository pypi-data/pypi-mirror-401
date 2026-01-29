"""Layout calculation and zone management for diagram generation.

This module provides clean separation between:
- Hub-spoke zones (one per hub)
- Hubless spoke zones (interconnected spokes without a hub)
- Zone position calculation
- Spoke position calculation

Following the pattern from cloudnetdraw's zone-based layout approach.
"""

from typing import NamedTuple

from gettopology.diagram.config import get_config
from gettopology.diagram.elements.vnet_elements import calculate_vnet_height
from gettopology.diagram.models import HubSpokeGroup
from gettopology.models import VirtualNetworkModel

# Get global config instance
_config = get_config()


class Zone(NamedTuple):
    """Represents a layout zone containing a hub and its spokes.

    Each hub gets its own zone, positioned horizontally.
    Spokes are assigned to zones based on which hub they peer with.
    """
    hub: VirtualNetworkModel
    hub_index: int
    spokes: list[VirtualNetworkModel]
    zone_x: float  # X position of zone start (hub X position)
    zone_y: float  # Y position of zone start (hub Y position)
    zone_bottom: float  # Bottom Y position of zone (updated after spoke positioning)


class HublessZone(NamedTuple):
    """Represents a hubless spoke zone (no hub, just interconnected spokes).

    The most-connected VNet acts as a "center" (like a hub) for layout purposes.
    Other VNets are arranged as spokes around it.
    """
    center_vnet: VirtualNetworkModel  # Most connected VNet acts as center
    spokes: list[VirtualNetworkModel]  # Remaining spokes
    zone_x: float
    zone_y: float
    zone_bottom: float


class ExternalZone(NamedTuple):
    """Represents an external VNet zone positioned above a peer VNet.

    External VNets are VNets that are peered with our topology but not fully collected.
    They are positioned above their peer VNet (hub, spoke, or hubless spoke).

    When multiple external VNets peer with the same VNet:
    - Single external VNet: Centered above the peer
    - Multiple external VNets: Split into left and right vertical stacks (index 0=right, 1=left, 2=right, etc.)
      This prevents lines from going through external VNet boxes.
    """
    peer_vnet_name: str  # Name of the VNet this external zone is positioned above
    external_vnet_names: list[str]  # List of external VNet names (stacked vertically in this zone)
    peering_resource_ids: list[str]  # Resource IDs for each external VNet (same order)
    zone_x: float  # X position (left side of zone, may be left or right of peer center)
    zone_y: float  # Y position (top of external zone)
    zone_bottom: float  # Bottom Y position of the zone
    is_right_zone: bool = True  # True if this is a right zone, False if left zone (for multiple external VNets)


def calculate_zone_positions(
    hub_spoke_groups: list[HubSpokeGroup],
    hubless_groups: list[list[VirtualNetworkModel]],
) -> tuple[list[Zone], list[HublessZone]]:
    """Calculate zone positions for hub-spoke groups and hubless spoke groups.

    This function separates the layout logic cleanly:
    - Hub-spoke groups get their own zones (one per hub)
    - Each hubless spoke group gets its own zone (treated as a hub-spoke pattern)

    Args:
        hub_spoke_groups: List of hub-spoke groups
        hubless_groups: List of hubless spoke groups (each group is a list of connected VNets)

    Returns:
        Tuple of (list of Zones, list of HublessZones)
    """
    page_width = _config.page_width
    legend_width = _config.legend_width
    # Shift canvas center right by legend width to make space for legend
    canvas_center_x = (page_width / 2) + legend_width
    vnet_width = _config.vnet_width
    zone_width = _config.zone_width
    zone_spacing = _config.zone_spacing

    # Adjust hub_y to account for legend height (legend is at top, ensure hubs are below it)
    legend_height = _config.legend_height
    legend_padding = _config.canvas_padding
    legend_bottom = legend_padding + legend_height
    legend_bottom_with_padding = legend_bottom + 20  # Extra padding below legend

    # Use the higher of: configured hub_y or legend_bottom_with_padding
    base_hub_y = _config.hub_y
    hub_y = max(base_hub_y, legend_bottom_with_padding)

    # Calculate hub center X (for single hub, center it; for multiple, space them)
    # Account for legend on the left
    hub_x_center = canvas_center_x - (vnet_width / 2)

    # Calculate hub heights for alignment
    hub_heights = [calculate_vnet_height(group.hub) for group in hub_spoke_groups]
    # Also consider hubless center heights for alignment
    hubless_center_heights = []
    for hubless_group in hubless_groups:
        if hubless_group:
            center_vnet = max(hubless_group, key=lambda v: v.peering_count)
            hubless_center_heights.append(calculate_vnet_height(center_vnet))
    all_heights = hub_heights + hubless_center_heights
    max_hub_height = max(all_heights) if all_heights else _config.vnet_min_height
    target_hub_center_y = hub_y + (max_hub_height / 2)

    zones: list[Zone] = []

    # Create zones for each hub-spoke group
    for zone_index, group in enumerate(hub_spoke_groups):
        # Calculate zone X position
        if len(hub_spoke_groups) > 1:
            zone_offset_x = zone_index * (zone_width + zone_spacing)
            zone_x = hub_x_center + zone_offset_x - (len(hub_spoke_groups) - 1) * (zone_width + zone_spacing) / 2
        else:
            zone_x = hub_x_center

        # Calculate hub Y position (center-aligned)
        hub_height = calculate_vnet_height(group.hub)
        hub_y_adjusted = target_hub_center_y - (hub_height / 2)

        # Calculate zone bottom (will be updated after spoke positioning)
        zone_bottom = hub_y_adjusted + hub_height

        zone = Zone(
            hub=group.hub,
            hub_index=zone_index,
            spokes=group.spokes,
            zone_x=zone_x,
            zone_y=hub_y_adjusted,
            zone_bottom=zone_bottom,
        )
        zones.append(zone)

    # Create hubless zones for each independent group
    hubless_zones: list[HublessZone] = []
    total_zones = len(hub_spoke_groups) + len(hubless_groups)

    for group_index, hubless_group in enumerate(hubless_groups):
        # Find most connected VNet to act as center (within this group)
        center_vnet = max(hubless_group, key=lambda v: v.peering_count)
        remaining_spokes = [v for v in hubless_group if v.name != center_vnet.name]

        # Calculate hubless zone X position (after all hub zones and previous hubless zones)
        hubless_zone_index = len(hub_spoke_groups) + group_index
        if total_zones > 1:
            zone_offset_x = hubless_zone_index * (zone_width + zone_spacing)
            hubless_zone_x = hub_x_center + zone_offset_x - (total_zones - 1) * (zone_width + zone_spacing) / 2
        else:
            # Only one zone total, center it
            hubless_zone_x = hub_x_center

        # Calculate center VNet Y position (align with hub centers)
        center_height = calculate_vnet_height(center_vnet)
        center_y_adjusted = target_hub_center_y - (center_height / 2)

        # Calculate zone bottom (will be updated after spoke positioning)
        hubless_zone_bottom = center_y_adjusted + center_height

        hubless_zone = HublessZone(
            center_vnet=center_vnet,
            spokes=remaining_spokes,
            zone_x=hubless_zone_x,
            zone_y=center_y_adjusted,
            zone_bottom=hubless_zone_bottom,
        )
        hubless_zones.append(hubless_zone)

    return zones, hubless_zones


def calculate_spoke_positions(
    zone: Zone,
    is_left: bool,
) -> list[tuple[VirtualNetworkModel, float, float]]:
    """Calculate positions for spokes in a zone.

    Args:
        zone: Zone containing hub and spokes
        is_left: True for left spokes, False for right spokes

    Returns:
        List of (spoke, x_position, y_position) tuples
    """
    hub_x = zone.zone_x
    hub_y = zone.zone_y
    hub_height = calculate_vnet_height(zone.hub)

    vnet_spacing_x = _config.vnet_spacing_x
    spacing_below_hub = _config.spacing_below_hub
    spacing_between_spokes = _config.spacing_between_spokes

    # Calculate starting Y position (below hub)
    spoke_start_y = hub_y + hub_height + spacing_below_hub

    # Calculate X position
    if is_left:
        x_position = hub_x - vnet_spacing_x
    else:
        x_position = hub_x + vnet_spacing_x

    # Calculate Y positions for each spoke
    positions: list[tuple[VirtualNetworkModel, float, float]] = []
    current_y = spoke_start_y

    # Filter spokes by side (even indices = left, odd = right)
    spokes = zone.spokes
    if is_left:
        # Left spokes: even indices
        spokes = [spoke for i, spoke in enumerate(spokes) if i % 2 == 0]
    else:
        # Right spokes: odd indices
        spokes = [spoke for i, spoke in enumerate(spokes) if i % 2 == 1]

    for spoke in spokes:
        positions.append((spoke, x_position, current_y))
        spoke_height = calculate_vnet_height(spoke)
        current_y += spoke_height + spacing_between_spokes

    return positions


def calculate_hubless_spoke_positions(
    hubless_zone: HublessZone,
) -> list[tuple[VirtualNetworkModel, float, float]]:
    """Calculate positions for hubless spokes.

    Args:
        hubless_zone: HublessZone containing center VNet and spokes

    Returns:
        List of (vnet, x_position, y_position) tuples, including center VNet first
    """
    center_x = hubless_zone.zone_x
    center_y = hubless_zone.zone_y
    center_height = calculate_vnet_height(hubless_zone.center_vnet)

    vnet_spacing_x = _config.vnet_spacing_x
    spacing_below_hub = _config.spacing_below_hub
    spacing_between_spokes = _config.spacing_between_spokes

    positions: list[tuple[VirtualNetworkModel, float, float]] = []

    # Add center VNet first
    positions.append((hubless_zone.center_vnet, center_x, center_y))

    # Calculate starting Y for remaining spokes
    spoke_start_y = center_y + center_height + spacing_below_hub

    # Split remaining spokes into left and right
    left_spokes: list[VirtualNetworkModel] = []
    right_spokes: list[VirtualNetworkModel] = []

    for index, spoke in enumerate(hubless_zone.spokes):
        if index % 2 == 0:  # Even indices go left
            left_spokes.append(spoke)
        else:  # Odd indices go right
            right_spokes.append(spoke)

    # Position left spokes
    current_y_left = spoke_start_y
    for spoke in left_spokes:
        x_position = center_x - vnet_spacing_x
        positions.append((spoke, x_position, current_y_left))
        spoke_height = calculate_vnet_height(spoke)
        current_y_left += spoke_height + spacing_between_spokes

    # Position right spokes
    current_y_right = spoke_start_y
    if left_spokes:
        # Right spokes start after first left spoke
        first_left_height = calculate_vnet_height(left_spokes[0])
        current_y_right = spoke_start_y + first_left_height + spacing_between_spokes

    for spoke in right_spokes:
        x_position = center_x + vnet_spacing_x
        positions.append((spoke, x_position, current_y_right))
        spoke_height = calculate_vnet_height(spoke)
        current_y_right += spoke_height + spacing_between_spokes

    return positions


def find_first_hub_zone(
    spoke: VirtualNetworkModel,
    hub_spoke_groups: list[HubSpokeGroup],
) -> int:
    """Find the first hub zone this spoke connects to.

    Simplified logic: assigns spoke to the first hub it peers with.
    This matches the cloudnetdraw pattern.

    Args:
        spoke: Spoke VNet to find zone for
        hub_spoke_groups: List of hub-spoke groups

    Returns:
        Zone index (0-based)
    """
    spoke_peering_names = set(spoke.peering_names)

    for zone_index, group in enumerate(hub_spoke_groups):
        if group.hub.name in spoke_peering_names:
            return zone_index

    # Fallback: return first zone
    return 0


def calculate_external_zone_positions(
    external_vnets: dict[str, list[tuple[str, str]]],  # external_vnet_name -> list of (peering_resource_id, source_vnet_name)
    zones: list[Zone],
    hubless_zone: HublessZone | None,
    regular_spoke_positions: dict[str, tuple[float, float, float]],  # vnet_name -> (x, y, height)
    hubless_spoke_positions: dict[str, tuple[float, float, float]],  # vnet_name -> (x, y, height)
    hub_name_to_position: dict[str, tuple[float, float, float]],  # hub_name -> (x, y, height)
) -> list[ExternalZone]:
    """Calculate zone positions for external VNets with horizontal overlap avoidance.

    External VNets are positioned ABOVE their peer VNets (always going UP, never at same level or below).
    Peer VNets can be:
    - Hub (from hub/spoke groups)
    - Spoke (from hub/spoke groups)
    - Central spoke (from hubless spoke groups)

    Stacking Strategy (same as spokes but going UP instead of DOWN):
    - Single external VNet: Centered above the peer
    - Multiple external VNets for same peer: Split into left and right stacks going UP
      - First (index 0): Right side, closest to peer (level 0)
      - Second (index 1): Left side, same Y as first (level 0)
      - Third (index 2): Right side, above first (level 1)
      - Fourth (index 3): Left side, same Y as third (level 1)
      - etc.

    To prevent horizontal overlaps between external zones from different peers, zones are
    shifted left or right when they would overlap with other external zones.

    Args:
        external_vnets: Dict mapping external VNet names to their peerings
        zones: List of hub-spoke zones
        hubless_zone: Optional hubless zone
        regular_spoke_positions: Dict of regular spoke positions
        hubless_spoke_positions: Dict of hubless spoke positions (including central spoke)
        hub_name_to_position: Dict of hub positions

    Returns:
        List of ExternalZone objects, one per unique peer VNet
    """
    external_spacing_y = _config.external_spacing_y
    external_spacing_x = _config.external_spacing_x
    vnet_min_height = _config.vnet_min_height
    vnet_width = _config.vnet_width

    # Group external VNets by their peer VNet (prioritize spokes over hubs)
    # Map: peer_vnet_name -> list of (external_vnet_name, peering_resource_id)
    external_by_peer: dict[str, list[tuple[str, str]]] = {}

    for external_vnet_name, peerings in external_vnets.items():
        # Find the best peer VNet (prioritize spokes over hubs)
        peer_vnet_name = None
        peering_resource_id = ""

        # First, try to find a regular spoke peer
        for peering_resource_id, source_vnet_name in peerings:
            if source_vnet_name in regular_spoke_positions:
                peer_vnet_name = source_vnet_name
                break

        # If no regular spoke, try hubless spoke
        if not peer_vnet_name:
            for peering_resource_id, source_vnet_name in peerings:
                if source_vnet_name in hubless_spoke_positions:
                    peer_vnet_name = source_vnet_name
                    break

        # If no spoke, use hub (or first available peer)
        if not peer_vnet_name:
            peering_resource_id, source_vnet_name = peerings[0]
            if source_vnet_name in hub_name_to_position:
                peer_vnet_name = source_vnet_name
            else:
                # Fallback: use first available peer
                peer_vnet_name = source_vnet_name

        # Group by peer VNet
        if peer_vnet_name not in external_by_peer:
            external_by_peer[peer_vnet_name] = []
        external_by_peer[peer_vnet_name].append((external_vnet_name, peering_resource_id))

    # Combine all VNet positions into a single dict for overlap checking
    all_vnet_positions: dict[str, tuple[float, float, float]] = {}
    all_vnet_positions.update(hub_name_to_position)
    all_vnet_positions.update(regular_spoke_positions)
    all_vnet_positions.update(hubless_spoke_positions)

    # Step 1: Create initial ExternalZone positions (centered above peers)
    # For multiple external VNets peering with the same VNet, split into left/right stacks
    initial_zones: list[ExternalZone] = []

    for peer_vnet_name, external_list in external_by_peer.items():
        # Get peer VNet position
        peer_x: float = 0.0
        peer_y: float = 0.0
        peer_height: float = vnet_min_height

        if peer_vnet_name in regular_spoke_positions:
            peer_x, peer_y, peer_height = regular_spoke_positions[peer_vnet_name]
        elif peer_vnet_name in hubless_spoke_positions:
            peer_x, peer_y, peer_height = hubless_spoke_positions[peer_vnet_name]
        elif peer_vnet_name in hub_name_to_position:
            peer_x, peer_y, peer_height = hub_name_to_position[peer_vnet_name]
        else:
            # Fallback: use default position
            continue

        # Find all VNets in the same vertical column (overlapping X position)
        # This includes the hub above the spoke, and any other VNets in that column
        topmost_y = peer_y  # Start with peer VNet's top Y
        peer_bottom_y = peer_y + peer_height
        peer_center_x = peer_x + (vnet_width / 2)

        # Check all VNets to find the topmost one in this vertical column
        for vnet_name, (vnet_x, vnet_y, vnet_h) in all_vnet_positions.items():
            # Skip the peer VNet itself
            if vnet_name == peer_vnet_name:
                continue

            # Check if VNet overlaps horizontally with the peer (same vertical column)
            vnet_left = vnet_x
            vnet_right = vnet_x + vnet_width
            peer_left = peer_x
            peer_right = peer_x + vnet_width

            # Check for horizontal overlap
            if not (vnet_right < peer_left or vnet_left > peer_right):
                # VNets overlap horizontally - check if this VNet is above the peer
                vnet_bottom_y = vnet_y + vnet_h
                # If this VNet is above the peer (or overlaps with it), track its top
                if vnet_bottom_y <= peer_bottom_y:
                    # This VNet is above or at the same level as peer - use its top
                    if vnet_y < topmost_y:
                        topmost_y = vnet_y

        # Split external VNets into left and right stacks (similar to spokes)
        num_external = len(external_list)

        if num_external == 1:
            # Single external VNet: position on RIGHT side (first external always goes right)
            # This prevents connector line from going through the external VNet box
            external_vnet_name, peering_resource_id = external_list[0]
            vnet_spacing_x = _config.vnet_spacing_x
            initial_zone_x = peer_center_x + vnet_spacing_x - (vnet_width / 2)  # Right side
            total_external_height = vnet_min_height
            zone_y = topmost_y - external_spacing_y - total_external_height
            zone_bottom = topmost_y - external_spacing_y

            initial_zone = ExternalZone(
                peer_vnet_name=peer_vnet_name,
                external_vnet_names=[external_vnet_name],
                peering_resource_ids=[peering_resource_id],
                zone_x=initial_zone_x,
                zone_y=zone_y,
                zone_bottom=zone_bottom,
                is_right_zone=True,  # Single VNet goes to right side
            )
            initial_zones.append(initial_zone)
        else:
            # Multiple external VNets: use same logic as spokes but going UP instead of DOWN
            # First (index 0): right, closest to hub/spoke (top position)
            # Second (index 1): left, same Y as first (top position)
            # Third (index 2): right, above first (second position)
            # Fourth (index 3): left, same Y as third (second position)
            # This mirrors spoke positioning: even indices = right, odd indices = left, but going UP
            vnet_spacing_x = _config.vnet_spacing_x

            # Group external VNets by side (same as spokes: even=right, odd=left)
            right_external: list[tuple[str, str]] = []  # (name, rid) - indices 0, 2, 4...
            left_external: list[tuple[str, str]] = []  # (name, rid) - indices 1, 3, 5...

            for index, (ext_name, ext_rid) in enumerate(external_list):
                if index % 2 == 0:  # Even indices (0, 2, 4...) go right
                    right_external.append((ext_name, ext_rid))
                else:  # Odd indices (1, 3, 5...) go left
                    left_external.append((ext_name, ext_rid))

            # Calculate positions needed (max of left and right counts)
            max_positions = max(len(right_external), len(left_external))

            # Calculate total height needed (stack going UP)
            total_height = max_positions * vnet_min_height + (max_positions - 1) * external_spacing_y if max_positions > 0 else 0

            # Calculate Y position: start from topmost_y and go UP
            # zone_bottom is where the first external VNet's bottom should be (closest to hub/spoke)
            zone_bottom = topmost_y - external_spacing_y
            zone_y = zone_bottom - total_height

            # Create separate zones for right and left sides (same Y so they align horizontally)
            if right_external:
                right_zone_x = peer_center_x + vnet_spacing_x - (vnet_width / 2)
                right_vnet_names = [name for name, _ in right_external]
                right_resource_ids = [rid for _, rid in right_external]

                right_zone = ExternalZone(
                    peer_vnet_name=peer_vnet_name,
                    external_vnet_names=right_vnet_names,
                    peering_resource_ids=right_resource_ids,
                    zone_x=right_zone_x,
                    zone_y=zone_y,
                    zone_bottom=zone_bottom,
                    is_right_zone=True,
                )
                initial_zones.append(right_zone)

            if left_external:
                left_zone_x = peer_center_x - vnet_spacing_x - (vnet_width / 2)
                left_vnet_names = [name for name, _ in left_external]
                left_resource_ids = [rid for _, rid in left_external]

                left_zone = ExternalZone(
                    peer_vnet_name=peer_vnet_name,
                    external_vnet_names=left_vnet_names,
                    peering_resource_ids=left_resource_ids,
                    zone_x=left_zone_x,
                    zone_y=zone_y,  # Same Y as right zone so they align horizontally
                    zone_bottom=zone_bottom,
                    is_right_zone=False,
                )
                initial_zones.append(left_zone)

    # Step 2: Resolve horizontal overlaps by shifting zones left/right
    # Track occupied zones with their Y ranges: list of (left_x, right_x, top_y, bottom_y) tuples
    occupied_zones: list[tuple[float, float, float, float]] = []
    final_zones: list[ExternalZone] = []

    # Sort zones by Y position (top to bottom) to process them in order
    sorted_zones = sorted(initial_zones, key=lambda z: z.zone_y)

    for zone in sorted_zones:
        zone_left = zone.zone_x
        zone_right = zone.zone_x + vnet_width
        zone_top = zone.zone_y
        zone_bottom = zone.zone_bottom

        # Check for horizontal overlap with already-placed zones that also overlap vertically
        has_overlap = False
        for occupied_left, occupied_right, occupied_top, occupied_bottom in occupied_zones:
            # Check if X ranges overlap AND Y ranges overlap
            x_overlaps = not (zone_right < occupied_left or zone_left > occupied_right)
            y_overlaps = not (zone_bottom < occupied_top or zone_top > occupied_bottom)
            if x_overlaps and y_overlaps:
                has_overlap = True
                break

        if has_overlap:
            # Find a non-overlapping position by shifting left or right
            # Try shifting right first, then left
            shift_amount = vnet_width + external_spacing_x
            new_zone_x = zone.zone_x

            # Try shifting right
            right_shift = zone.zone_x + shift_amount
            right_overlaps = False
            for occupied_left, occupied_right, occupied_top, occupied_bottom in occupied_zones:
                right_zone_left = right_shift
                right_zone_right = right_shift + vnet_width
                x_overlaps = not (right_zone_right < occupied_left or right_zone_left > occupied_right)
                y_overlaps = not (zone_bottom < occupied_top or zone_top > occupied_bottom)
                if x_overlaps and y_overlaps:
                    right_overlaps = True
                    break

            if not right_overlaps:
                new_zone_x = right_shift
            else:
                # Try shifting left
                left_shift = zone.zone_x - shift_amount
                left_overlaps = False
                for occupied_left, occupied_right, occupied_top, occupied_bottom in occupied_zones:
                    left_zone_left = left_shift
                    left_zone_right = left_shift + vnet_width
                    x_overlaps = not (left_zone_right < occupied_left or left_zone_left > occupied_right)
                    y_overlaps = not (zone_bottom < occupied_top or zone_top > occupied_bottom)
                    if x_overlaps and y_overlaps:
                        left_overlaps = True
                        break

                if not left_overlaps:
                    new_zone_x = left_shift
                else:
                    # Both sides overlap - try further shifts
                    # Keep trying right shifts until we find a free spot
                    max_shifts = 10  # Prevent infinite loops
                    for i in range(1, max_shifts):
                        test_x = zone.zone_x + (shift_amount * i)
                        test_left = test_x
                        test_right = test_x + vnet_width
                        test_overlaps = False
                        for occupied_left, occupied_right, occupied_top, occupied_bottom in occupied_zones:
                            x_overlaps = not (test_right < occupied_left or test_left > occupied_right)
                            y_overlaps = not (zone_bottom < occupied_top or zone_top > occupied_bottom)
                            if x_overlaps and y_overlaps:
                                test_overlaps = True
                                break
                        if not test_overlaps:
                            new_zone_x = test_x
                            break

                    # If still overlapping, try left shifts
                    if new_zone_x == zone.zone_x:
                        for i in range(1, max_shifts):
                            test_x = zone.zone_x - (shift_amount * i)
                            test_left = test_x
                            test_right = test_x + vnet_width
                            test_overlaps = False
                            for occupied_x_left, occupied_x_right, occupied_y_top, occupied_y_bottom in occupied_zones:
                                x_overlaps = not (test_right < occupied_x_left or test_left > occupied_x_right)
                                y_overlaps = not (zone_bottom < occupied_y_top or zone_top > occupied_y_bottom)
                                if x_overlaps and y_overlaps:
                                    test_overlaps = True
                                    break
                            if not test_overlaps:
                                new_zone_x = test_x
                                break

            # Create zone with adjusted X position (preserve is_right_zone flag)
            is_right = zone.is_right_zone if hasattr(zone, 'is_right_zone') else True
            adjusted_zone = ExternalZone(
                peer_vnet_name=zone.peer_vnet_name,
                external_vnet_names=zone.external_vnet_names,
                peering_resource_ids=zone.peering_resource_ids,
                zone_x=new_zone_x,
                zone_y=zone.zone_y,
                zone_bottom=zone.zone_bottom,
                is_right_zone=is_right,
            )
            final_zones.append(adjusted_zone)
            # Track the occupied zone (X and Y ranges)
            occupied_zones.append((new_zone_x, new_zone_x + vnet_width, zone_top, zone_bottom))
        else:
            # No overlap, use original position
            final_zones.append(zone)
            # Track the occupied zone (X and Y ranges)
            occupied_zones.append((zone_left, zone_right, zone_top, zone_bottom))

    return final_zones

