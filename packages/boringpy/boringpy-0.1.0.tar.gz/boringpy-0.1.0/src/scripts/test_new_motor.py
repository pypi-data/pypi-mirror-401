#!/usr/bin/env python
"""Test script for the new BoringPy generator motor."""

import sys
from pathlib import Path

from lib_boring_logger import logger

from boringpy.core.generator import GeneratorConfig
from boringpy.generators import ApiGenerator


def main():
    """Generate a test API using the new generator motor."""
    # Parse arguments
    if len(sys.argv) < 2:
        logger.error("Usage: python test_new_motor.py <package_name> [port]")
        sys.exit(1)

    package_name = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    logger.info("=" * 60)
    logger.info("BoringPy Generator Motor Test")
    logger.info("=" * 60)

    # Load template config
    template_dir = Path("templates/api")
    if not template_dir.exists():
        logger.error(f"Template directory not found: {template_dir}")
        sys.exit(1)

    logger.info(f"Loading template config from: {template_dir}")
    config = GeneratorConfig.from_template_json(template_dir)
    logger.success(f"Loaded config: {config.name}")

    # Create generator
    logger.info("Initializing ApiGenerator...")
    generator = ApiGenerator(config)

    # Set destination
    destination = Path("src/apps")
    if not destination.exists():
        logger.warning(f"Destination directory does not exist, creating: {destination}")
        destination.mkdir(parents=True, exist_ok=True)

    # Generate API
    logger.info("")
    logger.info(f"Generating API: {package_name}")
    logger.info(f"Port: {port}")
    logger.info(f"Destination: {destination}")
    logger.info("")

    try:
        generator.generate(
            destination=destination,
            package_name=package_name,
            port=port,
        )

        logger.info("")
        logger.info("=" * 60)
        logger.success("Generation completed successfully!")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Generation failed: {e}")
        logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()
