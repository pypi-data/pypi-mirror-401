# markmap-export

Export [Markmap](https://markmap.js.org/) mind maps to high-resolution PNG images.

## Why?

Markmap uses SVG with `<foreignObject>` for KaTeX and syntax highlighting, which breaks standard screenshot tools and SVG converters. This tool uses Playwright to render the actual browser output at any resolution.

## Install

```bash
uv tool install markmap-export
markmap-export --install-browser
```

## Usage

```bash
# Auto-detect optimal size (recommended)
markmap-export mindmap.html

# Specify output path
markmap-export mindmap.html -o output.png

# Custom dimensions and scale
markmap-export mindmap.html -w 3000 -H 4000 -s 2
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output` | Output PNG path | Same as input |
| `-w, --width` | Viewport width | Auto-detect |
| `-H, --height` | Viewport height | Auto-detect |
| `-s, --scale` | Device scale factor | 2.0 (Retina) |
| `--wait` | Render wait time (ms) | 2000 |
| `-q, --quiet` | Suppress output | False |

## License

MIT
