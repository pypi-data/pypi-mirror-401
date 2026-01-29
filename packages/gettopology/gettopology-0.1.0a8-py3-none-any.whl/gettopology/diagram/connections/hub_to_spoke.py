"""Hub-to-spoke and central spoke-to-spoke connection logic for diagram generation."""

from xml.etree.ElementTree import Element, SubElement

from gettopology.diagram.config import get_config
from gettopology.diagram.connections.base import VNET_HEIGHT, VNET_WIDTH
from gettopology.diagram.elements.edge_elements import create_waypoint

# Get global config instance
_config = get_config()


def create_hub_to_spoke_connection(
    root: Element,
    mxGeometry: Element,
    source_x: float,
    target_x: float,
    source_y: float,
    target_y: float,
    source_height: float,
    target_height: float | None = None,
) -> None:
    """Create hub-to-spoke or central spoke-to-spoke connection.

    Hub/center connects from bottom center to spoke side middle.
    This applies to:
    - Regular Hub → Spoke connections
    - Central Spoke → Spoke connections (hubless groups)

    Args:
        root: Root XML element (not used, but kept for consistency)
        mxGeometry: Geometry element to add waypoints to
        source_x: Source hub/center X position (left edge)
        target_x: Target spoke X position (left edge)
        source_y: Source hub/center Y position (top edge)
        target_y: Target spoke Y position (top edge)
        source_height: Source hub/center height
        target_height: Target spoke height (optional, uses default if None)
    """
    # Hub/center connects from bottom center to spoke side middle
    mxGeometry.set("exitX", "0.5")  # Horizontal center
    mxGeometry.set("exitY", "1.0")  # Bottom edge
    mxGeometry.set("exitDx", "0")
    mxGeometry.set("exitDy", "0")
    mxGeometry.set("exitPerimeter", "0")  # Connect to center, not perimeter

    # Spoke entry point: determine based on position
    # If target is to the left of source, connect to right side of spoke (x=1.0)
    # If target is to the right of source, connect to left side of spoke (x=0.0)
    if target_x < source_x:
        # Left spoke: connect to right side (inner side facing hub)
        entry_x = "1.0"
    else:
        # Right spoke: connect to left side (inner side facing hub)
        entry_x = "0.0"

    mxGeometry.set("entryX", entry_x)
    mxGeometry.set("entryY", "0.5")  # Middle of side (vertical center)
    mxGeometry.set("entryDx", "0")
    mxGeometry.set("entryDy", "0")
    mxGeometry.set("entryPerimeter", "0")  # 0 = connect to perimeter edge, not center

    # Add waypoints to force routing: from hub bottom center, go down, then horizontally to spoke side
    # Calculate waypoint positions to guide the edge to connect to the side middle
    if source_x is None or target_x is None or source_y is None or target_y is None or source_height is None:
        # Missing coordinates - skip waypoints, let Draw.io auto-route
        return

    source_y + source_height
    hub_center_x = source_x + (VNET_WIDTH / 2)

    # Calculate spoke's vertical center (middle of the side where connection should be)
    spoke_height = target_height if target_height is not None else VNET_HEIGHT
    spoke_center_y = target_y + (spoke_height / 2)

    # First waypoint: directly below hub bottom center, at spoke's vertical center Y
    # This creates a clean vertical drop from hub bottom, then horizontal to spoke
    waypoint1_x = hub_center_x
    waypoint1_y = spoke_center_y

    # Second waypoint: just outside the spoke's side edge (inner side), at the vertical center
    # This ensures connection at the side middle without weird extensions
    waypoint_offset = 5  # 5px outside the box
    if target_x < source_x:
        # Left spoke: waypoint just outside right side (inner side facing hub)
        waypoint2_x = target_x + VNET_WIDTH + waypoint_offset
    else:
        # Right spoke: waypoint just outside left side (inner side facing hub)
        waypoint2_x = target_x - waypoint_offset
    waypoint2_y = spoke_center_y  # Same Y as spoke center to ensure connection at side middle

    # Add waypoints as Array element
    array_elem = SubElement(mxGeometry, "Array")
    array_elem.set("as", "points")

    create_waypoint(array_elem, waypoint1_x, waypoint1_y)
    create_waypoint(array_elem, waypoint2_x, waypoint2_y)

