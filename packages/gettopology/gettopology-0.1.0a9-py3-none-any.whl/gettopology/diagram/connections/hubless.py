"""Hubless spoke-to-spoke connection logic for diagram generation.

Handles layout-aware rules for hubless connections:
- Same-side, directly above/below: top/bottom edges
- Same-side, not directly above/below: outer edges
- Different sides: inner-to-inner
"""

import logging
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


def create_hubless_connection(
    root: Element,
    mxGeometry: Element,
    source_x: float,
    target_x: float,
    source_y: float,
    target_y: float,
    source_height: float,
    target_height: float,
    source_name: str,
    target_name: str,
    source_is_left: bool,
    target_is_left: bool,
    source_center_y: float,
    target_center_y: float,
    all_vnet_positions: dict[str, tuple[float, float, float]] | None = None,
    same_hub: bool = False,
) -> None:
    """Create hubless spoke-to-spoke connection with layout-aware rules.

    Rules:
    - Same-side, directly above/below: top/bottom edges (vertical connection)
    - Same-side, not directly above/below: outer edges (left edge for left stack, right edge for right stack)
    - Different sides: inner-to-inner (left spoke right edge to right spoke left edge)

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
        target_name: Target VNet name
        source_is_left: Whether source is on left side
        target_is_left: Whether target is on left side
        source_center_y: Source VNet vertical center Y
        target_center_y: Target VNet vertical center Y
        all_vnet_positions: Dict of all VNet positions for blocking detection
        same_hub: Whether this is a same-hub connection (uses same rules)
    """
    # Track state for waypoint routing
    needs_outer_edge_waypoints = False

    # Check if same side (same X position, within tolerance)
    same_side_tolerance = 1.0  # 1px tolerance for same X
    same_side = abs(source_x - target_x) < same_side_tolerance

    if same_side:
        # Same stack: check if directly above/below
        # Determine which is upper and which is lower
        if source_y < target_y:
            upper_y = source_y
            upper_height = source_height
            lower_y = target_y
        else:
            upper_y = target_y
            upper_height = target_height
            lower_y = source_y

        # Check if there are any VNets between them in Y
        upper_bottom_y = upper_y + upper_height
        lower_top_y = lower_y
        vnets_between = []

        if all_vnet_positions:
            for vnet_name, (v_x, v_y, v_height) in all_vnet_positions.items():
                if vnet_name == source_name or vnet_name == target_name:
                    continue
                # Check if VNet is at same X and between upper and lower
                if abs(v_x - source_x) < same_side_tolerance:
                    v_bottom_y = v_y + v_height
                    # VNet is between if it overlaps the Y range between upper and lower
                    if (v_y >= upper_bottom_y and v_y <= lower_top_y) or \
                       (v_bottom_y >= upper_bottom_y and v_bottom_y <= lower_top_y) or \
                       (v_y <= upper_bottom_y and v_bottom_y >= lower_top_y):
                        vnets_between.append(vnet_name)

        directly_above_below = len(vnets_between) == 0

        if directly_above_below:
            # Vertical connection: top/bottom edges (from center)
            if source_y < target_y:
                # Source is upper: connect from bottom edge center
                source_exit_x = 0.5  # Horizontal center
                source_exit_y = 1.0  # Bottom edge
                # Target is lower: connect to top edge center
                target_entry_x = 0.5  # Horizontal center
                target_entry_y = 0.0  # Top edge
            else:
                # Target is upper: connect from bottom edge center
                target_entry_x = 0.5  # Horizontal center
                target_entry_y = 1.0  # Bottom edge
                # Source is lower: connect to top edge center
                source_exit_x = 0.5  # Horizontal center
                source_exit_y = 0.0  # Top edge
        else:
            # Not directly above/below: use outer side
            needs_outer_edge_waypoints = True
            if source_is_left:
                # Left stack: use left edge (outer)
                source_exit_x = 0.0  # Left edge
                source_exit_y = 0.5  # Vertical center
            else:
                # Right stack: use right edge (outer)
                source_exit_x = 1.0  # Right edge
                source_exit_y = 0.5  # Vertical center

            if target_is_left:
                # Left stack: use left edge (outer)
                target_entry_x = 0.0  # Left edge
                target_entry_y = 0.5  # Vertical center
            else:
                # Right stack: use right edge (outer)
                target_entry_x = 1.0  # Right edge
                target_entry_y = 0.5  # Vertical center
    else:
        # Different sides (left ↔ right): use inner to inner
        if source_is_left:
            # Left spoke: inner side = right edge
            source_exit_x = 1.0  # Right edge (inner)
            source_exit_y = 0.5  # Vertical center
        else:
            # Right spoke: inner side = left edge
            source_exit_x = 0.0  # Left edge (inner)
            source_exit_y = 0.5  # Vertical center

        if target_is_left:
            # Left spoke: inner side = right edge
            target_entry_x = 1.0  # Right edge (inner)
            target_entry_y = 0.5  # Vertical center
        else:
            # Right spoke: inner side = left edge
            target_entry_x = 0.0  # Left edge (inner)
            target_entry_y = 0.5  # Vertical center

    # Set connection points
    mxGeometry.set("exitX", str(source_exit_x))
    if abs(source_exit_x - 0.5) < 0.1:  # Vertical connection
        mxGeometry.set("exitY", str(source_exit_y))
    else:
        mxGeometry.set("exitY", "0.5")  # Side connection
    mxGeometry.set("exitDx", "0")
    mxGeometry.set("exitDy", "0")
    mxGeometry.set("exitPerimeter", "1")

    mxGeometry.set("entryX", str(target_entry_x))
    if abs(target_entry_x - 0.5) < 0.1:  # Vertical connection
        mxGeometry.set("entryY", str(target_entry_y))
    else:
        mxGeometry.set("entryY", "0.5")  # Side connection
    mxGeometry.set("entryDx", "0")
    mxGeometry.set("entryDy", "0")
    mxGeometry.set("entryPerimeter", "1")

    # Add waypoints for outer edge routing (same-side, not directly above/below)
    if needs_outer_edge_waypoints:
        _add_outer_edge_waypoints(
            mxGeometry,
            source_x, target_x,
            source_y, target_y,
            source_height, target_height,
            source_is_left,
            all_vnet_positions
        )


def _add_outer_edge_waypoints(
    mxGeometry: Element,
    source_x: float,
    target_x: float,
    source_y: float,
    target_y: float,
    source_height: float,
    target_height: float,
    source_is_left: bool,
    all_vnet_positions: dict[str, tuple[float, float, float]] | None = None,
) -> None:
    """Add waypoints for outer edge routing when VNets are same-side but not directly above/below.

    Routes around blocking VNets using outer edges.
    """

    # Both VNets are on the same side (same X), so they should both be left or both be right
    is_left_stack = source_is_left

    # Calculate actual connection points on the outer edges
    if is_left_stack:
        source_connection_x = source_x  # Left edge
        target_connection_x = target_x  # Left edge (same X, so same edge)
    else:
        source_connection_x = source_x + VNET_WIDTH  # Right edge
        target_connection_x = target_x + VNET_WIDTH  # Right edge (same X, so same edge)

    # Vertical center Y for both
    source_connection_y = source_y + (source_height / 2)
    target_connection_y = target_y + (target_height / 2)

    # Use blocking detection logic but route to outer edges
    route_h_offset = ROUTING_WAYPOINT_OFFSET_HORIZONTAL
    route_v_offset = ROUTING_WAYPOINT_OFFSET_VERTICAL

    # Find blocking VNet
    blocking_vnet_x = None
    blocking_vnet_y = None
    blocking_vnet_height = None
    blocking_vnet_name = None

    same_side_tolerance = 1.0
    min_y = min(source_y, target_y)
    max_y = max(source_y + source_height, target_y + target_height)

    if all_vnet_positions:
        for vnet_name, (v_x, v_y, v_height) in all_vnet_positions.items():
            # Check if VNet is at same X and between source and target
            if abs(v_x - source_x) < same_side_tolerance:
                v_bottom_y = v_y + v_height
                # VNet is between if it overlaps the Y range
                if (v_y >= min_y and v_y <= max_y) or \
                   (v_bottom_y >= min_y and v_bottom_y <= max_y) or \
                   (v_y <= min_y and v_bottom_y >= max_y):
                    blocking_vnet_x = v_x
                    blocking_vnet_y = v_y
                    blocking_vnet_height = v_height
                    blocking_vnet_name = vnet_name
                    # Blocking VNet detected for outer edge routing
                    break

    # Add waypoints
    array_elem = SubElement(mxGeometry, "Array")
    array_elem.set("as", "points")

    if blocking_vnet_x is not None and blocking_vnet_y is not None and blocking_vnet_height is not None:
        # Route around blocking VNet
        logging.debug(f"Routing around blocking VNet: {blocking_vnet_name}")

        route_above = source_connection_y < blocking_vnet_y and target_connection_y < blocking_vnet_y
        route_below = source_connection_y > (blocking_vnet_y + blocking_vnet_height) and target_connection_y > (blocking_vnet_y + blocking_vnet_height)

        # Waypoint 1: Go outward from source outer edge
        if is_left_stack:
            waypoint1_x = source_connection_x - route_h_offset
        else:
            waypoint1_x = source_connection_x + route_h_offset
        waypoint1_y = source_connection_y

        # Waypoint 2: Stay outward, move vertically around blocking VNet
        if is_left_stack:
            waypoint2_x = source_connection_x - route_h_offset
        else:
            waypoint2_x = source_connection_x + route_h_offset

        if route_above:
            waypoint2_y = blocking_vnet_y - route_v_offset
        elif route_below:
            waypoint2_y = blocking_vnet_y + blocking_vnet_height + route_v_offset
        else:
            # Route through middle: choose the side with more vertical space
            space_above = abs(source_connection_y - blocking_vnet_y) if source_connection_y < blocking_vnet_y else abs(target_connection_y - blocking_vnet_y)
            space_below = abs(source_connection_y - (blocking_vnet_y + blocking_vnet_height)) if source_connection_y > (blocking_vnet_y + blocking_vnet_height) else abs(target_connection_y - (blocking_vnet_y + blocking_vnet_height))
            waypoint2_y = blocking_vnet_y - route_v_offset if space_above > space_below else blocking_vnet_y + blocking_vnet_height + route_v_offset

        # Waypoint 3: Stay outward, move to target's Y level
        if is_left_stack:
            waypoint3_x = source_connection_x - route_h_offset
        else:
            waypoint3_x = source_connection_x + route_h_offset
        waypoint3_y = target_connection_y

        # Waypoint 4: Come back inward to target outer edge
        if is_left_stack:
            waypoint4_x = target_connection_x - route_h_offset
        else:
            waypoint4_x = target_connection_x + route_h_offset
        waypoint4_y = target_connection_y

        create_waypoint(array_elem, waypoint1_x, waypoint1_y)
        create_waypoint(array_elem, waypoint2_x, waypoint2_y)
        create_waypoint(array_elem, waypoint3_x, waypoint3_y)
        create_waypoint(array_elem, waypoint4_x, waypoint4_y)
    else:
        # No blocking VNet: direct connection
        if is_left_stack:
            waypoint1_x = source_connection_x - route_h_offset
            waypoint2_x = target_connection_x - route_h_offset
        else:
            waypoint1_x = source_connection_x + route_h_offset
            waypoint2_x = target_connection_x + route_h_offset

        create_waypoint(array_elem, waypoint1_x, source_connection_y)
        create_waypoint(array_elem, waypoint2_x, target_connection_y)

