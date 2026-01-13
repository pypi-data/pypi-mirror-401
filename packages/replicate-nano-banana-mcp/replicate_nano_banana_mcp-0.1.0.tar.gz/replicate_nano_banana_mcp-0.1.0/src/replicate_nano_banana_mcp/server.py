"""MCP server for generating images using Google's Nano Banana Pro model via Replicate."""

import os
from typing import Literal

import replicate
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Nano Banana Image Generator")


@mcp.tool()
def generate_image(
    prompt: str,
    resolution: Literal["1K", "2K"] = "2K",
    aspect_ratio: Literal["1:1", "4:3", "3:4", "16:9", "9:16"] = "4:3",
    output_format: Literal["png", "jpg", "webp"] = "png",
    safety_filter_level: Literal[
        "block_low_and_above", "block_medium_and_above", "block_only_high"
    ] = "block_only_high",
) -> str:
    """Generate an image using Google's Nano Banana Pro model.

    Args:
        prompt: Text description of the image to generate.
        resolution: Output resolution - "1K" or "2K".
        aspect_ratio: Aspect ratio of the output image.
        output_format: Output image format.
        safety_filter_level: Safety filter strictness level.

    Returns:
        URL of the generated image.
    """
    if not os.environ.get("REPLICATE_API_TOKEN"):
        raise ValueError(
            "REPLICATE_API_TOKEN environment variable is not set. "
            "Please set it to your Replicate API token."
        )

    output = replicate.run(
        "google/nano-banana-pro",
        input={
            "prompt": prompt,
            "resolution": resolution,
            "image_input": [],
            "aspect_ratio": aspect_ratio,
            "output_format": output_format,
            "safety_filter_level": safety_filter_level,
        },
    )

    return str(output.url)


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
