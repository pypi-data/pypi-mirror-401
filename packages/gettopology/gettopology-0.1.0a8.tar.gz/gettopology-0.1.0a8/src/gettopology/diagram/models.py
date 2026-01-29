"""Data models for diagram generation."""

from typing import NamedTuple

from gettopology.models import VirtualNetworkModel


class VNetCategory(NamedTuple):
    """Categorization of virtual networks for diagram layout."""
    hubs: list[VirtualNetworkModel]
    hub_spokes: list[VirtualNetworkModel]  # VNets that peer with hubs
    hubless_spokes: list[VirtualNetworkModel]  # VNets with peerings but no hub peerings
    stubs: list[VirtualNetworkModel]  # VNets with no peerings


class HubSpokeGroup(NamedTuple):
    """A hub and its associated spoke VNets."""
    hub: VirtualNetworkModel
    spokes: list[VirtualNetworkModel]

