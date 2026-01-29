"""Utility functions for logging, file validation, and data normalization."""

import logging
import os
import sys
from pathlib import Path

from rich.logging import RichHandler

from gettopology.models import SubscriptionInput, VirtualNetworkModel


def setup_logging(log_level: str = "INFO") -> None:
    """Configure logging with Rich handler.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    level = getattr(logging, log_level.upper(), logging.INFO)
    # Show file paths in DEBUG mode for better debugging
    show_path = (log_level.upper() == "DEBUG")
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, show_path=show_path)],
    )

    # Reduce Azure SDK HTTP logging verbosity
    # Azure SDK uses 'azure' and 'azure.core' loggers for HTTP requests/responses
    # Set them to WARNING to suppress INFO-level HTTP logs
    azure_logger = logging.getLogger("azure")
    azure_logger.setLevel(logging.WARNING)

    azure_core_logger = logging.getLogger("azure.core")
    azure_core_logger.setLevel(logging.WARNING)

    # Also suppress urllib3 and requests if they're being used
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)


def validate_file_path(file_path: str) -> Path:
    """Validate that a file path exists, is a file, and is readable.

    Args:
        file_path: Path to the file to validate

    Returns:
        Path object if valid

    Exits:
        sys.exit(1) if file is invalid, not found, or not readable
    """
    path = Path(file_path)

    if not path.exists():
        logging.error(f"File not found: {file_path}")
        sys.exit(1)

    if not path.is_file():
        logging.error(f"Path is not a file: {file_path}")
        sys.exit(1)

    # Cross-platform readability check using os.access
    if not os.access(path, os.R_OK):
        logging.error(f"File is not readable: {file_path}")
        sys.exit(1)

    return path


def normalize_subscription_ids(sub_ids: list[str]) -> tuple[list[str], list[str]]:
    """Trim whitespace and validate subscription IDs using regex pattern.

    This is a convenience wrapper around SubscriptionInput.normalize_subscription_ids().

    Args:
        sub_ids: List of subscription ID strings to normalize and validate

    Returns:
        tuple: (valid_ids, invalid_ids)
    """
    return SubscriptionInput.normalize_subscription_ids(sub_ids)


def generate_vnet_markdown(
    vnet: VirtualNetworkModel,
    route_table_routes: dict[str, list[dict]] | None = None,
) -> str:
    """Generate markdown for a single VNet in markmap format.

    Args:
        vnet: VirtualNetworkModel
        route_table_routes: Optional dict mapping route table ID -> routes

    Returns:
        Markdown string for the VNet
    """
    lines = []

    # Frontmatter
    lines.append("---")
    lines.append(f"title: VNet - {vnet.name}")
    lines.append("markmap:")
    lines.append("  colorFreezeLevel: 2")
    lines.append("---")
    lines.append("")
    lines.append(f"# {vnet.name}")
    lines.append("")

    # Address Space
    lines.append("## Address Space")
    for addr_space in vnet.address_space:
        lines.append(f"- {addr_space}")
    lines.append("")

    # Subnets
    if vnet.subnets:
        lines.append("## Subnets")
        for subnet in vnet.subnets:
            # Subnet header with name and address prefix(es)
            if subnet.address_prefixes:
                prefixes_str = ", ".join(subnet.address_prefixes)
            else:
                prefixes_str = subnet.address_prefix if subnet.address_prefix else ""

            lines.append(f"### {subnet.name} ({prefixes_str})")
            lines.append("")

            # Attached resources
            attached_items = []
            if subnet.nat_gateway_name:
                attached_items.append(("NAT Gateway", subnet.nat_gateway_name))
            if subnet.private_endpoint_name:
                attached_items.append(("Private Endpoint", subnet.private_endpoint_name))

            if attached_items:
                lines.append("#### Attached")
                for resource_type, resource_name in attached_items:
                    lines.append(f"- {resource_type}")
                    lines.append(f"  - {resource_name}")
                lines.append("")

            # Route Table with routes
            if subnet.route_table_id and subnet.route_table_name:
                lines.append(f"#### Route Table — {subnet.route_table_name}")
                lines.append("")
                lines.append("| Route Name | Address Prefix | Next Hop Type | Next Hop IP |")
                lines.append("|-|-|-|-|")

                # Get routes if available
                routes = []
                if route_table_routes and subnet.route_table_id in route_table_routes:
                    routes = route_table_routes[subnet.route_table_id]

                if routes:
                    for route in routes:
                        name = route.get('name', '')
                        prefix = route.get('addressPrefix', '')
                        hop_type = route.get('nextHopType', '')
                        hop_ip = route.get('nextHopIpAddress', '—')
                        lines.append(f"| {name} | {prefix} | {hop_type} | {hop_ip} |")
                else:
                    lines.append("| (No routes found) | — | — | — |")
                lines.append("")

            # Network Policies
            lines.append("#### Network Policies")
            lines.append(f"- Private Endpoint Policies: {subnet.private_endpoint_network_policies}")
            lines.append(f"- Private Link Service Policies: {subnet.private_link_service_network_policies}")
            lines.append(f"- Default Outbound Access: {str(subnet.default_outbound_access).lower()}")
            lines.append("")

    # Peering
    if vnet.peering_names:
        lines.append("## Peering")
        for i, peer_name in enumerate(vnet.peering_names):
            is_local = vnet.peering_local_flags[i] if i < len(vnet.peering_local_flags) else True
            lines.append(f"- {peer_name}")
            lines.append(f"  - Local Peering: {str(is_local).lower()}")
        lines.append("")

    # Absent (Not Configured)
    absent_items = []
    # Check if any subnet has NSG
    has_nsg = any(subnet.network_security_group_name for subnet in vnet.subnets)
    if not has_nsg:
        absent_items.append("NSG")
    if vnet.vpn_gateway == "No":
        absent_items.append("VPN Gateway")
    if vnet.expressroute == "No":
        absent_items.append("ExpressRoute")
    if vnet.firewall == "No":
        absent_items.append("Azure Firewall")
    if not vnet.enable_ddos_protection:
        absent_items.append("DDoS Protection")

    # Check delegations
    has_delegations = False
    for subnet in vnet.subnets:
        if subnet.delegation_names:
            has_delegations = True
            break
    if not has_delegations:
        absent_items.append("Delegations")

    if absent_items:
        lines.append("## Absent (Not Configured)")
        for item in absent_items:
            lines.append(f"- {item}")
        lines.append("")

    # Metadata
    lines.append("## Metadata")
    lines.append(f"- Subscription: {vnet.subscription_name or vnet.subscription_id}")
    lines.append(f"- Resource Group: {vnet.resource_group_name}")
    lines.append(f"- Location: {vnet.location}")

    return "\n".join(lines)

