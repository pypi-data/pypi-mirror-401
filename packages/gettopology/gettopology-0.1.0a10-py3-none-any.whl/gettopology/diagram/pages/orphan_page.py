"""Orphan/Stub VNet page generation for diagram.

Creates a separate page for VNets with no peerings (stubs/orphans).
"""

from xml.etree.ElementTree import Element, SubElement

from gettopology.diagram.config import get_config
from gettopology.diagram.elements.vnet_elements import calculate_vnet_height, create_vnet_group
from gettopology.diagram.legend import create_legend
from gettopology.models import VirtualNetworkModel

# Get global config instance
_config = get_config()

# Constants
CANVAS_PADDING = _config.canvas_padding
VNET_WIDTH = _config.vnet_width
VNET_SPACING_Y = _config.vnet_spacing_y
STUB_SPACING_X = _config.stub_spacing_x


def create_orphan_page(
    mxfile: Element,
    stubs: list[VirtualNetworkModel],
    cell_id_start: int,
) -> None:
    """Create orphan/stub VNet page.

    Args:
        mxfile: Root mxfile element
        stubs: List of stub/orphan VNets (no peerings)
        cell_id_start: Starting cell ID for this page
    """
    if not stubs:
        return

    # Create diagram for orphans
    orphan_diagram = SubElement(mxfile, "diagram")
    orphan_diagram.set("id", "topology-orphans")
    orphan_diagram.set("name", "Orphan VNets")

    orphan_mxGraphModel = SubElement(orphan_diagram, "mxGraphModel")
    orphan_mxGraphModel.set("dx", str(_config.drawio_page_dx))
    orphan_mxGraphModel.set("dy", str(_config.drawio_page_dy))
    orphan_mxGraphModel.set("grid", "1")
    orphan_mxGraphModel.set("gridSize", str(_config.drawio_grid_size))
    orphan_mxGraphModel.set("guides", "1")
    orphan_mxGraphModel.set("tooltips", "1")
    orphan_mxGraphModel.set("connect", "1")
    orphan_mxGraphModel.set("arrows", "1")
    orphan_mxGraphModel.set("fold", "1")
    orphan_mxGraphModel.set("page", "1")
    orphan_mxGraphModel.set("pageWidth", str(_config.page_width))
    orphan_mxGraphModel.set("pageHeight", str(_config.page_height))
    orphan_mxGraphModel.set("math", "0")
    orphan_mxGraphModel.set("shadow", "0")

    orphan_root = SubElement(orphan_mxGraphModel, "root")

    # Add mxCell for root
    orphan_root_cell = SubElement(orphan_root, "mxCell")
    orphan_root_cell.set("id", "0")

    orphan_root_cell_layer = SubElement(orphan_root, "mxCell")
    orphan_root_cell_layer.set("id", "1")
    orphan_root_cell_layer.set("parent", "0")

    # Create legend for orphan page
    orphan_cell_id_counter = cell_id_start
    orphan_legend_x = _config.legend_x
    orphan_legend_y = CANVAS_PADDING
    orphan_cell_id_counter, actual_legend_height = create_legend(orphan_root, orphan_cell_id_counter, orphan_legend_x, orphan_legend_y)

    # Layout orphans in exactly 3 columns with proper spacing
    # Start below legend - use actual legend height to ensure no overlap
    legend_padding = _config.legend_padding
    legend_bottom_y = CANVAS_PADDING + actual_legend_height + legend_padding

    orphan_start_y = legend_bottom_y + _config.legend_to_diagram_spacing

    # Use exactly 3 columns
    vnets_per_row = 3

    # Use fixed horizontal spacing between columns
    horizontal_spacing = STUB_SPACING_X

    # Calculate available width for 3 columns (excluding legend area)
    legend_area_right = _config.legend_x + _config.legend_width + _config.legend_padding

    # Calculate total width needed for 3 columns with spacing
    total_width_needed = (VNET_WIDTH * vnets_per_row) + (horizontal_spacing * (vnets_per_row - 1))

    # Center the 3 columns in the available space
    available_width = _config.page_width - legend_area_right - CANVAS_PADDING
    orphan_start_x = legend_area_right + ((available_width - total_width_needed) / 2)

    # Use proper vertical spacing between rows
    vertical_spacing = VNET_SPACING_Y

    # Track row heights to calculate Y positions correctly
    row_heights: dict[int, float] = {}  # row_number -> max height in that row

    # First pass: calculate max height for each row
    for index, vnet in enumerate(stubs):
        row_number = index // vnets_per_row
        vnet_height = calculate_vnet_height(vnet)
        if row_number not in row_heights:
            row_heights[row_number] = vnet_height
        else:
            row_heights[row_number] = max(row_heights[row_number], vnet_height)

    # Second pass: create VNets with proper positioning
    current_y: float = orphan_start_y
    for index, vnet in enumerate(stubs):
        row_number = index // vnets_per_row
        position_in_row = index % vnets_per_row

        # Calculate X position: start + (column_index * (width + spacing))
        x_position = orphan_start_x + (position_in_row * (VNET_WIDTH + horizontal_spacing))

        # Calculate Y position: if this is the first VNet in a row, use current_y
        # Otherwise, use the same Y as other VNets in the row
        if position_in_row == 0:
            # First VNet in row - set Y position
            if row_number > 0:
                # Add height of previous row + spacing
                current_y += row_heights[row_number - 1] + vertical_spacing
            y_position = current_y
        else:
            # Same row as previous VNet - use same Y
            y_position = current_y

        group_id, vnet_main_id, orphan_cell_id_counter = create_vnet_group(
            orphan_root, orphan_cell_id_counter, vnet, x_position, y_position, is_hub=False, is_stub=True
        )

