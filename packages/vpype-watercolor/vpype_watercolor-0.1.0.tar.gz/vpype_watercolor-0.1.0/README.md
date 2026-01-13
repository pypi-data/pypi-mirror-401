# vpype-watercolor

A [vpype](https://github.com/abey79/vpype) plugin for watercolor plotting. It adds water dipping and paint loading sequences before each colored layer for use with pen plotters.

> **Note:** This project is experimental. It works for me, but there might still be bugs and missing features.

<p align="center">
  <img src="examples/watercolor_example.jpg" alt="Watercolor painting created with a pen plotter" width="60%">
</p>

## How It Works

For each path in the input SVG, the plugin:

1. Draws a circle at the water tray (dip to wet brush)
2. Draws circles at the matching paint tray (load paint) - stacked over each other as one continuous line
3. Draws the path

## Installation

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and run the following command to install vpype-watercolor.

```bash
uv pip install vpype-watercolor
```

## Usage

```bash
uv run vpype \
  read --attr stroke examples/input.svg \
  scaleto 15cm 15cm \
  watercolor --layout examples/layout.svg --center --max-length 5cm --water-every 3 --paint-every 3 --color-map '{"#e30022": "#00A550"}' \
  write plot.svg
```

The `--attr stroke` option is required to read colors from the input SVG into layer properties.

### Options

Finding the right options for your brush and setup might need some experimentation.

- `-l, --layout FILE` (required): Path to layout SVG defining tray positions
- `--center`: Center the artwork within the paper area
- `--dip-radius LENGTH`: Radius of dip circles (default: 4mm)
- `--paint-circles INTEGER`: Number of circles at paint tray (default: 4)
- `--max-length LENGTH`: Maximum line length before splitting (e.g., 5cm). Lines longer than this are split into equal parts, each getting its own dip sequence.
- `--color-map JSON`: Map SVG colors to layout colors, e.g., `'{"#ff0000": "#cc0000"}'`. Useful when your SVG uses different colors than your physical paint trays.
- `--color-filter COLOR`: Only output paths matching this color (e.g., `'#ff0000'`). Applied after color-map.
- `--water-every INTEGER`: Dip in water every N line segments (default: 3).
- `--paint-every INTEGER`: Dip in paint every N line segments (default: 3).
- `--reverse-lines`: Draw each line forward then backward before pen up.
- `--translate X Y`: Translate the artwork by X and Y (e.g., `--translate 10mm 5mm`).

### Layout

The layout SVG defines the physical positions of trays on your plotter.

![Example layout that can be used as a layout to tell the plotter where the water, watercolor and paper is.](examples/layout.svg)

This is the layout I use. You can use it as a starting point. The fill color of the paint trays define the paint color. Go to [piebro.github.io/vpype-watercolor](https://piebro.github.io/vpype-watercolor) to interactively modify the layout and download it.

### Debug Visualization

To create a debug SVG that shows the layout with the plot overlaid:

```bash
vpype-merge-debug examples/layout.svg plot.svg debug.svg
```

This merges the layout SVG (with background and filled rectangles) with the plot paths for visual verification.

### Plot with AxiCLI

Install the AxiDraw API:

```bash
uv pip install https://cdn.evilmadscientist.com/dl/ad/public/AxiDraw_API.zip
```

Toggle the pen to adjust pen up/down positions:

```bash
axicli --mode toggle --pen_pos_down 20 --pen_pos_up 75
```

Generate a preview SVG to verify the plot before running:

```bash
uv run axicli plot.svg --model 2 -G4 --speed_pendown 15 --pen_pos_down 20 --pen_pos_up 75 --report_time -vg3 -o preview.svg
```

Run the plot and return to the align position when done:

```bash
uv run axicli plot.svg --model 2 -G4 --speed_pendown 15 --pen_pos_down 20 --pen_pos_up 75 && uv run axicli -m align
```

The `-G4` flag is required to strictly preserve file order. Without it, AxiCLI may reorder paths to optimize travel distance, which breaks the water→paint→line sequence.

### Plotting Pixel Art

The example above was created using this generative algorithm: [github.com/piebro/substitution-system](https://github.com/piebro/substitution-system).

Install [vpype-pixelart](https://github.com/abey79/vpype-pixelart) to convert pixel art images to plottable paths:

```bash
uv pip install vpype-pixelart
```

Extract all hex colors from a pixel art image for the color map, or just do it manually:

```bash
uv run --with pillow python -c "from PIL import Image; img = Image.open('examples/example_pixelart.png').convert('RGB'); print(' '.join(sorted(set(f'#{r:02x}{g:02x}{b:02x}' for r,g,b in img.get_flattened_data()))))"
```

Convert pixel art to watercolor plot:

```bash
uv run vpype pixelart --mode line --pen-width 1.5mm --overdraw 0.35 --upscale 4 examples/example_pixelart_2.png \
  reverse --flip \
  linesort --no-flip \
  watercolor --layout examples/layout.svg --center --water-every 16 --paint-every 4 --color-map '{"#006992": "#e30022", "#eaf8bf": "#120a8f", "#eca400": "#e3a857"}' --translate -100mm 0mm \
  write plot.svg
```

## Resources

- [Plotter Painting Q&A by Licia He](https://www.eyesofpanda.com/project/plotter_painting_q_a/)
- [Watercolour Plots by Amy Goodchild](https://www.amygoodchild.com/blog/watercolour-plots)
- [Watercolor Plots by Lars Wander](https://larswander.com/writing/watercolor-plots/)

## Development

To publish a new version to PyPI:

```bash
git tag v0.1.0
git push origin v0.1.0
```

## Contributing

Contributions are welcome. Open an issue or PR if you want to report a bug or have a feature request.

## License

All code in this project is licensed under the MIT License.
