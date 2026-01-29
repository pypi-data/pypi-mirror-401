"""Diagram generation module for Azure VNet topology."""

# Export config classes for use by diagram_generator
# Note: generate_hld_diagram is still exported from diagram_generator.py
# TODO: After full refactoring, generate_hld_diagram will be moved here
from gettopology.diagram.config import DiagramConfig, get_config

__all__ = ["DiagramConfig", "get_config"]

