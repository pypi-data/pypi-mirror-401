"""VNet categorization and grouping logic."""

import logging
from collections import deque

from gettopology.diagram.models import HubSpokeGroup, VNetCategory
from gettopology.models import TopologyModel, VirtualNetworkModel


def categorize_vnets(topology: TopologyModel) -> VNetCategory:
    """Categorize VNets into hubs, hub spokes, hubless spokes, and stubs.

    A hub spoke is a VNet that is connected (directly or transitively) to a hub.
    A hubless spoke is a VNet that has peerings but is NOT connected to any hub.

    Uses BFS to find all VNets transitively connected to hubs.

    Args:
        topology: TopologyModel containing all virtual networks

    Returns:
        VNetCategory with categorized VNets
    """
    hubs: list[VirtualNetworkModel] = []
    hub_spokes: list[VirtualNetworkModel] = []
    hubless_spokes: list[VirtualNetworkModel] = []
    stubs: list[VirtualNetworkModel] = []

    # Build VNet name to VNet mapping
    vnet_by_name: dict[str, VirtualNetworkModel] = {vnet.name: vnet for vnet in topology.virtual_networks}
    all_vnet_names: set[str] = set(vnet_by_name.keys())

    # Identify hubs (VNets with GatewaySubnet or AzureFirewallSubnet)
    hub_names = {vnet.name for vnet in topology.virtual_networks if vnet.hub}

    # First pass: categorize hubs and stubs
    for vnet in topology.virtual_networks:
        if vnet.hub:
            hubs.append(vnet)
        elif vnet.peering_count == 0:
            stubs.append(vnet)

    # Second pass: Use BFS to find all VNets transitively connected to hubs
    # Start BFS from each hub and mark all reachable VNets as hub spokes
    hub_connected_names: set[str] = set(hub_names)  # Start with hubs themselves
    queue = deque(hub_names)

    while queue:
        current_name = queue.popleft()
        current_vnet = vnet_by_name.get(current_name)
        if not current_vnet:
            continue

        # Check all peers of this VNet
        for peer_name in current_vnet.peering_names:
            # Only consider peers that exist in our topology and haven't been visited yet
            if peer_name in all_vnet_names and peer_name not in hub_connected_names:
                hub_connected_names.add(peer_name)
                queue.append(peer_name)

    # Third pass: Categorize remaining VNets (those with peerings but not connected to hubs)
    for vnet in topology.virtual_networks:
        if vnet.hub or vnet.peering_count == 0:
            continue  # Already categorized as hub or stub

        if vnet.name in hub_connected_names:
            hub_spokes.append(vnet)
        else:
            hubless_spokes.append(vnet)

    logging.info(
        f"Categorized: {len(hubs)} hub(s), {len(hub_spokes)} hub spoke(s) "
        f"(transitively connected to hubs), {len(hubless_spokes)} hubless spoke(s), {len(stubs)} stub(s)"
    )

    return VNetCategory(hubs=hubs, hub_spokes=hub_spokes, hubless_spokes=hubless_spokes, stubs=stubs)


def group_hubs_with_spokes(categories: VNetCategory) -> tuple[list[HubSpokeGroup], list[list[VirtualNetworkModel]], list[VirtualNetworkModel]]:
    """Group hubs with their spoke VNets (direct and transitive), and group hubless spokes into connected components.

    A spoke belongs to a hub group if it is transitively connected to that hub (via BFS).
    This includes:
    - Direct spokes: VNets that directly peer with the hub
    - Transitive spokes: VNets that peer with other spokes in the hub group

    Args:
        categories: VNetCategory with categorized VNets

    Returns:
        Tuple of:
        - List of HubSpokeGroup (hub with its spokes - direct and transitive)
        - List of hubless spoke groups (each group is a list of connected hubless VNets)
        - List of stub VNets
    """
    {hub.name for hub in categories.hubs}
    hub_spoke_groups: list[HubSpokeGroup] = []

    # Build adjacency list for all VNets (for BFS traversal)
    vnet_by_name: dict[str, VirtualNetworkModel] = {}
    all_vnets = categories.hubs + categories.hub_spokes + categories.hubless_spokes + categories.stubs
    for vnet in all_vnets:
        vnet_by_name[vnet.name] = vnet

    # For each hub, find all spokes transitively connected to it using BFS
    for hub in categories.hubs:
        # Use BFS to find all VNets transitively connected to this hub
        hub_connected_names: set[str] = {hub.name}  # Start with hub itself
        queue = deque([hub.name])

        while queue:
            current_name = queue.popleft()
            current_vnet = vnet_by_name.get(current_name)
            if not current_vnet:
                continue

            # Check all peers of this VNet
            for peer_name in current_vnet.peering_names:
                # Only consider peers that:
                # 1. Exist in our topology
                # 2. Haven't been visited yet
                # 3. Are hub spokes (transitively connected to hubs, as determined by BFS categorization)
                if (peer_name in vnet_by_name and
                    peer_name not in hub_connected_names and
                    peer_name in {s.name for s in categories.hub_spokes}):
                    hub_connected_names.add(peer_name)
                    queue.append(peer_name)

        # Find all hub spokes that are connected to this hub (directly or transitively)
        # Exclude the hub itself
        spokes = [
            spoke for spoke in categories.hub_spokes
            if spoke.name in hub_connected_names and spoke.name != hub.name
        ]
        hub_spoke_groups.append(HubSpokeGroup(hub=hub, spokes=spokes))

    # Group hubless spokes into connected components
    hubless_groups = group_hubless_spokes_into_components(categories.hubless_spokes)

    # Log grouping results
    logging.debug(
        f"Grouped {len(categories.hubs)} hub(s) with "
        f"{sum(len(group.spokes) for group in hub_spoke_groups)} total spoke(s), "
        f"{len(categories.hubless_spokes)} hubless spoke(s) into {len(hubless_groups)} group(s), "
        f"{len(categories.stubs)} stub(s)"
    )

    return (hub_spoke_groups, hubless_groups, categories.stubs)


def group_hubless_spokes_into_components(
    hubless_spokes: list[VirtualNetworkModel],
) -> list[list[VirtualNetworkModel]]:
    """Group hubless spokes into independent connected components.

    Two hubless spokes are in the same group if they are connected (directly or transitively)
    through peerings. Groups are independent if there's no path between them.

    Uses BFS to find connected components in the peering graph.

    Args:
        hubless_spokes: List of hubless spoke VNets

    Returns:
        List of groups, where each group is a list of VNets that are connected
        (transitively) through peerings.
    """
    if not hubless_spokes:
        return []

    # Build name-to-vnet mapping for quick lookup
    vnet_by_name: dict[str, VirtualNetworkModel] = {vnet.name: vnet for vnet in hubless_spokes}
    hubless_names: set[str] = set(vnet_by_name.keys())

    # Build adjacency list: vnet_name -> set of peer names (only hubless peers)
    adjacency: dict[str, set[str]] = {}
    for vnet in hubless_spokes:
        # Only include peers that are also hubless spokes
        hubless_peers = {peer_name for peer_name in vnet.peering_names if peer_name in hubless_names}
        adjacency[vnet.name] = hubless_peers

    # Find connected components using BFS
    visited: set[str] = set()
    components: list[list[VirtualNetworkModel]] = []

    for vnet in hubless_spokes:
        if vnet.name in visited:
            continue

        # BFS to find all connected VNets
        component_names: set[str] = set()
        queue = deque([vnet.name])
        visited.add(vnet.name)
        component_names.add(vnet.name)

        while queue:
            current_name = queue.popleft()
            # Add all unvisited hubless peers
            for peer_name in adjacency.get(current_name, set()):
                if peer_name not in visited:
                    visited.add(peer_name)
                    component_names.add(peer_name)
                    queue.append(peer_name)

        # Convert component names to VNet objects
        component = [vnet_by_name[name] for name in component_names]
        components.append(component)
        logging.debug(
            f"Hubless group {len(components)}: {len(component)} VNet(s) - "
            f"{', '.join(v.name for v in component)}"
        )

    logging.info(
        f"Grouped {len(hubless_spokes)} hubless spoke(s) into {len(components)} independent group(s)"
    )

    return components

