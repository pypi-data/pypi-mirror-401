"""Hub-to-hub connection logic for diagram generation."""

from xml.etree.ElementTree import Element, SubElement

from gettopology.diagram.config import get_config
from gettopology.diagram.connections.base import (
    ROUTING_WAYPOINT_OFFSET_CLOSE,
    ROUTING_WAYPOINT_OFFSET_VERTICAL,
    VNET_WIDTH,
)
from gettopology.diagram.elements.edge_elements import create_waypoint

# Get global config instance
_config = get_config()


def _detect_intermediate_hubs(
    source_x: float,
    target_x: float,
    source_name: str,
    target_name: str,
    hub_positions: dict[str, tuple[float, float, float]] | None,
) -> tuple[bool, float | None]:
    """Detect if there are intermediate hubs between source and target.
    
    Returns:
        tuple: (has_intermediate_hubs, max_intermediate_top_y)
    """
    has_intermediate_hubs = False
    max_intermediate_top_y = None
    
    if not hub_positions or not source_name or not target_name:
        return has_intermediate_hubs, max_intermediate_top_y
    
    source_center_x = source_x + (VNET_WIDTH / 2)
    target_center_x = target_x + (VNET_WIDTH / 2)
    min_x = min(source_center_x, target_center_x)
    max_x = max(source_center_x, target_center_x)
    
    # Check if any hub is horizontally between source and target
    # hub_positions stores (x, top_y, height) where x is left edge, top_y is top Y
    for hub_name, (hub_x, hub_y, hub_height) in hub_positions.items():
        if hub_name == source_name or hub_name == target_name:
            continue
        hub_center_x = hub_x + (VNET_WIDTH / 2)
        # Check if hub is between source and target horizontally
        if min_x < hub_center_x < max_x:
            has_intermediate_hubs = True
            # Track the top Y of intermediate hubs (hub_y is already top Y)
            if max_intermediate_top_y is None or hub_y < max_intermediate_top_y:
                max_intermediate_top_y = hub_y  # Lower Y = higher on screen
    
    return has_intermediate_hubs, max_intermediate_top_y


def create_hub_to_hub_connection(
    root: Element,
    mxGeometry: Element,
    source_x: float,
    target_x: float,
    source_y: float,
    target_y: float,
    source_height: float,
    target_height: float,
    hub_positions: dict[str, tuple[float, float, float]] | None = None,
    source_name: str = "",
    target_name: str = "",
) -> None:
    """Create hub-to-hub connection with routing logic for adjacent vs non-adjacent hubs.

    Args:
        root: Root XML element (not used, but kept for consistency)
        mxGeometry: Geometry element to add waypoints to
        source_x: Source hub X position (left edge)
        target_x: Target hub X position (left edge)
        source_y: Source hub center Y position
        target_y: Target hub center Y position
        source_height: Source hub height
        target_height: Target hub height
        hub_positions: Dict of hub positions (hub_name -> (x, y, height)) to detect intermediate hubs
        source_name: Source hub name (for detecting intermediate hubs)
        target_name: Target hub name (for detecting intermediate hubs)
    """
    # Calculate actual top Y positions
    # Note: source_y and target_y are CENTER Y positions (calculated in main_page.py)
    source_top_y = source_y - (source_height / 2)
    target_top_y = target_y - (target_height / 2)
    source_center_x = source_x + (VNET_WIDTH / 2)
    target_center_x = target_x + (VNET_WIDTH / 2)
    
    # Check if there are intermediate hubs between source and target
    has_intermediate_hubs, max_intermediate_top_y = _detect_intermediate_hubs(
        source_x, target_x, source_name, target_name, hub_positions
    )
    
    if has_intermediate_hubs:
        # Non-adjacent hubs: Connect from top middle to top middle, route over the top
        # Exit from top middle of source hub
        mxGeometry.set("exitX", "0.5")  # Horizontal center
        mxGeometry.set("exitY", "0.0")  # Top edge
        mxGeometry.set("exitDx", "0")
        mxGeometry.set("exitDy", "0")
        mxGeometry.set("exitPerimeter", "1")  # Connect to perimeter edge
        
        # Enter at top middle of target hub
        mxGeometry.set("entryX", "0.5")  # Horizontal center
        mxGeometry.set("entryY", "0.0")  # Top edge
        mxGeometry.set("entryDx", "0")
        mxGeometry.set("entryDy", "0")
        mxGeometry.set("entryPerimeter", "1")  # Connect to perimeter edge
        
        # Add waypoints: go up from source top, then horizontally above all intermediate hubs, then down to target top
        array_elem = SubElement(mxGeometry, "Array")
        array_elem.set("as", "points")
        
        # Calculate waypoint Y: above the tallest intermediate hub (or source/target if higher)
        # Use the minimum top Y (highest on screen) among source, target, and intermediate hubs
        min_top_y = min(source_top_y, target_top_y)
        if max_intermediate_top_y is not None:
            min_top_y = min(min_top_y, max_intermediate_top_y)
        
        # Waypoint Y: above the highest hub by the vertical offset (use larger offset for hub-to-hub)
        # Use 2x the offset to ensure clear separation above hubs
        waypoint_y = min_top_y - (ROUTING_WAYPOINT_OFFSET_VERTICAL * 2)
        
        # Waypoint 1: Above source hub top (go up at right angle)
        waypoint1_x = source_center_x
        create_waypoint(array_elem, waypoint1_x, waypoint_y)
        
        # Add intermediate waypoints above each intermediate hub to ensure horizontal routing
        if hub_positions and source_name and target_name:
            min_x = min(source_center_x, target_center_x)
            max_x = max(source_center_x, target_center_x)
            
            # Collect intermediate hubs and sort by X position
            intermediate_hubs = []
            for hub_name, (hub_x, hub_y, hub_height) in hub_positions.items():
                if hub_name == source_name or hub_name == target_name:
                    continue
                hub_center_x = hub_x + (VNET_WIDTH / 2)
                if min_x < hub_center_x < max_x:
                    intermediate_hubs.append((hub_center_x, hub_name))
            
            # Sort by X position to add waypoints in order
            intermediate_hubs.sort(key=lambda x: x[0])
            
            # Add waypoint above each intermediate hub
            for hub_center_x, hub_name in intermediate_hubs:
                create_waypoint(array_elem, hub_center_x, waypoint_y)
        
        # Waypoint 2: Above target hub top (horizontal line, then down)
        waypoint2_x = target_center_x
        create_waypoint(array_elem, waypoint2_x, waypoint_y)
    else:
        # Adjacent hubs: Connect from side middle to side middle with straight horizontal line
        if target_x > source_x:
            # Target is to the right: source connects from right side, target connects to left side
            mxGeometry.set("exitX", "1.0")  # Right side of source
            mxGeometry.set("exitY", "0.5")  # Middle of right side
            mxGeometry.set("entryX", "0.0")  # Left side of target
            mxGeometry.set("entryY", "0.5")  # Middle of left side
        else:
            # Target is to the left: source connects from left side, target connects to right side
            mxGeometry.set("exitX", "0.0")  # Left side of source
            mxGeometry.set("exitY", "0.5")  # Middle of left side
            mxGeometry.set("entryX", "1.0")  # Right side of target
            mxGeometry.set("entryY", "0.5")  # Middle of right side

        mxGeometry.set("exitDx", "0")
        mxGeometry.set("exitDy", "0")
        mxGeometry.set("exitPerimeter", "1")  # Connect to perimeter edge
        mxGeometry.set("entryDx", "0")
        mxGeometry.set("entryDy", "0")
        mxGeometry.set("entryPerimeter", "1")  # Connect to perimeter edge

        # Add waypoints at the same Y level to ensure straight horizontal line
        array_elem = SubElement(mxGeometry, "Array")
        array_elem.set("as", "points")

        # Waypoint at source side (just outside)
        if target_x > source_x:
            waypoint1_x = source_x + VNET_WIDTH + ROUTING_WAYPOINT_OFFSET_CLOSE  # Just outside right edge
        else:
            waypoint1_x = source_x - ROUTING_WAYPOINT_OFFSET_CLOSE  # Just outside left edge
        create_waypoint(array_elem, waypoint1_x, source_y)  # Use center Y

        # Waypoint at target side (just outside)
        if target_x > source_x:
            waypoint2_x = target_x - ROUTING_WAYPOINT_OFFSET_CLOSE  # Just outside left edge
        else:
            waypoint2_x = target_x + VNET_WIDTH + ROUTING_WAYPOINT_OFFSET_CLOSE  # Just outside right edge
        create_waypoint(array_elem, waypoint2_x, target_y)  # Use center Y

