"""Base utilities and constants for connection modules.

Provides shared functionality used across all connection types.
"""

from gettopology.diagram.config import get_config

# Get global config instance
_config = get_config()

# Shared constants used by all connection modules
VNET_WIDTH = _config.vnet_width
VNET_HEIGHT = _config.vnet_height_base
VNET_MIN_HEIGHT = _config.vnet_min_height

# Routing offsets
ROUTING_WAYPOINT_OFFSET_HORIZONTAL = _config.routing_waypoint_offset_horizontal
ROUTING_WAYPOINT_OFFSET_VERTICAL = _config.routing_waypoint_offset_vertical
ROUTING_WAYPOINT_OFFSET_CLOSE = _config.routing_waypoint_offset_close

