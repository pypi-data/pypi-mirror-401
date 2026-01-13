# replicate-nano-banana-mcp

An MCP (Model Context Protocol) server for generating images using Google's Nano Banana Pro model via Replicate.

## Features

- **MCP Server**: Expose image generation as an MCP tool for use with Claude and other MCP-compatible clients
- **CLI Tool**: Command-line interface for quick image generation testing

## Installation

```bash
pip install replicate-nano-banana-mcp
```

Or with uv:

```bash
uv pip install replicate-nano-banana-mcp
```

## Configuration

Set your Replicate API token as an environment variable:

```bash
export REPLICATE_API_TOKEN=your_token_here
```

## Usage

### MCP Server

Run the MCP server:

```bash
replicate-nano-banana-mcp
```

Or with uv:

```bash
uv run replicate-nano-banana-mcp
```

#### Claude Desktop Configuration

Add this to your Claude Desktop configuration file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "nano-banana": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/replicate-nano-banana-mcp",
        "run",
        "replicate-nano-banana-mcp"
      ],
      "env": {
        "REPLICATE_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

Or if installed globally:

```json
{
  "mcpServers": {
    "nano-banana": {
      "command": "replicate-nano-banana-mcp",
      "env": {
        "REPLICATE_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

### CLI Tool

Generate an image from the command line:

```bash
nano-banana-cli "A beautiful sunset over the ocean"
```

With options:

```bash
nano-banana-cli "A futuristic cityscape" \
  --resolution 2K \
  --aspect-ratio 16:9 \
  --output-format png \
  --safety-filter block_only_high
```

#### CLI Options

- `prompt`: Text description of the image to generate (required)
- `--resolution`: Output resolution - `1K` or `2K` (default: `2K`)
- `--aspect-ratio`: Aspect ratio - `1:1`, `4:3`, `3:4`, `16:9`, `9:16` (default: `4:3`)
- `--output-format`: Image format - `png`, `jpg`, `webp` (default: `png`)
- `--safety-filter`: Safety level - `block_low_and_above`, `block_medium_and_above`, `block_only_high` (default: `block_only_high`)

## MCP Tool

The server exposes a single tool:

### `generate_image`

Generate an image using Google's Nano Banana Pro model.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | (required) | Text description of the image to generate |
| `resolution` | string | `"2K"` | Output resolution: `"1K"` or `"2K"` |
| `aspect_ratio` | string | `"4:3"` | Aspect ratio: `"1:1"`, `"4:3"`, `"3:4"`, `"16:9"`, `"9:16"` |
| `output_format` | string | `"png"` | Output format: `"png"`, `"jpg"`, `"webp"` |
| `safety_filter_level` | string | `"block_only_high"` | Safety filter: `"block_low_and_above"`, `"block_medium_and_above"`, `"block_only_high"` |

**Returns:** URL of the generated image.

## Development

Clone the repository:

```bash
git clone https://github.com/sugarforever/replicate-nano-banana-mcp.git
cd replicate-nano-banana-mcp
```

Install dependencies:

```bash
uv sync
```

Run the server in development:

```bash
uv run replicate-nano-banana-mcp
```

Run the CLI in development:

```bash
uv run nano-banana-cli "Your prompt here"
```

## License

MIT License - see [LICENSE](LICENSE) for details.
