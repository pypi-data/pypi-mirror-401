"""Configuration loading and management for diagram generation."""

import logging
from pathlib import Path
from typing import Any

import yaml


class DiagramConfig:
    """Centralized configuration for diagram generation.

    Loads configuration from diagram_config.yaml and provides typed access
    to all configuration values with sensible defaults.
    """

    def __init__(self, config_path: Path | None = None):
        """Initialize configuration from YAML file.

        Args:
            config_path: Path to config file. If None, uses default location.
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "diagram_config.yaml"

        try:
            with open(config_path, encoding="utf-8") as f:
                config = yaml.safe_load(f)
            self._layout = config.get("layout", {})
        except (FileNotFoundError, yaml.YAMLError) as e:
            logging.warning(f"Could not load diagram config from {config_path}: {e}. Using defaults.")
            self._layout = {}

    def _get(self, key: str, default: Any) -> Any:
        """Get config value with default."""
        return self._layout.get(key, default)

    def _get_nested(self, *keys: str, default: Any) -> Any:
        """Get nested config value with default.

        Args:
            *keys: Path to nested value (e.g., "icon", "vnet_size")
            default: Default value if not found

        Returns:
            Config value or default
        """
        value = self._layout
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default
        return value if value is not None else default

    # Canvas settings
    @property
    def canvas_padding(self) -> int:
        return int(self._get("canvas_padding", 20))

    @property
    def page_width(self) -> int:
        return int(self._get("page_width", 1169))

    @property
    def page_height(self) -> int:
        return int(self._get("page_height", 827))

    # Zone settings
    @property
    def zone_width(self) -> int:
        return int(self._get("zone_width", 920))

    @property
    def zone_spacing(self) -> int:
        return int(self._get("zone_spacing", 200))

    # VNet box dimensions
    @property
    def vnet_width(self) -> int:
        return int(self._get("vnet_width", 400))

    @property
    def vnet_height_base(self) -> int:
        return int(self._get("vnet_height_base", 50))

    @property
    def vnet_min_height(self) -> int:
        return int(self._get("vnet_min_height", 70))

    # Spacing constants
    @property
    def vnet_spacing_x(self) -> int:
        return int(self._get("vnet_spacing_x", 300))

    @property
    def vnet_spacing_y(self) -> int:
        return int(self._get("vnet_spacing_y", 100))

    @property
    def hub_y(self) -> int:
        return int(self._get("hub_y", 200))

    @property
    def spoke_start_y(self) -> int:
        return int(self._get("spoke_start_y", 300))

    @property
    def spacing_below_hub(self) -> int:
        return int(self._get("spacing_below_hub", 50))

    @property
    def spacing_between_spokes(self) -> int:
        return int(self._get("spacing_between_spokes", 20))

    # Subnet layout
    @property
    def subnet_padding_top(self) -> int:
        return int(self._get("subnet_padding_top", 75))

    @property
    def subnet_height(self) -> int:
        return int(self._get("subnet_height", 30))

    @property
    def subnet_spacing(self) -> int:
        return int(self._get("subnet_spacing", 5))

    @property
    def subnet_padding_left(self) -> int:
        return int(self._get_nested("subnet", "padding_left", default=5))

    @property
    def subnet_width_offset(self) -> int:
        return int(self._get_nested("subnet", "width_offset", default=10))

    @property
    def subnet_padding_bottom(self) -> int:
        return int(self._get_nested("subnet", "padding_bottom", default=10))

    # External VNet positioning
    @property
    def external_spacing_x(self) -> int:
        return int(self._get("external_spacing_x", 50))

    @property
    def external_spacing_y(self) -> int:
        return int(self._get("external_spacing_y", 100))

    @property
    def stub_spacing_x(self) -> int:
        return int(self._get("stub_spacing_x", 100))

    # Icon settings
    @property
    def icon_vnet_size(self) -> int:
        return int(self._get_nested("icon", "vnet_size", default=20))

    @property
    def icon_subnet_size(self) -> int:
        return int(self._get_nested("icon", "subnet_size", default=20))

    @property
    def icon_subnet_height(self) -> int:
        return int(self._get_nested("icon", "subnet_height", default=12))

    @property
    def icon_spacing(self) -> int:
        return int(self._get_nested("icon", "icon_spacing", default=5))

    @property
    def icon_margin_right(self) -> int:
        return int(self._get_nested("icon", "icon_margin_right", default=6))

    # Icon image paths
    @property
    def icon_vnet(self) -> str:
        return str(self._get_nested("icon", "vnet", default="img/lib/azure2/networking/Virtual_Networks.svg"))

    @property
    def icon_subnet(self) -> str:
        return str(self._get_nested("icon", "subnet", default="img/lib/azure2/networking/Subnet.svg"))

    @property
    def icon_route_table(self) -> str:
        return str(self._get_nested("icon", "route_table", default="img/lib/azure2/networking/Route_Tables.svg"))

    @property
    def icon_nsg(self) -> str:
        return str(self._get_nested("icon", "nsg", default="img/lib/azure2/networking/Network_Security_Groups.svg"))

    @property
    def icon_firewall(self) -> str:
        return str(self._get_nested("icon", "firewall", default="img/lib/azure2/networking/Firewalls.svg"))

    @property
    def icon_bastion(self) -> str:
        return str(self._get_nested("icon", "bastion", default="img/lib/azure2/networking/Bastions.svg"))

    @property
    def icon_vpn_gateway(self) -> str:
        return str(self._get_nested("icon", "vpn_gateway", default="img/lib/mscae/VPN_Gateway.svg"))

    @property
    def icon_expressroute(self) -> str:
        return str(self._get_nested("icon", "expressroute", default="img/lib/azure2/networking/ExpressRoute_Circuits.svg"))

    @property
    def icon_router_vpn(self) -> str:
        return str(self._get_nested("icon", "router_vpn", default="img/lib/allied_telesis/security/Router_VPN.svg"))

    @property
    def icon_router_expressroute(self) -> str:
        return str(self._get_nested("icon", "router_expressroute", default="img/lib/active_directory/shadowed_router.svg"))

    @property
    def icon_nat(self) -> str:
        return str(self._get_nested("icon", "nat", default="img/lib/azure2/networking/NAT.svg"))

    @property
    def icon_private_endpoint(self) -> str:
        return str(self._get_nested("icon", "private_endpoint", default="img/lib/azure2/other/Private_Endpoints.svg"))

    @property
    def icon_ddos(self) -> str:
        return str(self._get_nested("icon", "ddos", default="img/lib/azure2/networking/DDoS_Protection_Plans.svg"))

    # Routing/waypoint settings
    @property
    def routing_waypoint_offset_horizontal(self) -> int:
        return int(self._get_nested("routing", "waypoint_offset_horizontal", default=50))

    @property
    def routing_waypoint_offset_vertical(self) -> int:
        return int(self._get_nested("routing", "waypoint_offset_vertical", default=20))

    @property
    def routing_waypoint_offset_close(self) -> int:
        return int(self._get_nested("routing", "waypoint_offset_close", default=5))

    @property
    def routing_clearance(self) -> int:
        return int(self._get_nested("routing", "route_clearance", default=20))

    # Style colors
    @property
    def color_hub_stroke(self) -> str:
        return str(self._get_nested("colors", "hub_stroke", default="#0078D4"))

    @property
    def color_hub_fill(self) -> str:
        return str(self._get_nested("colors", "hub_fill", default="#E6F1FB"))

    @property
    def color_hub_font(self) -> str:
        return str(self._get_nested("colors", "hub_font", default="#004578"))

    @property
    def color_spoke_stroke(self) -> str:
        return str(self._get_nested("colors", "spoke_stroke", default="#CC6600"))

    @property
    def color_spoke_fill(self) -> str:
        return str(self._get_nested("colors", "spoke_fill", default="#f2f7fc"))

    @property
    def color_spoke_font(self) -> str:
        return str(self._get_nested("colors", "spoke_font", default="#CC6600"))

    @property
    def color_external_stroke(self) -> str:
        return str(self._get_nested("colors", "external_stroke", default="#6C757D"))

    @property
    def color_external_fill(self) -> str:
        return str(self._get_nested("colors", "external_fill", default="#F8F9FA"))

    @property
    def color_external_font(self) -> str:
        return str(self._get_nested("colors", "external_font", default="#495057"))

    @property
    def color_stub_stroke(self) -> str:
        return str(self._get_nested("colors", "stub_stroke", default="#20B2AA"))

    @property
    def color_stub_fill(self) -> str:
        return str(self._get_nested("colors", "stub_fill", default="#E0F7F5"))

    @property
    def color_stub_font(self) -> str:
        return str(self._get_nested("colors", "stub_font", default="#006666"))

    @property
    def color_subnet_stroke(self) -> str:
        return str(self._get_nested("colors", "subnet_stroke", default="#C8C6C4"))

    @property
    def color_subnet_fill(self) -> str:
        return str(self._get_nested("colors", "subnet_fill", default="#FAF9F8"))

    @property
    def color_subnet_font(self) -> str:
        return str(self._get_nested("colors", "subnet_font", default="#323130"))

    @property
    def color_hub_to_hub(self) -> str:
        return str(self._get_nested("colors", "hub_to_hub", default="#6A1B9A"))

    @property
    def color_hub_to_spoke(self) -> str:
        return str(self._get_nested("colors", "hub_to_spoke", default="#0078D4"))

    # Edge colors (from existing config)
    @property
    def edge_color_hubless_spoke(self) -> str:
        return str(self._get("edge_color_hubless_spoke", "#8B0000"))

    @property
    def edge_color_cross_tenant(self) -> str:
        return str(self._get("edge_color_cross_tenant", "#808080"))

    # Edge line patterns
    @property
    def edge_pattern_hub_to_hub(self) -> str:
        return str(self._get_nested("edge_patterns", "hub_to_hub", default="solid"))

    @property
    def edge_pattern_hub_to_spoke(self) -> str:
        return str(self._get_nested("edge_patterns", "hub_to_spoke", default="solid"))

    @property
    def edge_pattern_hubless_spoke(self) -> str:
        return str(self._get_nested("edge_patterns", "hubless_spoke", default="dashed"))

    @property
    def edge_pattern_cross_tenant(self) -> str:
        return str(self._get_nested("edge_patterns", "cross_tenant", default="solid"))

    @property
    def edge_pattern_external(self) -> str:
        return str(self._get_nested("edge_patterns", "external", default="solid"))

    @property
    def edge_dash_pattern(self) -> str:
        return str(self._get_nested("edge_patterns", "dash_pattern", default="8 8"))

    # Legend settings
    @property
    def legend_width(self) -> int:
        return int(self._get("legend_width", 250))

    @property
    def legend_height(self) -> int:
        return int(self._get("legend_height", 600))

    @property
    def legend_padding(self) -> int:
        return int(self._get("legend_padding", 15))

    @property
    def legend_item_spacing(self) -> int:
        return int(self._get("legend_item_spacing", 8))

    @property
    def legend_item_height(self) -> int:
        return int(self._get("legend_item_height", 20))

    @property
    def legend_x(self) -> int:
        return int(self._get("legend_x", 20))

    @property
    def legend_y(self) -> int:
        return int(self._get("legend_y", 50))

    @property
    def legend_to_diagram_spacing(self) -> int:
        return int(self._get("legend_to_diagram_spacing", 20))

    # Legend layout settings (3-column layout)
    @property
    def legend_column_gap(self) -> int:
        return int(self._get_nested("legend", "column_gap", default=15))

    @property
    def legend_column_margin(self) -> int:
        return int(self._get_nested("legend", "column_margin", default=5))

    @property
    def legend_vnet_box_width(self) -> int:
        return int(self._get_nested("legend", "vnet_box_width", default=40))

    @property
    def legend_vnet_box_height(self) -> int:
        return int(self._get_nested("legend", "vnet_box_height", default=30))

    @property
    def legend_vnet_box_to_label_gap(self) -> int:
        return int(self._get_nested("legend", "vnet_box_to_label_gap", default=45))

    @property
    def legend_connection_line_length(self) -> int:
        return int(self._get_nested("legend", "connection_line_length", default=50))

    @property
    def legend_connection_line_to_label_gap(self) -> int:
        return int(self._get_nested("legend", "connection_line_to_label_gap", default=5))

    @property
    def legend_icon_size(self) -> int:
        return int(self._get_nested("legend", "icon_size", default=20))

    @property
    def legend_icons_per_sub_column(self) -> int:
        return int(self._get_nested("legend", "icons_per_sub_column", default=4))

    @property
    def legend_icon_sub_column_gap(self) -> int:
        return int(self._get_nested("legend", "icon_sub_column_gap", default=5))

    @property
    def legend_icon_to_label_gap(self) -> int:
        return int(self._get_nested("legend", "icon_to_label_gap", default=5))

    # Cell ID management
    @property
    def cell_id_start(self) -> int:
        return int(self._get_nested("cell_id", "start", default=10))

    # Draw.io settings
    @property
    def drawio_grid_size(self) -> int:
        return int(self._get_nested("drawio", "grid_size", default=10))

    @property
    def drawio_page_dx(self) -> int:
        return int(self._get_nested("drawio", "page_dx", default=1422))

    @property
    def drawio_page_dy(self) -> int:
        return int(self._get_nested("drawio", "page_dy", default=794))

    # Label/text spacing
    @property
    def label_spacing_top(self) -> int:
        return int(self._get_nested("label", "spacing_top", default=5))

    @property
    def label_spacing_left(self) -> int:
        return int(self._get_nested("label", "spacing_left", default=5))

    # Hybrid connectivity settings
    @property
    def hybrid_onprem_x_offset(self) -> int:
        return int(self._get_nested("hybrid", "onprem_x_offset", default=200))

    @property
    def hybrid_azure_x(self) -> int:
        return int(self._get_nested("hybrid", "azure_x", default=700))

    @property
    def hybrid_connection_spacing(self) -> int:
        return int(self._get_nested("hybrid", "connection_spacing", default=300))

    @property
    def hybrid_vertical_spacing(self) -> int:
        return int(self._get_nested("hybrid", "vertical_spacing", default=150))

    @property
    def hybrid_onprem_box_width(self) -> int:
        return int(self._get_nested("hybrid", "onprem_box_width", default=250))

    @property
    def hybrid_onprem_box_height(self) -> int:
        return int(self._get_nested("hybrid", "onprem_box_height", default=140))

    @property
    def hybrid_router_icon_size(self) -> int:
        return int(self._get_nested("hybrid", "router_icon_size", default=30))

    @property
    def hybrid_content_start_y(self) -> int:
        return int(self._get_nested("hybrid", "content_start_y", default=35))

    @property
    def hybrid_content_spacing(self) -> int:
        return int(self._get_nested("hybrid", "content_spacing", default=8))

    @property
    def hybrid_content_bottom_padding(self) -> int:
        return int(self._get_nested("hybrid", "content_bottom_padding", default=10))

    @property
    def hybrid_info_box_width(self) -> int:
        return int(self._get_nested("hybrid", "info_box_width", default=300))

    @property
    def hybrid_info_box_line_height(self) -> int:
        return int(self._get_nested("hybrid", "info_box_line_height", default=20))

    @property
    def hybrid_info_box_padding(self) -> int:
        return int(self._get_nested("hybrid", "info_box_padding", default=10))

    @property
    def hybrid_info_box_offset_y(self) -> int:
        return int(self._get_nested("hybrid", "info_box_offset_y", default=50))


# Global config instance (singleton pattern)
_config_instance: DiagramConfig | None = None


def get_config() -> DiagramConfig:
    """Get the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = DiagramConfig()
    return _config_instance

