"""External VNet connection logic for diagram generation.

Handles connections to external VNets (VNets that are peered but not in the topology):
- Hub/hubless center to external: top center to side center with branching
- Spoke to external: route around hub if present
- Non-central hubless spoke to external: connect from outside edge
"""

from xml.etree.ElementTree import Element, SubElement

from gettopology.diagram.config import get_config
from gettopology.diagram.connections.base import (
    ROUTING_WAYPOINT_OFFSET_HORIZONTAL,
    ROUTING_WAYPOINT_OFFSET_VERTICAL,
    VNET_WIDTH,
)
from gettopology.diagram.elements.edge_elements import create_waypoint

# Get global config instance
_config = get_config()


def is_external_connection(
    source_x: float | None,
    target_x: float | None,
    source_y: float | None,
    target_y: float | None,
    source_height: float | None,
    target_height: float | None,
) -> bool:
    """Check if this is an external connection.

    External VNet is above hub/hubless spoke and horizontally aligned.

    Args:
        source_x: Source VNet X position (left edge)
        target_x: Target VNet X position (left edge)
        source_y: Source VNet Y position (top edge)
        target_y: Target VNet Y position (top edge)
        source_height: Source VNet height
        target_height: Target VNet height

    Returns:
        True if this is an external connection
    """
    if source_x is None or target_x is None or source_y is None or target_y is None or source_height is None or target_height is None:
        return False

    source_center_x = source_x + (VNET_WIDTH / 2)
    target_center_x = target_x + (VNET_WIDTH / 2)
    target_bottom_y = target_y + target_height
    source_top_y = source_y

    # External connection: external VNet (target) is above source, and they're horizontally aligned
    # Use more lenient horizontal alignment check (within VNET_WIDTH) to catch hubless spoke connections
    return target_bottom_y < source_top_y and abs(target_center_x - source_center_x) < VNET_WIDTH


def create_external_connection(
    root: Element,
    mxGeometry: Element,
    source_x: float,
    target_x: float,
    source_y: float,
    target_y: float,
    source_height: float,
    target_height: float,
    source_name: str,
    source_is_hub: bool,
    hubless_centers: dict[int, str] | None = None,
    hubless_group_map: dict[str, int] | None = None,
    hub_positions: dict[str, tuple[float, float, float]] | None = None,
    all_vnet_positions: dict[str, tuple[float, float, float]] | None = None,
) -> None:
    """Create external VNet connection with appropriate routing.

    Handles three cases:
    1. Hub/hubless center to external: top center to side center with branching
    2. Spoke to external: route around hub if present
    3. Non-central hubless spoke to external: connect from outside edge

    Args:
        root: Root XML element (not used, but kept for consistency)
        mxGeometry: Geometry element to set connection points and add waypoints
        source_x: Source VNet X position (left edge)
        target_x: Target VNet X position (left edge)
        source_y: Source VNet Y position (top edge)
        target_y: Target VNet Y position (top edge)
        source_height: Source VNet height
        target_height: Target VNet height
        source_name: Source VNet name
        source_is_hub: Whether source is a hub
        hubless_centers: Map of group_index -> center_name
        hubless_group_map: Map of vnet_name -> group_index
        hub_positions: Dict of hub positions for routing around hubs
        all_vnet_positions: Dict of all VNet positions for routing
    """
    # Check if source is a hub or hubless center
    is_hubless_center = False
    if hubless_centers:
        is_hubless_center = source_name in hubless_centers.values()
    is_central_peer = source_is_hub or is_hubless_center

    # Check if source is a non-central hubless spoke
    is_non_central_hubless = False
    if hubless_group_map and hubless_centers and source_name in hubless_group_map:
        source_group = hubless_group_map.get(source_name)
        if source_group is not None:
            center_name = hubless_centers.get(source_group)
            is_non_central_hubless = (center_name is not None and source_name != center_name)

    if is_central_peer:
        # Hub or hubless center with external VNets in left/right stacks
        # Route: Start from top center (at height/2 from top), go up, then branch left/right to side center of external box
        _create_central_to_external_connection(
            mxGeometry,
            source_x, target_x,
            source_y, target_y,
            source_height, target_height
        )
    elif not source_is_hub and hub_positions:
        # Spoke-to-external connection: Add waypoints to route around hub
        _create_spoke_to_external_connection(
            mxGeometry,
            source_x, target_x,
            source_y, target_y,
            source_height, target_height,
            hub_positions
        )
    elif is_non_central_hubless:
        # Non-central hubless spoke to external: connect from outside edge
        _create_hubless_spoke_to_external_connection(
            mxGeometry,
            source_x, target_x,
            source_name,
            hubless_group_map,
            hubless_centers,
            hub_positions,
            all_vnet_positions
        )


def _create_central_to_external_connection(
    mxGeometry: Element,
    source_x: float,
    target_x: float,
    source_y: float,
    target_y: float,
    source_height: float,
    target_height: float,
) -> None:
    """Create connection from hub/hubless center to external VNet.

    Routes from top center, up, then branches left/right to side center of external box.
    """
    source_center_x = source_x + (VNET_WIDTH / 2)  # Center X of hub/center
    source_y + (source_height / 2)  # Top center Y (at height/2 from top)

    target_side_center_y = target_y + (target_height / 2)  # Side center Y (at height/2 from top)

    # Determine if external VNet is on left or right side
    is_left_stack = target_x < source_center_x

    # Calculate connection points
    if is_left_stack:
        # Left stack: connect to left side center of external box
        target_connection_x = target_x  # Left edge
    else:
        # Right stack: connect to right side center of external box
        target_connection_x = target_x + VNET_WIDTH  # Right edge

    # Set normalized connection points
    # Source: top center (at height/2 from top) - this is actually the middle, not top
    # We want to connect from the top edge at center X, so exitY should be 0.0 (top edge)
    mxGeometry.set("exitX", "0.5")  # Horizontal center
    mxGeometry.set("exitY", "0.0")  # Top edge (we'll use waypoints to route from top center)
    mxGeometry.set("exitDx", "0")
    mxGeometry.set("exitDy", "0")
    mxGeometry.set("exitPerimeter", "1")

    # Target: side center (left or right side, at height/2 from top)
    if is_left_stack:
        mxGeometry.set("entryX", "0.0")  # Left edge
    else:
        mxGeometry.set("entryX", "1.0")  # Right edge
    mxGeometry.set("entryY", "0.5")  # At height/2 from top (middle of height)
    mxGeometry.set("entryDx", "0")
    mxGeometry.set("entryDy", "0")
    mxGeometry.set("entryPerimeter", "1")

    # Add waypoints: go up from top center, then branch left/right to external box side
    array_elem = SubElement(mxGeometry, "Array")
    array_elem.set("as", "points")

    # Waypoint 1: At source top center (top edge at center X) - start point
    create_waypoint(array_elem, source_center_x, source_y)  # Top edge Y

    # Waypoint 2: Go up from top center
    create_waypoint(array_elem, source_center_x, source_y - ROUTING_WAYPOINT_OFFSET_VERTICAL)

    # Waypoint 3: At the Y level of external box side center, but still at source center X (before branching)
    create_waypoint(array_elem, source_center_x, target_side_center_y)

    # Waypoint 4: At external box side center (final connection point)
    create_waypoint(array_elem, target_connection_x, target_side_center_y)


def _create_spoke_to_external_connection(
    mxGeometry: Element,
    source_x: float,
    target_x: float,
    source_y: float,
    target_y: float,
    source_height: float,
    target_height: float,
    hub_positions: dict[str, tuple[float, float, float]],
) -> None:
    """Create connection from spoke to external VNet, routing around hub if present.

    The external VNet is above the spoke, but we need to avoid going through the hub.
    """
    source_center_x = source_x + (VNET_WIDTH / 2)
    source_top_y = source_y
    target_center_x = target_x + (VNET_WIDTH / 2)
    target_bottom_y = target_y + target_height

    # Find if there's a hub between the spoke and external VNet
    hub_in_path = False
    hub_x = None
    hub_y = None
    hub_height = None

    for hub_name, (h_x, h_y, h_height) in hub_positions.items():
        hub_center_x = h_x + (VNET_WIDTH / 2)
        hub_top_y = h_y
        hub_bottom_y = h_y + h_height

        # Check if hub is horizontally between source and target, and vertically between them
        min_x = min(source_center_x, target_center_x)
        max_x = max(source_center_x, target_center_x)
        if (min_x <= hub_center_x <= max_x and
            source_top_y < hub_bottom_y and
            target_bottom_y < hub_top_y):
            hub_in_path = True
            hub_x = h_x
            hub_y = h_y
            hub_height = h_height
            break

    if hub_in_path and hub_x is not None and hub_y is not None and hub_height is not None:
        # Route around hub: go horizontally first, then up, then back horizontally, then up to external
        # Determine which side to route around (prefer the side with more space)
        source_left_edge = source_x
        source_right_edge = source_x + VNET_WIDTH
        hub_left_edge = hub_x
        hub_right_edge = hub_x + VNET_WIDTH

        # Calculate space on left and right sides
        space_left = abs(source_left_edge - hub_right_edge) if source_x < hub_x else abs(hub_left_edge - source_right_edge)
        space_right = abs(source_right_edge - hub_left_edge) if source_x > hub_x else abs(hub_right_edge - source_left_edge)

        # Route around the side with more space
        array_elem = SubElement(mxGeometry, "Array")
        array_elem.set("as", "points")

        if space_left > space_right:
            # Route left: go left from spoke, then up above hub, then right to center, then up to external
            create_waypoint(array_elem, source_x - ROUTING_WAYPOINT_OFFSET_HORIZONTAL, source_top_y)
            create_waypoint(array_elem, source_x - ROUTING_WAYPOINT_OFFSET_HORIZONTAL, hub_y - ROUTING_WAYPOINT_OFFSET_VERTICAL)
            create_waypoint(array_elem, target_center_x, hub_y - ROUTING_WAYPOINT_OFFSET_VERTICAL)
        else:
            # Route right: go right from spoke, then up above hub, then left to center, then up to external
            create_waypoint(array_elem, source_x + VNET_WIDTH + ROUTING_WAYPOINT_OFFSET_HORIZONTAL, source_top_y)
            create_waypoint(array_elem, source_x + VNET_WIDTH + ROUTING_WAYPOINT_OFFSET_HORIZONTAL, hub_y - ROUTING_WAYPOINT_OFFSET_VERTICAL)
            create_waypoint(array_elem, target_center_x, hub_y - ROUTING_WAYPOINT_OFFSET_VERTICAL)
    # else: No hub in path, let orthogonalEdgeStyle handle routing automatically


def _create_hubless_spoke_to_external_connection(
    mxGeometry: Element,
    source_x: float,
    target_x: float,
    source_name: str,
    hubless_group_map: dict[str, int] | None,
    hubless_centers: dict[int, str] | None,
    hub_positions: dict[str, tuple[float, float, float]] | None,
    all_vnet_positions: dict[str, tuple[float, float, float]] | None,
) -> None:
    """Create connection from non-central hubless spoke to external VNet.

    Connects from outside edge of the spoke to bottom center of external VNet.
    """
    if not hubless_group_map or not hubless_centers:
        return

    source_group = hubless_group_map.get(source_name)
    if source_group is None:
        return

    center_name = hubless_centers.get(source_group)
    if not center_name:
        return

    # Find center position
    center_x = None
    if hub_positions and center_name in hub_positions:
        center_x, _, _ = hub_positions[center_name]
    elif all_vnet_positions and center_name in all_vnet_positions:
        center_x, _, _ = all_vnet_positions[center_name]

    if center_x is not None:
        is_left_spoke = source_x < center_x
        # Use outside edge: left edge for left stack, right edge for right stack
        if is_left_spoke:
            # Left stack: connect from left edge (outside)
            mxGeometry.set("exitX", "0.0")  # Left edge
        else:
            # Right stack: connect from right edge (outside)
            mxGeometry.set("exitX", "1.0")  # Right edge
        mxGeometry.set("exitY", "0.5")  # Vertical center
        mxGeometry.set("exitDx", "0")
        mxGeometry.set("exitDy", "0")
        mxGeometry.set("exitPerimeter", "1")

        # Target (external): connect to bottom center
        mxGeometry.set("entryX", "0.5")  # Horizontal center
        mxGeometry.set("entryY", "1.0")  # Bottom edge
        mxGeometry.set("entryDx", "0")
        mxGeometry.set("entryDy", "0")
        mxGeometry.set("entryPerimeter", "1")

