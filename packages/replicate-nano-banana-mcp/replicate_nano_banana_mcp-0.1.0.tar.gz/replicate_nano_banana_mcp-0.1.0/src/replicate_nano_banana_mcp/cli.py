"""CLI for testing the Nano Banana image generation."""

import argparse
import os
import sys

import replicate


def generate_image(
    prompt: str,
    resolution: str = "2K",
    aspect_ratio: str = "4:3",
    output_format: str = "png",
    safety_filter_level: str = "block_only_high",
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
    """Run the CLI."""
    parser = argparse.ArgumentParser(
        description="Generate images using Google's Nano Banana Pro model via Replicate"
    )
    parser.add_argument("prompt", help="Text description of the image to generate")
    parser.add_argument(
        "--resolution",
        choices=["1K", "2K"],
        default="2K",
        help="Output resolution (default: 2K)",
    )
    parser.add_argument(
        "--aspect-ratio",
        choices=["1:1", "4:3", "3:4", "16:9", "9:16"],
        default="4:3",
        help="Aspect ratio of the output image (default: 4:3)",
    )
    parser.add_argument(
        "--output-format",
        choices=["png", "jpg", "webp"],
        default="png",
        help="Output image format (default: png)",
    )
    parser.add_argument(
        "--safety-filter",
        choices=["block_low_and_above", "block_medium_and_above", "block_only_high"],
        default="block_only_high",
        help="Safety filter strictness level (default: block_only_high)",
    )

    args = parser.parse_args()

    if not os.environ.get("REPLICATE_API_TOKEN"):
        print(
            "Error: REPLICATE_API_TOKEN environment variable is not set.",
            file=sys.stderr,
        )
        print(
            "Please set it to your Replicate API token: export REPLICATE_API_TOKEN=<your-token>",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Generating image for prompt: {args.prompt}")
    print("Please wait...")

    try:
        url = generate_image(
            prompt=args.prompt,
            resolution=args.resolution,
            aspect_ratio=args.aspect_ratio,
            output_format=args.output_format,
            safety_filter_level=args.safety_filter,
        )
        print(f"\nGenerated image URL: {url}")
    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
