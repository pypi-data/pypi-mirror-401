"""MCP server for generating images using Google's Nano Banana Pro model via Replicate."""

__version__ = "0.1.0"

from .server import generate_image, mcp

__all__ = ["generate_image", "mcp", "__version__"]
