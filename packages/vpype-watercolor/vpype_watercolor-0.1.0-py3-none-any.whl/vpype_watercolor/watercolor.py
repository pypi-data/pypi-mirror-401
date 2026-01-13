"""vpype plugin for watercolor plotting.

This plugin adds water dipping and paint loading sequences before each colored path
for watercolor plotting with pen plotters.
"""

import json
from dataclasses import dataclass
from pathlib import Path

import click
import numpy as np
import vpype as vp
import vpype_cli
from svgelements import SVG, Color, Rect


@dataclass
class Tray:
    """Represents a tray in the layout (water or paint)."""

    center_x: float
    center_y: float
    width: float
    height: float
    color: str | None  # hex color for paint trays, None for water


def normalize_color(color: Color | str | None) -> str | None:
    """Normalize a color to lowercase 6-digit hex format."""
    if color is None:
        return None
    if isinstance(color, str):
        if color.lower() == "none":
            return None
        color = Color(color)
    # Get hex representation and normalize
    hex_val = color.hex
    if hex_val:
        return hex_val.lower()
    return None


def parse_color_map(color_map_json: str | None) -> dict[str, str]:
    """Parse a JSON color map string and normalize all colors.

    Args:
        color_map_json: JSON string mapping source colors to target colors,
                        e.g., '{"#ff0000": "#cc0000", "#00ff00": "#00cc00"}'

    Returns:
        Dict mapping normalized source colors to normalized target colors

    Raises:
        click.ClickException: If JSON is invalid
    """
    if color_map_json is None:
        return {}

    try:
        raw_map = json.loads(color_map_json)
    except json.JSONDecodeError as e:
        raise click.ClickException(f"Invalid JSON in --color-map: {e}")

    if not isinstance(raw_map, dict):
        raise click.ClickException("--color-map must be a JSON object/dict")

    # Normalize all colors in the map
    normalized_map: dict[str, str] = {}
    for src, dst in raw_map.items():
        src_norm = normalize_color(src)
        dst_norm = normalize_color(dst)
        if src_norm is None or dst_norm is None:
            raise click.ClickException(
                f"Invalid color in --color-map: {src} -> {dst}"
            )
        normalized_map[src_norm] = dst_norm

    return normalized_map


def parse_layout(layout_path: Path) -> tuple[dict[str, Tray], Tray, Tray, tuple[float, float]]:
    """Parse layout.svg to extract paint trays, water tray, and paper area.

    Args:
        layout_path: Path to the layout SVG file

    Returns:
        Tuple of (color_trays dict, water_tray, paper, page_size)
        color_trays is keyed by normalized hex color
        page_size is (width, height) in user units

    Raises:
        click.ClickException: If water or paper rectangles are missing
    """
    svg = SVG.parse(str(layout_path))

    # Get page size from SVG dimensions
    page_width = svg.width
    page_height = svg.height

    color_trays: dict[str, Tray] = {}
    water_tray: Tray | None = None
    paper: Tray | None = None

    for elem in svg.elements():
        if not isinstance(elem, Rect):
            continue

        # Calculate center from rect bounds
        cx = elem.x + elem.width / 2
        cy = elem.y + elem.height / 2

        elem_id = getattr(elem, "id", None)

        if elem_id == "water":
            water_tray = Tray(
                center_x=cx,
                center_y=cy,
                width=elem.width,
                height=elem.height,
                color=None,
            )
        elif elem_id == "paper":
            paper = Tray(
                center_x=cx,
                center_y=cy,
                width=elem.width,
                height=elem.height,
                color=None,
            )
        else:
            # Paint tray - extract fill color
            fill_color = getattr(elem, "fill", None)
            color_hex = normalize_color(fill_color)
            if color_hex:
                color_trays[color_hex] = Tray(
                    center_x=cx,
                    center_y=cy,
                    width=elem.width,
                    height=elem.height,
                    color=color_hex,
                )

    if water_tray is None:
        raise click.ClickException(
            "Layout SVG must contain a rectangle with id='water'"
        )
    if paper is None:
        raise click.ClickException(
            "Layout SVG must contain a rectangle with id='paper'"
        )

    return color_trays, water_tray, paper, (page_width, page_height)


def line_length(line: np.ndarray) -> float:
    """Calculate the total length of a line (sum of segment lengths).

    Args:
        line: numpy array of complex points

    Returns:
        Total length of the line
    """
    if len(line) < 2:
        return 0.0
    diffs = np.diff(line)
    return float(np.sum(np.abs(diffs)))


def split_line_equal(line: np.ndarray, max_length: float) -> list[np.ndarray]:
    """Split a line into equal parts if it exceeds max_length.

    Args:
        line: numpy array of complex points
        max_length: maximum length per segment

    Returns:
        List of line segments (each as numpy array of complex points)
    """
    total_length = line_length(line)
    if total_length <= max_length:
        return [line]

    # Calculate number of parts needed
    num_parts = int(np.ceil(total_length / max_length))
    target_length = total_length / num_parts

    # Calculate cumulative distances along the line
    diffs = np.diff(line)
    segment_lengths = np.abs(diffs)
    cumulative = np.concatenate([[0], np.cumsum(segment_lengths)])

    # Find split points
    parts = []
    current_start_idx = 0
    current_start_point = line[0]

    for part_num in range(1, num_parts):
        target_distance = part_num * target_length

        # Find the segment where this distance falls
        idx = np.searchsorted(cumulative, target_distance, side="right") - 1
        idx = min(idx, len(line) - 2)  # Clamp to valid segment index

        # Interpolate to find exact split point
        segment_start_dist = cumulative[idx]
        segment_end_dist = cumulative[idx + 1]
        segment_length = segment_end_dist - segment_start_dist

        if segment_length > 0:
            t = (target_distance - segment_start_dist) / segment_length
            split_point = line[idx] + t * (line[idx + 1] - line[idx])
        else:
            split_point = line[idx]

        # Create part from current start to split point
        part_points = [current_start_point]
        for i in range(current_start_idx, idx + 1):
            if i > current_start_idx or not np.isclose(line[i], current_start_point):
                part_points.append(line[i])
        if not np.isclose(split_point, part_points[-1]):
            part_points.append(split_point)

        parts.append(np.array(part_points))
        current_start_idx = idx
        current_start_point = split_point

    # Add final part
    final_points = [current_start_point]
    for i in range(current_start_idx, len(line)):
        if i > current_start_idx or not np.isclose(line[i], current_start_point):
            final_points.append(line[i])
    parts.append(np.array(final_points))

    return parts


def generate_circle(cx: float, cy: float, radius: float, num_points: int = 64) -> np.ndarray:
    """Generate a circle as a numpy array of complex points.

    Args:
        cx: Center x coordinate
        cy: Center y coordinate
        radius: Circle radius
        num_points: Number of points to discretize the circle

    Returns:
        numpy array of complex points representing the circle
    """
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=True)
    return cx + radius * np.cos(angles) + 1j * (cy + radius * np.sin(angles))


def get_layer_color(layer: vp.LineCollection) -> str | None:
    """Get the color of a layer from its vp_color property."""
    prop = layer.property("vp_color")
    if prop is None:
        return None
    # vp_color is a vpype.Color object, convert to hex string
    if hasattr(prop, "as_hex"):
        return prop.as_hex().lower()
    return normalize_color(str(prop))


@click.command()
@click.option(
    "-l",
    "--layout",
    type=vpype_cli.PathType(exists=True),
    required=True,
    help="Path to layout SVG defining water tray, paint trays, and paper position.",
)
@click.option(
    "--dip-radius",
    type=vpype_cli.LengthType(),
    default="4mm",
    help="Radius of dip circles (default: 4mm).",
)
@click.option(
    "--paint-circles",
    type=int,
    default=4,
    help="Number of circles to draw at paint tray (default: 4).",
)
@click.option(
    "--center",
    is_flag=True,
    help="Center the artwork within the paper area.",
)
@click.option(
    "--max-length",
    type=vpype_cli.LengthType(),
    default=None,
    help="Maximum line length before splitting (e.g., 5cm). Lines longer than this will be split into equal parts, each getting its own dip sequence.",
)
@click.option(
    "--color-map",
    type=str,
    default=None,
    help='JSON dict mapping SVG colors to layout colors, e.g., \'{"#ff0000": "#cc0000"}\'.',
)
@click.option(
    "--color-filter",
    type=str,
    default=None,
    help="Only output paths matching this color (e.g., '#ff0000'). Applied after color-map.",
)
@click.option(
    "--water-every",
    type=int,
    default=3,
    help="Dip in water every N line segments (default: 3).",
)
@click.option(
    "--paint-every",
    type=int,
    default=3,
    help="Dip in paint every N line segments (default: 3).",
)
@click.option(
    "--reverse-lines",
    is_flag=True,
    help="Draw each line forward then backward before pen up.",
)
@click.option(
    "--translate",
    nargs=2,
    type=vpype_cli.LengthType(),
    default=None,
    help="Translate the artwork by X Y (e.g., --translate 10mm 5mm).",
)
@vpype_cli.global_processor
def watercolor(
    document: vp.Document,
    layout: Path,
    dip_radius: float,
    paint_circles: int,
    center: bool,
    max_length: float | None,
    color_map: str | None,
    color_filter: str | None,
    water_every: int,
    paint_every: int,
    reverse_lines: bool,
    translate: tuple[float, float] | None,
) -> vp.Document:
    """Add watercolor dipping sequence before each layer's paths.

    For each layer in the document, this command:
    1. Moves to the water tray and draws a dip circle
    2. Moves to the matching paint tray and draws small circles
    3. Then draws the original paths

    The layout SVG must contain:
    - A rectangle with id="water" for the water tray
    - A rectangle with id="paper" for the paper area
    - Rectangles with fill colors matching the layer colors for paint trays
    """
    # Parse layout
    color_trays, water_tray, paper, page_size = parse_layout(Path(layout))

    # Parse color map
    color_mapping = parse_color_map(color_map)

    # Normalize color filter
    normalized_filter = normalize_color(color_filter) if color_filter else None

    # Set document page size from layout
    document.page_size = page_size

    # Small circle radius for paint dipping
    small_radius = dip_radius * 0.5

    # Calculate paper bounds for translating artwork
    paper_x = paper.center_x - paper.width / 2
    paper_y = paper.center_y - paper.height / 2

    # Get overall document bounds to calculate translation offset
    doc_bounds = document.bounds()
    if doc_bounds is None:
        raise click.ClickException("Document has no geometry to process")

    # Calculate artwork dimensions
    artwork_width = doc_bounds[2] - doc_bounds[0]
    artwork_height = doc_bounds[3] - doc_bounds[1]

    # Translation offset to move artwork to paper position
    if center:
        # Center artwork within paper area
        translate_x = paper_x + (paper.width - artwork_width) / 2 - doc_bounds[0]
        translate_y = paper_y + (paper.height - artwork_height) / 2 - doc_bounds[1]
    else:
        # Align to top-left of paper area
        translate_x = paper_x - doc_bounds[0]
        translate_y = paper_y - doc_bounds[1]

    # Apply additional translation if specified
    if translate:
        translate_x += translate[0]
        translate_y += translate[1]

    translation = complex(translate_x, translate_y)

    # Process each layer
    for layer_id in document.layers:
        layer = document.layers[layer_id]
        layer_color = get_layer_color(layer)

        if layer_color is None:
            # Try to infer color from layer - skip if no color
            click.echo(f"Warning: Layer {layer_id} has no color, skipping dip sequence")
            continue

        # Apply color mapping if specified
        mapped_color = color_mapping.get(layer_color, layer_color)

        # Skip layer if color filter is specified and doesn't match
        if normalized_filter and mapped_color != normalized_filter:
            # Remove this layer from the document
            document.layers[layer_id] = vp.LineCollection()
            continue

        # Find matching paint tray
        if mapped_color not in color_trays:
            available = ", ".join(color_trays.keys()) if color_trays else "none"
            if layer_color != mapped_color:
                raise click.ClickException(
                    f"No paint tray found for color {mapped_color} (mapped from {layer_color}). "
                    f"Available colors: {available}"
                )
            raise click.ClickException(
                f"No paint tray found for color {layer_color}. "
                f"Available colors: {available}"
            )

        paint_tray = color_trays[mapped_color]

        # Generate water circle (separate line)
        water_circle = generate_circle(water_tray.center_x, water_tray.center_y, dip_radius)

        # Generate paint circles as one continuous line (stacked over each other)
        paint_circles_list = []
        for _ in range(paint_circles):
            paint_circle = generate_circle(
                paint_tray.center_x,
                paint_tray.center_y,
                small_radius,
            )
            paint_circles_list.append(paint_circle)
        paint_line = np.concatenate(paint_circles_list)

        # Add dip sequence before each line
        new_lc = vp.LineCollection()

        new_lc.append(water_circle)
        new_lc.append(water_circle)
        new_lc.append(water_circle)

        line_count = 0
        for line in layer:
            # Split line if max_length is specified
            if max_length is not None:
                line_parts = split_line_equal(line, max_length)
            else:
                line_parts = [line]

            for part in line_parts:
                line_count += 1
                # Add water circle on first line and every N lines after
                if line_count == 1 or (line_count - 1) % water_every == 0:
                    new_lc.append(water_circle)
                # Add paint circles on first line and every N lines after
                if line_count == 1 or (line_count - 1) % paint_every == 0:
                    new_lc.append(paint_line)
                # Then add the path translated to paper position
                translated_part = part + translation
                if reverse_lines:
                    # Draw forward then backward as one continuous line
                    new_lc.append(np.concatenate([translated_part, translated_part[::-1]]))
                else:
                    new_lc.append(translated_part)

        # Update layer color to mapped color
        if layer_color != mapped_color:
            new_lc.set_property("vp_color", vp.Color(mapped_color))
        else:
            # Preserve original color
            new_lc.set_property("vp_color", vp.Color(layer_color))

        document.layers[layer_id] = new_lc

    return document


watercolor.help_group = "Plugins"


# vpype uses 96 DPI internally (96 units per inch = 96/25.4 units per mm)
VPYPE_UNITS_PER_MM = 96 / 25.4


def merge_svgs(layout_path: Path, plot_path: Path, output_path: Path) -> None:
    """Merge layout and plot SVGs into a single debug SVG."""
    import re

    layout_content = layout_path.read_text()
    plot_content = plot_path.read_text()

    # Extract the inner content from plot SVG (everything between <svg> tags)
    plot_match = re.search(r"<svg[^>]*>(.*)</svg>", plot_content, re.DOTALL)
    if not plot_match:
        raise click.ClickException("Could not parse plot SVG")
    plot_inner = plot_match.group(1)

    # Remove metadata and inkscape-specific attributes from plot content
    plot_inner = re.sub(r"<metadata>.*?</metadata>", "", plot_inner, flags=re.DOTALL)
    plot_inner = re.sub(r"<defs/>", "", plot_inner)
    plot_inner = re.sub(r' inkscape:\w+="[^"]*"', "", plot_inner)

    # Scale factor to convert from vpype units to layout viewBox units (mm)
    scale = 1 / VPYPE_UNITS_PER_MM

    # Wrap plot content in a group with scale transform
    plot_inner = f'<g transform="scale({scale})">{plot_inner}</g>'

    # Insert plot content before closing </svg> tag of layout
    output_content = layout_content.replace("</svg>", f"{plot_inner}</svg>")

    output_path.write_text(output_content)


@click.command()
@click.argument("layout", type=click.Path(exists=True, path_type=Path))
@click.argument("plot", type=click.Path(exists=True, path_type=Path))
@click.argument("output", type=click.Path(path_type=Path))
def merge_debug_cli(layout: Path, plot: Path, output: Path) -> None:
    """Merge layout SVG with plot SVG for debug visualization.

    LAYOUT is the layout SVG file (with background and filled rectangles).
    PLOT is the vpype output SVG file.
    OUTPUT is the merged debug SVG file to create.
    """
    merge_svgs(layout, plot, output)
    click.echo(f"Merged SVG written to {output}")
