"""Diagram generation for Azure VNet topology using Draw.io XML format."""

from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path
from typing import Any
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring

from gettopology.azure_service import collect_hybrid_connectivity, query_route_table_routes
from gettopology.diagram.categorization import categorize_vnets, group_hubs_with_spokes
from gettopology.diagram.config import get_config
from gettopology.diagram.connections.hub_to_spoke import create_hub_to_spoke_connection
from gettopology.diagram.elements.edge_elements import build_edge_style
from gettopology.diagram.layout import (
    calculate_zone_positions,
)
from gettopology.models import (
    TopologyModel,
)
from gettopology.utils import generate_vnet_markdown

# Get global config instance
_config = get_config()

# Draw.io layout constants (from config)
CANVAS_PADDING = _config.canvas_padding
ZONE_WIDTH = _config.zone_width
ZONE_SPACING = _config.zone_spacing
VNET_WIDTH = _config.vnet_width
VNET_HEIGHT = _config.vnet_height_base
VNET_SPACING_X = _config.vnet_spacing_x
VNET_SPACING_Y = _config.vnet_spacing_y
HUB_Y = _config.hub_y
SPOKE_START_Y = _config.spoke_start_y
SPACING_BELOW_HUB = _config.spacing_below_hub
SPACING_BETWEEN_SPOKES = _config.spacing_between_spokes
SUBNET_PADDING_TOP = _config.subnet_padding_top
SUBNET_HEIGHT = _config.subnet_height
SUBNET_SPACING = _config.subnet_spacing
VNET_MIN_HEIGHT = _config.vnet_min_height
EXTERNAL_SPACING_X = _config.external_spacing_x
EXTERNAL_SPACING_Y = _config.external_spacing_y
STUB_SPACING_X = _config.stub_spacing_x
EDGE_COLOR_HUBLESS_SPOKE = _config.edge_color_hubless_spoke
EDGE_COLOR_CROSS_TENANT = _config.edge_color_cross_tenant

# VNet height calculation is now in vnet_elements module
# Imported above as calculate_vnet_height


# Models and categorization functions are now in separate modules
# Imported above


def _create_peering_edge(
    root: Element,
    cell_id: int,
    source_id: int,
    target_id: int,
    is_local: bool = True,
    source_is_hub: bool = False,
    target_is_hub: bool = False,
    source_x: float | None = None,
    target_x: float | None = None,
    source_y: float | None = None,
    target_y: float | None = None,
    source_height: float | None = None,
    target_height: float | None = None,
    source_name: str = "",
    target_name: str = "",
    hubless_spoke_names: set[str] | None = None,
    hubless_center_name: str | None = None,  # Deprecated: use hubless_group_map and hubless_centers
    hubless_group_map: dict[str, int] | None = None,  # vnet_name -> group_index
    hubless_centers: dict[int, str] | None = None,  # group_index -> center_name
    is_cross_tenant: bool = False,
    hub_positions: dict[str, tuple[float, float, float]] | None = None,
    all_vnet_positions: dict[str, tuple[float, float, float]] | None = None,
    ) -> int:
    """Create a peering connection edge mxCell element.

    Args:
        root: Root element to add the cell to
        cell_id: Starting cell ID (will be incremented)
        source_id: Source VNet cell ID
        target_id: Target VNet cell ID
        is_local: True if local peering (same subscription), False if cross-subscription
        source_is_hub: Whether source VNet is a hub
        target_is_hub: Whether target VNet is a hub

    Returns:
        The cell ID used for this edge
    """
    # Determine edge style based on peering type:
    # - Hub-to-Hub: Dark purple solid (#6A1B9A)
    # - Hub-to-Spoke: Blue solid (#0078D4) for local, Green solid (#28A745) for cross-subscription
    # - Spoke-to-Spoke: Dashed maroon/red (#8B0000) for local, Green solid for cross-subscription
    # - Cross-subscription: Green solid (NOT dashed) (#28A745)
    # - External (horizontal): Green solid with straight line style

    # Check if this is an external connection (external VNet above hub or hubless spoke)
    # Use lenient tolerance (VNET_WIDTH) to catch hubless spoke connections
    is_external_connection = False
    if source_x is not None and target_x is not None and source_y is not None and target_y is not None and source_height is not None and target_height is not None:
        source_center_x = source_x + (VNET_WIDTH / 2)
        target_center_x = target_x + (VNET_WIDTH / 2)
        target_bottom_y = target_y + target_height
        source_top_y = source_y
        # Use lenient tolerance (VNET_WIDTH) to catch hubless spoke connections
        is_external_connection = target_bottom_y < source_top_y and abs(target_center_x - source_center_x) < VNET_WIDTH

    if source_is_hub and target_is_hub:
        # Hub-to-Hub: Check if there are intermediate hubs to determine edge style
        # If intermediate hubs exist, use orthogonalEdgeStyle to respect waypoints
        # Otherwise, use "none" for straight line between adjacent hubs
        from gettopology.diagram.connections.hub_to_hub import _detect_intermediate_hubs
        
        has_intermediate_hubs = False
        if source_x is not None and target_x is not None:
            has_intermediate_hubs, _ = _detect_intermediate_hubs(
                source_x, target_x, source_name, target_name, hub_positions
            )
        
        # Use orthogonalEdgeStyle if intermediate hubs exist (to respect waypoints)
        # Otherwise use "none" for straight line between adjacent hubs
        edge_style_type = "orthogonalEdgeStyle" if has_intermediate_hubs else "none"
        pattern = _config.edge_pattern_hub_to_hub
        edge_style = build_edge_style(_config.color_hub_to_hub, pattern, edge_style_type, _config)
    elif is_external_connection or is_cross_tenant:
        # External (cross-tenant) or cross-tenant connection: Use gray color from config
        if is_external_connection and source_is_hub:
            # External connection from hub: straight vertical line
            edge_style = f"edgeStyle=none;rounded=0;html=1;strokeColor={EDGE_COLOR_CROSS_TENANT};strokeWidth=2;startArrow=block;endArrow=block;"
        else:
            # External from spoke or cross-tenant: use orthogonal routing to avoid overlapping boxes
            edge_style = f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={EDGE_COLOR_CROSS_TENANT};strokeWidth=2;startArrow=block;endArrow=block;"
    elif (source_is_hub or target_is_hub) and not (hubless_spoke_names and (source_name in hubless_spoke_names or target_name in hubless_spoke_names)):
        # Hub-to-Spoke (real hub, not hubless): Blue with configurable pattern
        pattern = _config.edge_pattern_hub_to_spoke
        edge_style = build_edge_style(_config.color_hub_to_spoke, pattern, "orthogonalEdgeStyle", _config)
    elif hubless_spoke_names and (source_name in hubless_spoke_names or target_name in hubless_spoke_names):
        # Spoke-to-Spoke (hubless): Use maroon for same tenant, gray for cross-tenant
        if is_cross_tenant:
            # Cross-tenant hubless spoke connection: gray
            edge_style = f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={EDGE_COLOR_CROSS_TENANT};strokeWidth=2;startArrow=block;endArrow=block;"
        else:
            # Same tenant hubless spoke connection: maroon with configurable pattern
            pattern = _config.edge_pattern_hubless_spoke
            edge_style = build_edge_style(EDGE_COLOR_HUBLESS_SPOKE, pattern, "orthogonalEdgeStyle", _config)
    else:
        # Fallback: Spoke-to-Spoke (hubless): Maroon with configurable pattern
        pattern = _config.edge_pattern_hubless_spoke
        edge_style = build_edge_style(EDGE_COLOR_HUBLESS_SPOKE, pattern, "orthogonalEdgeStyle", _config)

    # Create mxCell for edge
    mxCell = SubElement(root, "mxCell")
    mxCell.set("id", str(cell_id))
    mxCell.set("style", edge_style)
    mxCell.set("edge", "1")
    mxCell.set("parent", "1")
    mxCell.set("source", str(source_id))
    mxCell.set("target", str(target_id))

    # Add geometry with explicit connection points for hub-to-spoke connections
    mxGeometry = SubElement(mxCell, "mxGeometry")
    mxGeometry.set("relative", "1")
    mxGeometry.set("as", "geometry")

    # For Hub-to-Spoke connections: Hub connects from bottom center, Spoke connects to appropriate side
    # For Hub-to-External connections: Hub connects from top middle, External connects to bottom middle
    # Check if this is an external connection first (before checking hub-to-spoke)
    if is_external_connection:
        # Use dedicated module for external connections
        # Ensure all position values are not None before calling
        if source_x is not None and target_x is not None and source_y is not None and target_y is not None and source_height is not None and target_height is not None:
            from gettopology.diagram.connections.external import create_external_connection
            create_external_connection(
                root, mxGeometry,
                source_x, target_x,
                source_y, target_y,
                source_height, target_height,
                source_name, source_is_hub,
                hubless_centers, hubless_group_map,
                hub_positions, all_vnet_positions
            )
    elif not source_is_hub and not target_is_hub and source_x is not None and target_x is not None and source_y is not None and target_y is not None and source_height is not None and target_height is not None and all_vnet_positions:
        # Spoke-to-Spoke connection: Always connect to side centers, route around blocking VNets
        source_center_x = source_x + (VNET_WIDTH / 2)
        source_center_y = source_y + (source_height / 2)
        target_center_x = target_x + (VNET_WIDTH / 2)
        target_center_y = target_y + (target_height / 2)

        # Connection: {source_name} -> {target_name}

        # Determine which side to connect on (inner vs outer) based on hub/center position
        # Inner sides: facing the hub/center (for spokes on same side)
        # Outer sides: facing away from hub/center (for spokes on opposite sides)

        # Find hub/center position for source and target
        source_hub_x = None
        target_hub_x = None

        # Check if source is a hubless spoke (has hubless center)
        if hubless_group_map and hubless_centers:
            source_group = hubless_group_map.get(source_name)
            if source_group is None:
                # Check if source is a center
                for group_idx, center_name in hubless_centers.items():
                    if source_name == center_name:
                        source_group = group_idx
                        break
            if source_group is not None:
                source_center_name: str | None = hubless_centers.get(source_group)
                if source_center_name:
            # Try to find hubless center position from hub_positions or all_vnet_positions
                    if hub_positions and source_center_name in hub_positions:
                        source_hub_x, _, _ = hub_positions[source_center_name]
                    elif all_vnet_positions and source_center_name in all_vnet_positions:
                        source_hub_x, _, _ = all_vnet_positions[source_center_name]
                if source_name == source_center_name:
                    # Source IS the hubless center
                    source_hub_x = source_x
        elif hubless_center_name and hubless_spoke_names and source_name in hubless_spoke_names:
            # Fallback to old logic
            if hub_positions and hubless_center_name in hub_positions:
                source_hub_x, _, _ = hub_positions[hubless_center_name]
            elif all_vnet_positions and hubless_center_name in all_vnet_positions:
                source_hub_x, _, _ = all_vnet_positions[hubless_center_name]
        elif source_name == hubless_center_name:
            # Source IS the hubless center (fallback)
            source_hub_x = source_x

        # Check if target is a hubless spoke (has hubless center)
        if hubless_group_map and hubless_centers:
            target_group = hubless_group_map.get(target_name)
            if target_group is None:
                # Check if target is a center
                for group_idx, center_name in hubless_centers.items():
                    if target_name == center_name:
                        target_group = group_idx
                        break
            if target_group is not None:
                target_center_name: str | None = hubless_centers.get(target_group)
                if target_center_name:
            # Try to find hubless center position from hub_positions or all_vnet_positions
                    if hub_positions and target_center_name in hub_positions:
                        target_hub_x, _, _ = hub_positions[target_center_name]
                    elif all_vnet_positions and target_center_name in all_vnet_positions:
                        target_hub_x, _, _ = all_vnet_positions[target_center_name]
                if target_name == target_center_name:
                    # Target IS the hubless center
                    target_hub_x = target_x
        elif hubless_center_name and hubless_spoke_names and target_name in hubless_spoke_names:
            # Fallback to old logic
            if hub_positions and hubless_center_name in hub_positions:
                target_hub_x, _, _ = hub_positions[hubless_center_name]
            elif all_vnet_positions and hubless_center_name in all_vnet_positions:
                target_hub_x, _, _ = all_vnet_positions[hubless_center_name]
        elif target_name == hubless_center_name:
            # Target IS the hubless center (fallback)
            target_hub_x = target_x

        # For regular hub-spoke, find the hub by checking which hub the spoke peers with
        # Find closest hub (spoke should be near its hub)
        if source_hub_x is None and hub_positions:
            source_center_x = source_x + (VNET_WIDTH / 2)
            min_distance = float('inf')
            for hub_name, (hub_x, _, _) in hub_positions.items():
                hub_center_x = hub_x + (VNET_WIDTH / 2)
                distance = abs(source_center_x - hub_center_x)
                if distance < min_distance:
                    min_distance = distance
                    source_hub_x = hub_x

        if target_hub_x is None and hub_positions:
            target_center_x = target_x + (VNET_WIDTH / 2)
            min_distance = float('inf')
            for hub_name, (hub_x, _, _) in hub_positions.items():
                hub_center_x = hub_x + (VNET_WIDTH / 2)
                distance = abs(target_center_x - hub_center_x)
                if distance < min_distance:
                    min_distance = distance
                    target_hub_x = hub_x

        # Determine if spokes are on same side or opposite sides
        source_is_left = False
        target_is_left = False

        source_center_x = source_x + (VNET_WIDTH / 2)
        target_center_x = target_x + (VNET_WIDTH / 2)

        if source_hub_x is not None:
            source_hub_center_x = source_hub_x + (VNET_WIDTH / 2)
            source_is_left = source_center_x < source_hub_center_x
        else:
            # If we can't find hub, try to infer from position relative to target
            # If source is to the left of target and they're close, source might be left spoke
            if source_center_x < target_center_x and abs(source_center_x - target_center_x) < (VNET_WIDTH * 3):
                source_is_left = True

        if target_hub_x is not None:
            target_hub_center_x = target_hub_x + (VNET_WIDTH / 2)
            target_is_left = target_center_x < target_hub_center_x
        else:
            # If we can't find hub, try to infer from position relative to source
            # If target is to the right of source and they're close, target might be right spoke
            if target_center_x > source_center_x and abs(source_center_x - target_center_x) < (VNET_WIDTH * 3):
                target_is_left = False
            elif target_center_x < source_center_x and abs(source_center_x - target_center_x) < (VNET_WIDTH * 3):
                target_is_left = True

        # Determine connection sides
        # Spoke-to-spoke connections:
        # - Same hub/group: use inner sides (facing hub/center)
        # - Different hub/group: use outer sides (facing away from their hubs, towards each other)
        # Exception: connections to/from central hub/spoke are handled separately

        # Check if this is a hubless spoke connection (both must be in the same hubless group)
        is_hubless_connection = False
        if hubless_group_map and hubless_centers:
            # Check if both VNets are hubless spokes and in the same group
            source_group = hubless_group_map.get(source_name)
            target_group = hubless_group_map.get(target_name)
            # Also check if source or target is a hubless center
            if source_group is None:
                # Check if source is a center
                for group_idx, center_name in hubless_centers.items():
                    if source_name == center_name:
                        source_group = group_idx
                        break
            if target_group is None:
                # Check if target is a center
                for group_idx, center_name in hubless_centers.items():
                    if target_name == center_name:
                        target_group = group_idx
                        break

            if source_group is not None and target_group is not None and source_group == target_group:
                is_hubless_connection = True
        elif hubless_center_name and hubless_spoke_names:
            # Fallback to old logic for backward compatibility
            if (source_name in hubless_spoke_names or source_name == hubless_center_name) and \
               (target_name in hubless_spoke_names or target_name == hubless_center_name):
                is_hubless_connection = True

        # Check if spokes belong to the same hub (for regular hub-spoke groups)
        same_hub = False
        if not is_hubless_connection:
            # Only check same_hub for regular hub-spoke connections
            if source_hub_x is not None and target_hub_x is not None:
                same_hub = (source_hub_x == target_hub_x)
            elif source_hub_x is None and target_hub_x is None:
                # Neither has a hub found - check if they're on opposite sides (left vs right)
                # This suggests they might be in the same hub group but hub detection failed
                # Use a heuristic: if one is clearly left and one is clearly right, and they're close horizontally,
                # they're likely in the same hub group
                if source_is_left != target_is_left:
                    # Opposite sides - check if they're reasonably close (within 3x VNET_WIDTH)
                    horizontal_distance = abs(source_center_x - target_center_x)
                    if horizontal_distance < (VNET_WIDTH * 3):
                        same_hub = True  # Likely same hub group
            else:
                # One has hub_x, the other doesn't - check if they're on opposite sides and close
                if source_is_left != target_is_left:
                    horizontal_distance = abs(source_center_x - target_center_x)
                    if horizontal_distance < (VNET_WIDTH * 3):
                        same_hub = True  # Likely same hub group

        # Check if this is a Central Spoke → Spoke connection (should use Hub → Spoke pattern, not layout-aware rules)
        is_central_spoke_to_spoke = False
        if is_hubless_connection and hubless_centers:
            source_group = hubless_group_map.get(source_name) if hubless_group_map else None
            target_group = hubless_group_map.get(target_name) if hubless_group_map else None

            # Check if source is center
            if source_group is None:
                for group_idx, center_name in hubless_centers.items():
                    if source_name == center_name:
                        source_group = group_idx
                        break

            # Check if target is center
            if target_group is None:
                for group_idx, center_name in hubless_centers.items():
                    if target_name == center_name:
                        target_group = group_idx
                        break

            # If one is center and the other is not, this is Central Spoke → Spoke
            if source_group is not None and target_group is not None and source_group == target_group:
                source_center_name = hubless_centers.get(source_group)
                target_center_name = hubless_centers.get(target_group)
                is_central_spoke_to_spoke = (source_name == source_center_name and target_name != target_center_name) or \
                                           (target_name == target_center_name and source_name != source_center_name)

        # For hubless connections, apply special rules based on layout
        # For regular hub-spoke, use same_hub logic to determine if layout-aware rules apply
        # Layout-aware rules (same-side vertical/outer, cross-side inner-to-inner) apply to:
        # 1. Hubless Spoke ↔ Spoke connections (NOT Central Spoke → Spoke)
        # 2. Same-hub connections (spokes within the same hub group)
        # Central Spoke → Spoke uses Hub → Spoke pattern (handled separately below)
        use_layout_aware_rules = (is_hubless_connection and not is_central_spoke_to_spoke) or same_hub

        # Initialize blocking detection variables (used later regardless of layout-aware rules)
        vnet_in_path = False
        blocking_vnet_x = None
        blocking_vnet_y = None
        blocking_vnet_height = None
        blocking_vnet_name = None

        if use_layout_aware_rules:
            # LAYOUT-AWARE CONNECTION LOGIC (applies to hubless and same-hub connections)
            # Use dedicated module for hubless/same-hub connections
            from gettopology.diagram.connections.hubless import create_hubless_connection

            connection_type = "HUBLESS" if is_hubless_connection else "SAME-HUB"
            logging.debug(f"Connection {source_name} -> {target_name}: {connection_type} (layout-aware)")

            create_hubless_connection(
                root, mxGeometry,
                source_x, target_x,
                source_y, target_y,
                source_height, target_height,
                source_name, target_name,
                source_is_left, target_is_left,
                source_center_y, target_center_y,
                all_vnet_positions,
                same_hub
            )

            # Connection points and waypoints are set by create_hubless_connection
            # Skip blocking detection and waypoint routing for layout-aware connections
        else:
            # Different hub/group: use outer sides (facing away from their hubs, towards each other)
            # Determine which outer sides face each other
            if target_x < source_x:
                # Target is to the left: source connects from left side (outer), target connects to right side (outer)
                source_exit_x = 0.0  # Left edge (outer)
                target_entry_x = 1.0  # Right edge (outer)
            else:
                # Target is to the right: source connects from right side (outer), target connects to left side (outer)
                source_exit_x = 1.0  # Right edge (outer)
                target_entry_x = 0.0  # Left edge (outer)

            # Set connection points for different-hub connections
            mxGeometry.set("exitX", str(source_exit_x))
            mxGeometry.set("exitY", "0.5")  # Side connection: use 0.5 for vertical center
            mxGeometry.set("exitDx", "0")
            mxGeometry.set("exitDy", "0")
            mxGeometry.set("exitPerimeter", "1")

            mxGeometry.set("entryX", str(target_entry_x))
            mxGeometry.set("entryY", "0.5")  # Side connection: use 0.5 for vertical center
            mxGeometry.set("entryDx", "0")
            mxGeometry.set("entryDy", "0")
            mxGeometry.set("entryPerimeter", "1")

            # Blocking detection: Only for different-hub connections
            # Layout-aware connections (hubless and same-hub) follow specific rules
            # (same-side vertical/outer, different-side inner-to-inner) so blocking detection is not needed
            # Note: vnet_in_path and blocking variables are already initialized above

            if not use_layout_aware_rules:
                # Only check for blocking VNets for different-hub connections

                # Calculate bounding box between source and target
                min_x = min(source_x, target_x)
                max_x = max(source_x + VNET_WIDTH, target_x + VNET_WIDTH)
                min_y = min(source_y, target_y)
                max_y = max(source_y + source_height, target_y + target_height)

                for vnet_name, (v_x, v_y, v_height) in all_vnet_positions.items():
                    # Skip source and target VNets
                    if vnet_name == source_name or vnet_name == target_name:
                        continue

                    vnet_left_edge = v_x
                    vnet_right_edge = v_x + VNET_WIDTH
                    vnet_top_y = v_y
                    vnet_bottom_y = v_y + v_height

                    # Check if VNet overlaps the bounding box between source and target
                    vnet_overlaps_horizontally = not (vnet_right_edge <= min_x or vnet_left_edge >= max_x)
                    vnet_overlaps_vertically = not (vnet_bottom_y <= min_y or vnet_top_y >= max_y)

                    if vnet_overlaps_horizontally and vnet_overlaps_vertically:
                        vnet_in_path = True
                        blocking_vnet_x = v_x
                        blocking_vnet_y = v_y
                        blocking_vnet_height = v_height
                        blocking_vnet_name = vnet_name
                        # Blocking VNet detected - routing will go around it
                        break

        # Calculate actual connection points (side centers)
        if target_x < source_x:
            # Target is to the left: source connects from left side, target connects to right side
            source_connection_x = source_x  # Left edge
            target_connection_x = target_x + VNET_WIDTH  # Right edge
        else:
            # Target is to the right: source connects from right side, target connects to left side
            source_connection_x = source_x + VNET_WIDTH  # Right edge
            target_connection_x = target_x  # Left edge

        source_connection_y = source_center_y  # Side center Y
        target_connection_y = target_center_y  # Side center Y

        if vnet_in_path and blocking_vnet_x is not None and blocking_vnet_y is not None and blocking_vnet_height is not None:
            logging.debug(f"Routing around blocking VNet: {blocking_vnet_name} for {source_name} -> {target_name}")
            # Route around blocking VNet: determine best path (left or right, above or below)
            source_left_edge = source_x
            source_right_edge = source_x + VNET_WIDTH
            blocking_left_edge = blocking_vnet_x
            blocking_right_edge = blocking_vnet_x + VNET_WIDTH
            target_left_edge = target_x
            target_right_edge = target_x + VNET_WIDTH

            # Calculate space on left and right sides
            space_left = min(abs(source_left_edge - blocking_right_edge), abs(target_left_edge - blocking_right_edge)) if source_x < blocking_vnet_x or target_x < blocking_vnet_x else min(abs(blocking_left_edge - source_right_edge), abs(blocking_left_edge - target_right_edge))
            space_right = min(abs(source_right_edge - blocking_left_edge), abs(target_right_edge - blocking_left_edge)) if source_x > blocking_vnet_x or target_x > blocking_vnet_x else min(abs(blocking_right_edge - source_left_edge), abs(blocking_right_edge - target_left_edge))

            # Determine if we should route above or below blocking VNet
            route_above = source_connection_y < blocking_vnet_y and target_connection_y < blocking_vnet_y
            route_below = source_connection_y > (blocking_vnet_y + blocking_vnet_height) and target_connection_y > (blocking_vnet_y + blocking_vnet_height)

            # Default: route around the side with more space
            route_h_offset = _config.routing_waypoint_offset_horizontal
            route_v_offset = _config.routing_waypoint_offset_vertical

            # Add waypoints
            array_elem = SubElement(mxGeometry, "Array")
            array_elem.set("as", "points")

            if space_left > space_right:
                # Route left: go left from source side, then up/down around blocking VNet, then right to target side
                waypoint1_x = source_connection_x - route_h_offset  # Go left from source side
                waypoint1_y = source_connection_y  # Same Y as source side center

                if route_above:
                    waypoint2_y = blocking_vnet_y - route_v_offset  # Above blocking VNet
                elif route_below:
                    waypoint2_y = blocking_vnet_y + blocking_vnet_height + route_v_offset  # Below blocking VNet
                else:
                    # Route through middle: choose the side with more vertical space
                    space_above = abs(source_connection_y - blocking_vnet_y) if source_connection_y < blocking_vnet_y else abs(target_connection_y - blocking_vnet_y)
                    space_below = abs(source_connection_y - (blocking_vnet_y + blocking_vnet_height)) if source_connection_y > (blocking_vnet_y + blocking_vnet_height) else abs(target_connection_y - (blocking_vnet_y + blocking_vnet_height))
                    waypoint2_y = blocking_vnet_y - route_v_offset if space_above > space_below else blocking_vnet_y + blocking_vnet_height + route_v_offset

                waypoint2_x = min(source_x, target_x) - route_h_offset  # Stay left
                waypoint3_x = waypoint2_x  # Stay left
                waypoint3_y = waypoint2_y  # Stay at blocking VNet level
                waypoint4_x = target_connection_x - route_h_offset  # Approach target from left
                waypoint4_y = target_connection_y  # Same Y as target side center
            else:
                # Route right: go right from source side, then up/down around blocking VNet, then left to target side
                waypoint1_x = source_connection_x + route_h_offset  # Go right from source side
                waypoint1_y = source_connection_y  # Same Y as source side center

                if route_above:
                    waypoint2_y = blocking_vnet_y - route_v_offset  # Above blocking VNet
                elif route_below:
                    waypoint2_y = blocking_vnet_y + blocking_vnet_height + route_v_offset  # Below blocking VNet
                else:
                    # Route through middle: choose the side with more vertical space
                    space_above = abs(source_connection_y - blocking_vnet_y) if source_connection_y < blocking_vnet_y else abs(target_connection_y - blocking_vnet_y)
                    space_below = abs(source_connection_y - (blocking_vnet_y + blocking_vnet_height)) if source_connection_y > (blocking_vnet_y + blocking_vnet_height) else abs(target_connection_y - (blocking_vnet_y + blocking_vnet_height))
                    waypoint2_y = blocking_vnet_y - route_v_offset if space_above > space_below else blocking_vnet_y + blocking_vnet_height + route_v_offset

                waypoint2_x = max(source_x, target_x) + VNET_WIDTH + route_h_offset  # Stay right
                waypoint3_x = waypoint2_x  # Stay right
                waypoint3_y = waypoint2_y  # Stay at blocking VNet level
                waypoint4_x = target_connection_x + route_h_offset  # Approach target from right
                waypoint4_y = target_connection_y  # Same Y as target side center

            waypoint1 = SubElement(array_elem, "mxPoint")
            waypoint1.set("x", str(waypoint1_x))
            waypoint1.set("y", str(waypoint1_y))

            waypoint2 = SubElement(array_elem, "mxPoint")
            waypoint2.set("x", str(waypoint2_x))
            waypoint2.set("y", str(waypoint2_y))

            waypoint3 = SubElement(array_elem, "mxPoint")
            waypoint3.set("x", str(waypoint3_x))
            waypoint3.set("y", str(waypoint3_y))

            waypoint4 = SubElement(array_elem, "mxPoint")
            waypoint4.set("x", str(waypoint4_x))
            waypoint4.set("y", str(waypoint4_y))
        else:
            # No blocking VNet: direct connection with waypoints to ensure clean routing
            route_h_offset = _config.routing_waypoint_offset_horizontal

            array_elem = SubElement(mxGeometry, "Array")
            array_elem.set("as", "points")

            # Waypoint 1: Just outside source side
            waypoint1_x = source_connection_x + (route_h_offset if target_x > source_x else -route_h_offset)
            waypoint1_y = source_connection_y

            # Waypoint 2: Just outside target side (at same Y level if horizontal, or adjust if vertical)
            waypoint2_x = target_connection_x + (-route_h_offset if target_x > source_x else route_h_offset)
            waypoint2_y = target_connection_y

            waypoint1 = SubElement(array_elem, "mxPoint")
            waypoint1.set("x", str(waypoint1_x))
            waypoint1.set("y", str(waypoint1_y))

            waypoint2 = SubElement(array_elem, "mxPoint")
            waypoint2.set("x", str(waypoint2_x))
            waypoint2.set("y", str(waypoint2_y))
    elif source_is_hub and target_is_hub and source_x is not None and target_x is not None and source_y is not None and target_y is not None and source_height is not None and target_height is not None:
        # Hub-to-Hub: Use dedicated module
        from gettopology.diagram.connections.hub_to_hub import create_hub_to_hub_connection
        create_hub_to_hub_connection(
            root, mxGeometry,
            source_x, target_x,
            source_y, target_y,
            source_height, target_height,
            hub_positions,  # Pass hub positions to detect intermediate hubs
            source_name,  # Pass source name
            target_name  # Pass target name
        )
    # Check if source is a hubless center
    is_source_hubless_center = False
    if hubless_centers:
        is_source_hubless_center = source_name in hubless_centers.values()

    # Check if target is a hubless center (for Spoke → Central Spoke - should not use Hub → Spoke pattern)
    is_target_hubless_center = False
    if hubless_centers:
        is_target_hubless_center = target_name in hubless_centers.values()

    # Hub → Spoke OR Central Spoke → Spoke: Hub/center connects from bottom center to spoke side middle
    if (source_is_hub or is_source_hubless_center) and not target_is_hub and not is_target_hubless_center and source_x is not None and target_x is not None and source_y is not None and target_y is not None and source_height is not None:
        # Regular hub or hubless spoke center: Use dedicated module
        create_hub_to_spoke_connection(
            root, mxGeometry,
            source_x, target_x,
            source_y, target_y,
            source_height, target_height
        )

    return cell_id


def generate_hld_diagram(
    topology: TopologyModel,
    output_dir: str,
    hybrid_data: dict[str, Any] | None = None,
) -> str:
    """Generate High-Level Diagram (HLD) in Draw.io XML format.

    HLD shows:
    - VNet name
    - Address space
    - Subscription name / Resource group
    - Peering connections between VNets

    Layout:
    - Hubs at the top (or center)
    - Hub spokes below hubs
    - Hubless spokes below hub spokes
    - Stubs at the bottom

    Args:
        topology: TopologyModel containing all virtual networks
        output_dir: Output directory path (will create hld/ subdirectory)

    Returns:
        str: Path to the generated Draw.io file
    """
    if not topology.virtual_networks:
        logging.warning("No virtual networks to diagram")
        return

    # Categorize VNets
    categories = categorize_vnets(topology)

    # Group hubs with their spokes
    hub_spoke_groups, hubless_groups, stubs = group_hubs_with_spokes(categories)

    # Create Draw.io XML structure
    mxfile = Element("mxfile")
    mxfile.set("host", "app.diagrams.net")
    mxfile.set("modified", "2024-01-01T00:00:00.000Z")
    mxfile.set("agent", "gettopology")
    mxfile.set("version", "22.1.0")
    mxfile.set("etag", "dummy")
    mxfile.set("type", "device")

    # Legend will be created after calculating all positions to avoid overlaps
    cell_id_counter = _config.cell_id_start
    legend_x = _config.legend_x

    # Create mapping of VNet names to main cell IDs (for edge connections)
    vnet_name_to_main_id: dict[str, int] = {}
    # Create mapping of VNet names to tenant IDs (for cross-tenant detection)
    vnet_name_to_tenant_id: dict[str, str] = {vnet.name: vnet.tenant_id for vnet in topology.virtual_networks}
    # Track which VNets are hubs (for edge styling)
    hub_names: set[str] = {vnet.name for vnet in categories.hubs}
    # Track which VNets are hubless spokes (for edge styling - to distinguish from hub-spoke)
    # Flatten all hubless groups into a single set
    hubless_spoke_names: set[str] = {vnet.name for group in hubless_groups for vnet in group}
    # Track the center VNet for each hubless group (acts as hub for connection purposes)
    # Map: group_index -> center_name
    hubless_centers: dict[int, str] = {}
    # Track which hubless group each VNet belongs to: vnet_name -> group_index
    hubless_group_map: dict[str, int] = {}
    for group_index, group in enumerate(hubless_groups):
        # Find center (most connected VNet in this group)
        center_vnet = max(group, key=lambda v: v.peering_count)
        hubless_centers[group_index] = center_vnet.name
        # Map all VNets in this group to the group index
        for vnet in group:
            hubless_group_map[vnet.name] = group_index
    # Track hub positions for hub-to-hub connections
    hub_name_to_position: dict[str, tuple[float, float, float]] = {}  # (x, y, height)
    # Track hubless spoke positions for external VNet connections
    hubless_spoke_positions: dict[str, tuple[float, float, float]] = {}  # (x, y, height)
    # Track regular spoke positions for external VNet connections
    regular_spoke_positions: dict[str, tuple[float, float, float]] = {}  # (x, y, height)
    # Track all VNet positions (hubs + regular spokes + hubless spokes) for overlap detection
    all_vnet_positions: dict[str, tuple[float, float, float]] = {}  # (x, y, height)
    # cell_id_counter already initialized above for legend creation

    # Store edge information to create after all VNets (for proper z-ordering)
    # Format: (source_id, target_id, is_local, source_is_hub, target_is_hub, source_x, target_x, source_y, target_y, source_height, target_height, source_name, target_name, is_cross_tenant)
    edges_to_create: list[tuple[int, int, bool, bool, bool, float | None, float | None, float | None, float | None, float | None, float | None, str, str, bool]] = []
    created_edges: set[tuple[int, int]] = set()  # Track to avoid duplicates

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
        """Helper to add edge to list only if it doesn't already exist (bidirectional check)."""
        edge_key: tuple[int, int] = tuple(sorted([source_id, target_id]))  # type: ignore[arg-type]
        if edge_key not in created_edges:
            # For hubless spokes, the center VNet should be treated as a hub for connection purposes
            # Check if source is a hubless center (acts as hub for connections)
            is_hubless_center = False
            if hubless_centers:
                is_hubless_center = source_name in hubless_centers.values()
            source_is_hub = (source_name in hub_names and source_name not in hubless_spoke_names) or is_hubless_center
            target_is_hub = target_name in hub_names and target_name not in hubless_spoke_names
            # Check if this is cross-tenant: different tenant_id or external VNet (not in vnet_name_to_tenant_id)
            source_tenant_id = vnet_name_to_tenant_id.get(source_name)
            target_tenant_id = vnet_name_to_tenant_id.get(target_name)
            is_cross_tenant = (source_tenant_id is not None and target_tenant_id is not None and source_tenant_id != target_tenant_id) or (target_name not in vnet_name_to_tenant_id)  # External VNet is cross-tenant
            edges_to_create.append((source_id, target_id, is_local, source_is_hub, target_is_hub, source_x, target_x, source_y, target_y, source_height, target_height, source_name, target_name, is_cross_tenant))
            created_edges.add(edge_key)

    # Determine primary subscription ID (first hub's subscription)
    primary_subscription_id = hub_spoke_groups[0].hub.subscription_id if hub_spoke_groups else None

    # Calculate zone positions using layout module (separates hub-spoke from hubless)
    zones, hubless_zones = calculate_zone_positions(hub_spoke_groups, hubless_groups)

    # Create main page only if there are zones (hub-spoke groups)
    # (External VNets are determined inside create_main_page, but they typically only exist
    # when there are zones/spokes to connect to, so checking zones is sufficient)
    if zones:
        # Create main page diagram structure
        diagram = SubElement(mxfile, "diagram")
        diagram.set("id", "topology-hld")
        diagram.set("name", "Azure VNet Topology - HLD")

        mxGraphModel = SubElement(diagram, "mxGraphModel")
        mxGraphModel.set("dx", str(_config.drawio_page_dx))
        mxGraphModel.set("dy", str(_config.drawio_page_dy))
        mxGraphModel.set("grid", "1")
        mxGraphModel.set("gridSize", str(_config.drawio_grid_size))
        mxGraphModel.set("guides", "1")
        mxGraphModel.set("tooltips", "1")
        mxGraphModel.set("connect", "1")
        mxGraphModel.set("arrows", "1")
        mxGraphModel.set("fold", "1")
        mxGraphModel.set("page", "1")
        mxGraphModel.set("pageWidth", str(_config.page_width))
        mxGraphModel.set("pageHeight", str(_config.page_height))
        mxGraphModel.set("math", "0")
        mxGraphModel.set("shadow", "0")

        root = SubElement(mxGraphModel, "root")

        # Add mxCell for root
        root_cell = SubElement(root, "mxCell")
        root_cell.set("id", "0")

        root_cell_layer = SubElement(root, "mxCell")
        root_cell_layer.set("id", "1")
        root_cell_layer.set("parent", "0")

        # Create main page content
        from gettopology.diagram.pages.main_page import create_main_page
        (
            cell_id_counter,
            vnet_name_to_main_id,
            hub_name_to_position,
            regular_spoke_positions,
            hubless_spoke_positions,
            all_vnet_positions,
            edges_to_create,
        ) = create_main_page(
            root, topology, zones, primary_subscription_id, hubless_spoke_names, stubs,
            hub_names, vnet_name_to_tenant_id, hubless_group_map, hubless_centers,
            cell_id_counter, legend_x, _create_peering_edge
        )

        # Create all edges from edges_to_create list
        for edge_data in edges_to_create:
            if len(edge_data) == 14:
                source_id, target_id, is_local, source_is_hub, target_is_hub, source_x, target_x, source_y, target_y, source_height, target_height, source_name, target_name, is_cross_tenant = edge_data  # type: ignore[misc]
            elif len(edge_data) == 13:
                # Backward compatibility: old format without is_cross_tenant
                source_id, target_id, is_local, source_is_hub, target_is_hub, source_x, target_x, source_y, target_y, source_height, target_height, source_name, target_name = edge_data  # type: ignore[misc]
                # Check tenant_id if available
                source_tenant_id = vnet_name_to_tenant_id.get(source_name)
                target_tenant_id = vnet_name_to_tenant_id.get(target_name)
                is_cross_tenant = (source_tenant_id is not None and target_tenant_id is not None and source_tenant_id != target_tenant_id) or (target_name not in vnet_name_to_tenant_id)
            else:
                # Backward compatibility: old format without names
                source_id, target_id, is_local, source_is_hub, target_is_hub, source_x, target_x, source_y, target_y, source_height, target_height = edge_data  # type: ignore[misc]
                source_name = ""
                target_name = ""
                is_cross_tenant = False
            _create_peering_edge(
                root, cell_id_counter, source_id, target_id, is_local,
                source_is_hub, target_is_hub, source_x, target_x, source_y, target_y,
                source_height, target_height, source_name, target_name,
                hubless_spoke_names, None, hubless_group_map, hubless_centers,
                is_cross_tenant, hub_name_to_position, all_vnet_positions
            )
            cell_id_counter += 1

    # Create second page for hubless spokes if they exist
    from gettopology.diagram.pages.hubless_page import create_hubless_page
    create_hubless_page(
        mxfile, hubless_groups, primary_subscription_id, hubless_spoke_names,
        _create_peering_edge, _config.cell_id_start
    )

    # Create third page for orphan/stub VNets if they exist
    from gettopology.diagram.pages.orphan_page import create_orphan_page
    create_orphan_page(mxfile, stubs, _config.cell_id_start)

    # Create fourth page for hybrid connectivity if connections exist
    if hybrid_data:
        try:
            # Check if we have any VPN or ExpressRoute connections (not VNet-to-VNet)
            hybrid_connections = [
                conn for conn in hybrid_data['connections']
                if conn.connection_type in ["IPsec", "ExpressRoute"] and conn.local_network_gateway_id
            ]
            if hybrid_connections:
                from gettopology.diagram.pages.hybrid_page import create_hybrid_page
                create_hybrid_page(mxfile, topology, hybrid_data, primary_subscription_id, _config.cell_id_start)
        except Exception as e:
            # If hybrid connectivity page generation fails, log but don't fail entire diagram generation
            logging.warning(f"Failed to generate hybrid connectivity page: {e}")

    # Create hld subdirectory
    hld_dir = Path(output_dir) / "hld"
    hld_dir.mkdir(parents=True, exist_ok=True)

    # Write to hld subdirectory
    xml_str = minidom.parseString(tostring(mxfile)).toprettyxml(indent="  ")
    hld_file_path = hld_dir / "topology-hld.drawio"
    with open(hld_file_path, "w", encoding="utf-8") as f:
        f.write(xml_str)

    logging.info(f"HLD diagram saved to {hld_file_path}")
    return str(hld_file_path)


def generate_lld_diagram(topology: TopologyModel, output_path: str) -> None:
    """Generate Low-Level Diagram (LLD) in Draw.io XML format.

    LLD shows all HLD details plus:
    - Subnets
    - Subnet address ranges
    - Private endpoints
    - NSG associations
    - Route table associations
    - Subnet delegations

    Args:
        topology: TopologyModel containing all virtual networks
        output_path: Path to save the Draw.io XML file
    """
    # TODO: Implement LLD generation
    logging.info("LLD diagram generation not yet implemented")
    pass

def generate_markmap_diagram(
    topology: TopologyModel,
    output_path: str,
    subscription_ids: list[str] | None = None,
    credential: Any = None,
    route_table_routes: dict[str, list[dict]] | None = None,
    ) -> None:
    """Generate markmap diagram for VNets and add as new page to Draw.io file.

    This function is only called when -vnet flag is used.
    It generates markdown for each VNet, queries route table routes if needed,
    calls markmap CLI to generate HTML, and adds it as a new page to the Draw.io file.

    Args:
        topology: TopologyModel containing all virtual networks
        output_path: Output directory path
        subscription_ids: Optional list of subscription IDs for route table queries
        credential: Optional Azure credential for route table queries
        route_table_routes: Optional pre-populated route table routes dict (for synthetic data)
    """
    if not topology.virtual_networks:
        logging.warning("No virtual networks for markmap diagram")
        return

    # Collect route table IDs from all subnets
    route_table_ids = []
    for vnet in topology.virtual_networks:
        for subnet in vnet.subnets:
            if subnet.route_table_id and subnet.route_table_id not in route_table_ids:
                route_table_ids.append(subnet.route_table_id)

    # Query route table routes if we have route tables and credentials (unless already provided)
    if route_table_routes is None:
        if route_table_ids and subscription_ids and credential:
            logging.info(f"Querying route table routes for {len(route_table_ids)} route table(s)...")
            route_table_routes = query_route_table_routes(route_table_ids, subscription_ids, credential)

    # Create vnet subdirectory for HTML files
    vnet_dir = Path(output_path) / "vnet"
    vnet_dir.mkdir(parents=True, exist_ok=True)

    # Generate separate markdown and HTML files for each VNet
    import platform

    # Check if running in Azure Cloud Shell
    def is_azure_cloud_shell() -> bool:
        """Check if running in Azure Cloud Shell."""
        azureps_env = os.getenv("AZUREPS_HOST_ENVIRONMENT", "")
        return "cloud-shell" in azureps_env.lower()

    # Determine markmap command based on environment
    if is_azure_cloud_shell():
        # Azure Cloud Shell doesn't allow global npm installs, use npx
        markmap_cmd = ["npx", "markmap"]
        logging.info("Azure Cloud Shell detected, using 'npx markmap'")
    else:
        # Use global markmap installation
        markmap_cmd = ["markmap.cmd"] if platform.system() == "Windows" else ["markmap"]

    generated_files = []
    for vnet in topology.virtual_networks:
        # Generate markdown for this VNet
        vnet_markdown = generate_vnet_markdown(vnet, route_table_routes)

        # Write individual markdown file for this VNet (temporary, will be deleted)
        safe_vnet_name = vnet.name.replace(" ", "_").replace("/", "_")
        markdown_path = Path(output_path) / f"{safe_vnet_name}-markmap.md"
        markdown_path.write_text(vnet_markdown, encoding="utf-8")
        # logging.info(f"Markdown generated: {markdown_path}")

        html_generated = False
        # Write HTML to vnet subdirectory
        html_path = vnet_dir / f"{safe_vnet_name}-markmap.html"

        # Try to generate HTML using markmap CLI
        try:
            # Check if markmap-cli is available (skip version check for npx in Cloud Shell)
            if is_azure_cloud_shell():
                # In Cloud Shell, npx will download if needed, so skip version check
                check_result = None
            else:
                # Check version for global install (timeout is non-critical - actual generation will work)
                try:
                    check_result = subprocess.run(
                        markmap_cmd + ["--version"],
                        capture_output=True,
                        text=True,
                        timeout=10,
                        shell=False,
                    )
                except subprocess.TimeoutExpired:
                    # Version check timed out, but proceed anyway - actual generation will wor
                    logging.info("Version check timed out, but proceeding anyway")
                    check_result = None

            if check_result is None or check_result.returncode == 0:
                # Generate HTML for this VNet (--no-open prevents auto-opening in browser)
                try:
                    subprocess.run(
                        markmap_cmd + [str(markdown_path), "-o", str(html_path), "--no-open"],
                        check=True,
                        timeout=60 if is_azure_cloud_shell() else 30,  # Longer timeout for npx download
                        shell=False,
                        capture_output=True,
                        text=True,
                    )
                    logging.info(f"Markmap HTML generated: {html_path}")
                    generated_files.append(str(html_path))
                    html_generated = True
                except subprocess.CalledProcessError as e:
                    error_msg = e.stderr or e.stdout or str(e)
                    if is_azure_cloud_shell():
                        logging.warning(
                            f"Could not generate markmap HTML for {vnet.name} in Azure Cloud Shell. "
                            f"Error: {error_msg}. "
                            f"Ensure markmap-cli is installed locally: npm install markmap-cli"
                        )
                    else:
                        logging.warning(f"Could not generate markmap HTML for {vnet.name}: {error_msg}")
            else:
                if is_azure_cloud_shell():
                    logging.warning("Could not run 'npx markmap' in Azure Cloud Shell")
                else:
                    logging.warning("markmap CLI not found. Install with: npm install -g markmap-cli")
        except FileNotFoundError:
            # Try alternative command formats on Windows as fallback (only for non-Cloud Shell)
            if not is_azure_cloud_shell() and platform.system() == "Windows":
                # Try markmap without .cmd extension (might be in PATH differently)
                fallback_cmd = ["markmap"]
                try:
                    subprocess.run(
                        fallback_cmd + [str(markdown_path), "-o", str(html_path), "--no-open"],
                        check=True,
                        timeout=30,
                        shell=False,
                        capture_output=True,
                        text=True,
                    )
                    logging.info(f"Markmap HTML generated: {html_path}")
                    generated_files.append(str(html_path))
                    html_generated = True
                except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError) as e:
                    logging.warning(f"Could not generate markmap HTML for {vnet.name}: {e}")
            else:
                if is_azure_cloud_shell():
                    logging.warning("Could not run 'npx markmap' in Azure Cloud Shell. Ensure npm is available.")
                else:
                    logging.warning("markmap CLI not found. Install with: npm install -g markmap-cli")
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            logging.warning(f"Could not generate markmap HTML for {vnet.name}: {e}")

        # Delete markdown file if HTML was successfully generated
        if html_generated and markdown_path.exists():
            try:
                markdown_path.unlink()
                logging.debug(f"Deleted markdown file: {markdown_path}")
            except OSError as e:
                logging.warning(f"Could not delete markdown file {markdown_path}: {e}")


def generate_index_html(output_dir: str, hld_file_path: str) -> None:
    """Generate index.html with embedded Draw.io and VNet markmap links.

    Args:
        output_dir: Output directory path
        hld_file_path: Path to the HLD Draw.io file
    """
    import json
    import xml.etree.ElementTree as ET
    from defusedxml.ElementTree import parse as safe_parse

    output_path = Path(output_dir)
    hld_path = Path(hld_file_path)
    vnet_dir = output_path / "vnet"

    # Parse Draw.io XML to extract all pages
    if not hld_path.exists():
        logging.warning(f"HLD file not found: {hld_path}. Skipping index.html generation.")
        return

    tree = safe_parse(hld_path)
    root = tree.getroot()
    diagrams = root.findall('diagram')

    # Extract each page's XML
    pages = []
    for diagram in diagrams:
        page_id = diagram.get('id', 'unknown')
        page_name = diagram.get('name', 'Unnamed Page')
        # Create temporary mxfile with just this diagram
        temp_root = ET.Element('mxfile')
        temp_root.set('host', root.get('host', 'app.diagrams.net'))
        temp_root.set('modified', root.get('modified', ''))
        temp_root.set('agent', root.get('agent', 'gettopology'))
        temp_root.set('version', root.get('version', '22.1.0'))
        temp_root.set('etag', root.get('etag', 'dummy'))
        temp_root.set('type', root.get('type', 'device'))
        temp_root.append(diagram)
        page_xml = ET.tostring(temp_root, encoding='unicode')
        pages.append({
            'id': page_id,
            'name': page_name,
            'xml': page_xml
        })

    # Find all markmap HTML files
    markmap_files = sorted(vnet_dir.glob("*-markmap.html")) if vnet_dir.exists() else []
    vnets = []
    for html_file in markmap_files:
        vnet_name = html_file.stem.replace("-markmap", "").replace("_", " ")
        # Use relative path from index.html location
        vnets.append({
            "name": vnet_name,
            "file": f"vnet/{html_file.name}"
        })

    # Generate HTML content (using the same template from featuretest)
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Azure VNet Topology Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            color: #333;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            background: linear-gradient(135deg, #0078D4 0%, #005a9e 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .nav-tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 2px solid #ddd;
        }}

        .nav-tab {{
            padding: 12px 24px;
            background: #e0e0e0;
            border: none;
            cursor: pointer;
            font-size: 16px;
            border-radius: 8px 8px 0 0;
            transition: all 0.3s;
        }}

        .nav-tab:hover {{
            background: #d0d0d0;
        }}

        .nav-tab.active {{
            background: #0078D4;
            color: white;
        }}

        .content-section {{
            display: none;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}

        .content-section.active {{
            display: block;
        }}

        .vnet-list {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}

        .vnet-item {{
            background: #f9f9f9;
            border: 2px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            cursor: pointer;
            transition: all 0.3s;
        }}

        .vnet-item:hover {{
            border-color: #0078D4;
            background: #e6f1fb;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}

        .vnet-item.active {{
            border-color: #0078D4;
            background: #cce4f7;
        }}

        .vnet-name {{
            font-weight: bold;
            color: #0078D4;
            margin-bottom: 5px;
        }}

        .markmap-container {{
            margin-top: 30px;
            border: 2px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
            display: none;
        }}

        .markmap-container.active {{
            display: block;
        }}

        .markmap-container iframe {{
            width: 100%;
            height: 800px;
            border: none;
        }}

        .drawio-container {{
            margin-top: 20px;
            border: 1px solid transparent;
            border-radius: 8px;
            overflow: hidden;
            min-height: 600px;
        }}

        .section-title {{
            font-size: 1.5em;
            color: #0078D4;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
        }}

        .info-text {{
            color: #666;
            margin-bottom: 20px;
            font-style: italic;
        }}

        .page-tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }}

        .page-tab {{
            padding: 10px 20px;
            background: #e0e0e0;
            border: none;
            cursor: pointer;
            font-size: 14px;
            border-radius: 6px;
            transition: all 0.3s;
        }}

        .page-tab:hover {{
            background: #d0d0d0;
        }}

        .page-tab.active {{
            background: #0078D4;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Azure VNet Topology Dashboard</h1>
            <p>Interactive visualization of your Azure Virtual Network topology</p>
        </header>

        <div class="nav-tabs">
            <button class="nav-tab active" onclick="showSection('topology')">Topology Diagram</button>
            <button class="nav-tab" onclick="showSection('vnets')">VNet Details</button>
        </div>

        <!-- Topology Section -->
        <div id="topology-section" class="content-section active">
            <h2 class="section-title">High-Level Topology Diagram</h2>
            <p class="info-text">Interactive Draw.io diagram showing all VNets, peerings, and connections</p>
            <!-- Page tabs for multiple Draw.io pages -->
            <div class="page-tabs" id="page-tabs">
                <!-- Page tabs will be inserted here -->
            </div>
            <div class="drawio-container" id="drawio-container">
                <p style="padding: 20px; color: #666;">Loading diagram...</p>
            </div>
        </div>

        <!-- VNets Section -->
        <div id="vnets-section" class="content-section">
            <h2 class="section-title">Virtual Network Details</h2>
            <p class="info-text">Click on a VNet to view its detailed markmap visualization</p>
            <div class="vnet-list" id="vnet-list">
                <!-- VNet items will be inserted here -->
            </div>
            <div class="markmap-container" id="markmap-container">
                <iframe id="markmap-iframe" src=""></iframe>
            </div>
        </div>
    </div>

    <script>
        // Embedded Draw.io pages (no fetch needed - works with file:// protocol)
        const drawioPages = {json.dumps(pages)};

        // VNet list
        const vnets = {json.dumps(vnets)};

        let currentPageIndex = 0;

        // Populate page tabs
        function populatePageTabs() {{
            const pageTabs = document.getElementById('page-tabs');
            if (!pageTabs || drawioPages.length <= 1) {{
                if (pageTabs) pageTabs.style.display = 'none';
                return;
            }}

            pageTabs.innerHTML = '';
            drawioPages.forEach((page, index) => {{
                const tab = document.createElement('button');
                tab.className = 'page-tab' + (index === 0 ? ' active' : '');
                tab.textContent = page.name;
                tab.onclick = () => switchPage(index, tab);
                pageTabs.appendChild(tab);
            }});
        }}

        // Switch between Draw.io pages
        function switchPage(index, tabElement) {{
            if (index === currentPageIndex) return;

            // Update tab active state
            document.querySelectorAll('#page-tabs .page-tab').forEach(t => t.classList.remove('active'));
            tabElement.classList.add('active');

            currentPageIndex = index;
            const page = drawioPages[index];
            loadDrawioDiagram(page.xml, page.id);
        }}

        // Load Draw.io diagram
        function loadDrawioDiagram(pageXml, pageId) {{
            const drawioContainer = document.getElementById('drawio-container');

            if (!pageXml || pageXml.trim() === '') {{
                drawioContainer.innerHTML =
                    '<p style="color: red; padding: 20px;">Draw.io diagram not available.</p>';
                return;
            }}

            try {{
                // Clear container completely (this removes any existing viewer instances)
                drawioContainer.innerHTML = '';

                // Create the embed configuration
                const config = {{
                    highlight: '#0000ff',
                    nav: true,
                    resize: true,
                    'dark-mode': 'light',
                    toolbar: 'zoom layers tags lightbox',
                    edit: '_blank',
                    xml: pageXml
                }};

                // Create the embed div with unique ID
                const embedDiv = document.createElement('div');
                embedDiv.id = 'drawio-diagram-' + (pageId || 'default');
                embedDiv.className = 'mxgraph';
                embedDiv.style.cssText = 'max-width:100%;border:1px solid transparent;min-height:600px;';
                embedDiv.setAttribute('data-mxgraph', JSON.stringify(config));

                drawioContainer.appendChild(embedDiv);

                // Function to process the diagram
                function processDiagram() {{
                    // Try multiple ways to access the viewer
                    let viewer = null;
                    if (typeof mxGraphViewer !== 'undefined') {{
                        viewer = mxGraphViewer;
                    }} else if (window.mxGraphViewer) {{
                        viewer = window.mxGraphViewer;
                    }} else if (typeof GraphViewer !== 'undefined') {{
                        viewer = GraphViewer;
                    }} else if (window.GraphViewer) {{
                        viewer = window.GraphViewer;
                    }}

                    if (viewer && typeof viewer.processElements === 'function') {{
                        try {{
                            // Process all mxgraph elements (should only be one now)
                            viewer.processElements();
                        }} catch (e) {{
                            console.error('Error processing diagram:', e);
                            // Try to manually process just our element
                            const element = document.getElementById(embedDiv.id);
                            if (element) {{
                                try {{
                                    const data = JSON.parse(element.getAttribute('data-mxgraph'));
                                    // Try different viewer methods
                                    if (viewer.createViewerForElement) {{
                                        viewer.createViewerForElement(element, data);
                                    }} else if (viewer.processElement) {{
                                        viewer.processElement(element);
                                    }}
                                }} catch (err) {{
                                    console.error('Error processing element:', err);
                                }}
                            }}
                        }}
                    }} else {{
                        // Wait a bit and try again (max 15 attempts = 1.5 seconds)
                        if (typeof processDiagram.attempts === 'undefined') {{
                            processDiagram.attempts = 0;
                        }}
                        processDiagram.attempts++;
                        if (processDiagram.attempts < 15) {{
                            setTimeout(processDiagram, 100);
                        }} else {{
                            console.error('Draw.io viewer not available after multiple attempts');
                            drawioContainer.innerHTML =
                                '<p style="color: orange; padding: 20px;">⚠️ Unable to load Draw.io diagram.</p>' +
                                '<p style="color: #666; padding: 0 20px 20px;">Please refresh the page or open <a href="hld/topology-hld.drawio" target="_blank">hld/topology-hld.drawio</a> directly in Draw.io.</p>';
                        }}
                    }}
                }}

                // Load the viewer script if not already loaded
                const existingScript = document.querySelector('script[src*="viewer-static.min.js"]');
                if (!existingScript) {{
                    const script = document.createElement('script');
                    script.type = 'text/javascript';
                    script.src = 'https://viewer.diagrams.net/js/viewer-static.min.js';
                    script.onload = function() {{
                        // Wait a bit for viewer to initialize, then process
                        setTimeout(processDiagram, 300);
                    }};
                    script.onerror = () => {{
                        drawioContainer.innerHTML =
                            '<p style="color: orange; padding: 20px;">⚠️ Draw.io viewer requires internet connection.</p>' +
                            '<p style="color: #666; padding: 0 20px 20px;">For offline use, open <a href="hld/topology-hld.drawio" target="_blank">hld/topology-hld.drawio</a> directly in Draw.io.</p>';
                    }};
                    document.body.appendChild(script);
                }} else {{
                    // Script already loaded, wait a bit for DOM to be ready, then process
                    // Use a longer delay to ensure previous diagram is fully cleared
                    setTimeout(processDiagram, 150);
                }}
            }} catch (error) {{
                console.error('Error embedding diagram:', error);
                drawioContainer.innerHTML =
                    '<p style="color: red; padding: 20px;">Error processing Draw.io diagram.</p>' +
                    '<p style="color: #666; padding: 0 20px 20px;">You can open it directly: <a href="hld/topology-hld.drawio" target="_blank">hld/topology-hld.drawio</a></p>';
            }}
        }}

        // Populate VNet list
        function populateVnetList() {{
            const vnetList = document.getElementById('vnet-list');
            vnetList.innerHTML = '';

            vnets.forEach(vnet => {{
                const item = document.createElement('div');
                item.className = 'vnet-item';
                item.innerHTML = `<div class="vnet-name">${{vnet.name}}</div>`;
                item.onclick = () => showMarkmap(vnet.file, item);
                vnetList.appendChild(item);
            }});
        }}

        // Show markmap for selected VNet
        function showMarkmap(file, item) {{
            // Remove active class from all items
            document.querySelectorAll('.vnet-item').forEach(i => i.classList.remove('active'));

            // Add active class to clicked item
            item.classList.add('active');

            // Show markmap container and load iframe
            const container = document.getElementById('markmap-container');
            const iframe = document.getElementById('markmap-iframe');
            iframe.src = file;
            container.classList.add('active');

            // Scroll to markmap
            container.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
        }}

        // Show section based on tab
        function showSection(section) {{
            // Hide all sections
            document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));

            // Remove active class from all tabs
            document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));

            // Show selected section
            document.getElementById(section + '-section').classList.add('active');

            // Add active class to clicked tab
            event.target.classList.add('active');
        }}

        // Initialize on page load
        window.onload = function() {{
            populatePageTabs();
            if (drawioPages.length > 0) {{
                const firstPage = drawioPages[0];
                loadDrawioDiagram(firstPage.xml, firstPage.id);
            }}
            populateVnetList();
        }};
    </script>
</body>
</html>"""

    index_path = output_path / "index.html"
    index_path.write_text(html_content, encoding="utf-8")
    logging.info(f"Index page generated: {index_path}")

    if vnets:
        logging.info(f"Index page includes {len(vnets)} VNet markmap link(s)")


def hybrid_connection_diagram(
    topology: TopologyModel,
    output_dir: str,
    subscription_ids: list[str],
    credential: Any,
    hybrid_data: dict[str, Any] | None = None,
) -> None:
    """Generate hybrid connection diagram for the topology (Phase 1: Data Collection).

    Collects and displays hybrid connectivity information including:
    - VPN and ExpressRoute connections
    - Local Network Gateways (on-premises)
    - Correlation with VNets and Virtual Network Gateways

    Args:
        topology: TopologyModel containing VNets and gateways
        output_dir: Output directory path
        subscription_ids: List of subscription IDs to search in
        credential: Azure credential object
    """
    logging.info("Generating hybrid connection diagram...")

    # Collect hybrid connectivity data if not provided
    if hybrid_data is None:
        hybrid_data = collect_hybrid_connectivity(topology, subscription_ids, credential)

    connections = hybrid_data['connections']
    local_network_gateways = hybrid_data['local_network_gateways']
    vnet_to_connections = hybrid_data['vnet_to_connections']
    gateway_to_connections = hybrid_data['gateway_to_connections']
    connection_to_local_gateway = hybrid_data['connection_to_local_gateway']
    connection_to_peer_gateway = hybrid_data['connection_to_peer_gateway']

    # Print summary
    print("\n" + "=" * 80)
    print("HYBRID CONNECTIVITY SUMMARY")
    print("=" * 80)
    print(f"\nTotal Connections: {len(connections)}")
    print(f"Total Local Network Gateways: {len(local_network_gateways)}")
    print(f"VNets with Connections: {len(vnet_to_connections)}")

    # Print connections by VNet
    if vnet_to_connections:
        print("\n" + "-" * 80)
        print("CONNECTIONS BY VNET")
        print("-" * 80)
        for vnet_name, vnet_connections in sorted(vnet_to_connections.items()):
            # Find VNet details
            vnet = next((v for v in topology.virtual_networks if v.name == vnet_name), None)
            if vnet:
                print(f"\nVNet: {vnet_name}")
                print(f"  Subscription: {vnet.subscription_name or vnet.subscription_id}")
                print(f"  Resource Group: {vnet.resource_group_name}")
                print(f"  Region: {vnet.location}")
                print(f"  Connections: {len(vnet_connections)}")
                for conn in vnet_connections:
                    print(f"\n    Connection: {conn.name}")
                    print(f"      Type: {conn.connection_type}")
                    print(f"      Status: {conn.connection_status or 'Unknown'}")
                    print(f"      Resource Group: {conn.resource_group_name}")
                    print(f"      Region: {conn.location}")
                    
                    # Connection protocol (for VPN)
                    if conn.connection_protocol:
                        print(f"      Protocol: {conn.connection_protocol}")
                    
                    # Connection mode
                    if conn.connection_mode:
                        print(f"      Mode: {conn.connection_mode}")
                    
                    # Authentication type
                    if conn.authentication_type:
                        print(f"      Authentication: {conn.authentication_type}")
                    
                    # BGP
                    if conn.enable_bgp:
                        print(f"      BGP: Enabled")
                    
                    # Routing method
                    if conn.use_policy_based_traffic_selectors:
                        print(f"      Routing: Policy-based")
                    else:
                        print(f"      Routing: Route-based")
                    
                    # Routing weight
                    if conn.routing_weight is not None:
                        print(f"      Routing Weight: {conn.routing_weight}")
                    
                    # IPsec policies (for VPN)
                    if conn.ipsec_policies:
                        print(f"      IPsec Policies: {len(conn.ipsec_policies)} policy/policies")
                        for idx, policy in enumerate(conn.ipsec_policies, 1):
                            print(f"        Policy {idx}:")
                            if policy.get('ipsecEncryption'):
                                print(f"          Encryption: {policy.get('ipsecEncryption')}")
                            if policy.get('ipsecIntegrity'):
                                print(f"          Integrity: {policy.get('ipsecIntegrity')}")
                            if policy.get('ikeEncryption'):
                                print(f"          IKE Encryption: {policy.get('ikeEncryption')}")
                            if policy.get('ikeIntegrity'):
                                print(f"          IKE Integrity: {policy.get('ikeIntegrity')}")
                            if policy.get('pfsGroup'):
                                print(f"          PFS Group: {policy.get('pfsGroup')}")
                            if policy.get('dhGroup'):
                                print(f"          DH Group: {policy.get('dhGroup')}")
                    
                    # Traffic statistics
                    if conn.ingress_bytes_transferred is not None or conn.egress_bytes_transferred is not None:
                        ingress_gb = (conn.ingress_bytes_transferred or 0) / (1024**3)
                        egress_gb = (conn.egress_bytes_transferred or 0) / (1024**3)
                        print(f"      Traffic: Ingress {ingress_gb:.2f} GB, Egress {egress_gb:.2f} GB")

                    # Show local network gateway (for S2S VPN)
                    if conn.local_network_gateway_id:
                        local_gw = connection_to_local_gateway.get(conn.resource_id)
                        if local_gw:
                            print(f"      Local Network Gateway: {local_gw.name}")
                            if local_gw.fqdn:
                                print(f"        FQDN: {local_gw.fqdn}")
                            if local_gw.gateway_ip_address:
                                print(f"        On-Prem IP: {local_gw.gateway_ip_address}")
                            if local_gw.address_prefixes:
                                print(f"        On-Prem Prefixes: {', '.join(local_gw.address_prefixes)}")
                            else:
                                print(f"        On-Prem Prefixes: None (BGP routing)")
                            if local_gw.bgp_settings:
                                bgp_peering = local_gw.bgp_settings.get('bgpPeeringAddress', 'N/A')
                                asn = local_gw.bgp_settings.get('asn', 'N/A')
                                print(f"        BGP: ASN {asn}, Peering {bgp_peering}")

                    # Show peer (for ExpressRoute or VNet-to-VNet)
                    if conn.peer_id:
                        # Check if it's an ExpressRoute Circuit or another gateway
                        if 'expressRouteCircuits' in conn.peer_id.lower():
                            circuit_name = conn.peer_id.split('/')[-1]
                            print(f"      ExpressRoute Circuit: {circuit_name}")
                        elif 'virtualNetworkGateways' in conn.peer_id.lower():
                            # VNet-to-VNet connection
                            peer_gw = connection_to_peer_gateway.get(conn.resource_id)
                            if peer_gw:
                                peer_gw_name = peer_gw.get('name', 'Unknown')
                                print(f"      Peer Gateway: {peer_gw_name} (VNet-to-VNet)")
                            else:
                                peer_name = conn.peer_id.split('/')[-1]
                                print(f"      Peer Gateway: {peer_name} (VNet-to-VNet)")
                        else:
                            # Unknown peer type
                            peer_name = conn.peer_id.split('/')[-1]
                            print(f"      Peer: {peer_name}")

    # Print local network gateways
    if local_network_gateways:
        print("\n" + "-" * 80)
        print("LOCAL NETWORK GATEWAYS (On-Premises)")
        print("-" * 80)
        for lng in local_network_gateways:
            print(f"\n  Name: {lng.name}")
            print(f"    Subscription: {lng.subscription_id}")
            print(f"    Resource Group: {lng.resource_group_name}")
            print(f"    Region: {lng.location}")
            
            # Provisioning state
            if lng.provisioning_state:
                state_icon = "✓" if lng.provisioning_state == "Succeeded" else "✗"
                print(f"    State: {state_icon} {lng.provisioning_state}")
            
            # Gateway IP or FQDN
            if lng.fqdn:
                print(f"    FQDN: {lng.fqdn}")
            if lng.gateway_ip_address:
                print(f"    Gateway IP: {lng.gateway_ip_address}")
            
            # Address prefixes (may be empty if BGP is used)
            if lng.address_prefixes:
                print(f"    Address Prefixes: {', '.join(lng.address_prefixes)}")
            else:
                print(f"    Address Prefixes: None (BGP routing)")
            
            # BGP settings
            if lng.bgp_settings:
                bgp_peering = lng.bgp_settings.get('bgpPeeringAddress', 'N/A')
                asn = lng.bgp_settings.get('asn', 'N/A')
                peer_weight = lng.bgp_settings.get('peerWeight', 'N/A')
                print(f"    BGP Settings:")
                print(f"      BGP Peering Address: {bgp_peering}")
                print(f"      ASN: {asn}")
                print(f"      Peer Weight: {peer_weight}")

    # Print connections without VNet correlation (orphaned)
    vnet_connection_ids = {conn.resource_id for conns in vnet_to_connections.values() for conn in conns}
    orphaned_connections = [conn for conn in connections if conn.resource_id not in vnet_connection_ids]
    if orphaned_connections:
        print("\n" + "-" * 80)
        print(f"ORPHANED CONNECTIONS (not correlated with VNets): {len(orphaned_connections)}")
        print("-" * 80)
        for conn in orphaned_connections:
            print(f"  {conn.name} ({conn.connection_type}) - Gateway ID: {conn.virtual_network_gateway_id}")

    print("\n" + "=" * 80)
    logging.info("Hybrid connectivity data collection completed")
