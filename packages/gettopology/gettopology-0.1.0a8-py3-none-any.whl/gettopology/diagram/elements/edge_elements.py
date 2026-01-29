"""Edge/connection element creation utilities for diagram generation."""

from xml.etree.ElementTree import Element, SubElement

from gettopology.diagram.config import get_config

# Get global config instance
_config = get_config()


def build_edge_style(
    color: str,
    pattern: str = "solid",
    edge_style_type: str = "orthogonalEdgeStyle",
    config=None
) -> str:
    """Build edge style string with configurable pattern.

    Args:
        color: Edge color (hex code)
        pattern: "solid" or "dashed"
        edge_style_type: Draw.io edge style ("orthogonalEdgeStyle", "none", etc.)
        config: DiagramConfig instance (optional, uses global if None)

    Returns:
        Complete edge style string for Draw.io
    """
    if config is None:
        config = _config

    dashed = ""
    if pattern == "dashed":
        dashed = f"dashed=1;dashPattern={config.edge_dash_pattern};"

    # Build style string
    if edge_style_type == "none":
        # For hub-to-hub and external connections - straight line
        return (
            f"edgeStyle={edge_style_type};rounded=0;html=1;"
            f"strokeColor={color};strokeWidth=2;"
            f"{dashed}startArrow=block;endArrow=block;"
        )
    else:
        # For orthogonal routing (hub-to-spoke, hubless, etc.)
        return (
            f"edgeStyle={edge_style_type};rounded=0;"
            f"orthogonalLoop=1;jettySize=auto;html=1;"
            f"strokeColor={color};strokeWidth=2;"
            f"{dashed}startArrow=block;endArrow=block;"
        )


def create_edge_element(
    root: Element,
    cell_id: int,
    source_id: int,
    target_id: int,
    style: str
) -> Element:
    """Create a basic edge XML element.

    Args:
        root: Root XML element
        cell_id: Cell ID for the edge
        source_id: Source VNet cell ID
        target_id: Target VNet cell ID
        style: Edge style string

    Returns:
        Created mxCell element
    """
    mxCell = SubElement(root, "mxCell")
    mxCell.set("id", str(cell_id))
    mxCell.set("style", style)
    mxCell.set("edge", "1")
    mxCell.set("parent", "1")
    mxCell.set("source", str(source_id))
    mxCell.set("target", str(target_id))

    return mxCell


def create_waypoint(
    array_elem: Element,
    x: float,
    y: float
) -> Element:
    """Create a waypoint XML element.

    Args:
        array_elem: Array element to add waypoint to
        x: X coordinate
        y: Y coordinate

    Returns:
        Created mxPoint element
    """
    waypoint = SubElement(array_elem, "mxPoint")
    waypoint.set("x", str(x))
    waypoint.set("y", str(y))
    return waypoint

