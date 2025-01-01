"""
Command Line Interface for DocsForAI.

This module provides the CLI commands for building and downloading documentation.
"""

import click
import logging
from pathlib import Path
from typing import Optional

from .builder import build_documentation
from .downloader.github_api import download_from_github
from .utils import parse_config

# Configure logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_logging(debug: bool):
    """Configure logging level based on debug flag."""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    else:
        logging.getLogger().setLevel(logging.INFO)

@click.group()
@click.version_option()
@click.option('--debug', is_flag=True, help='Enable debug logging')
def main(debug: bool):
    """DocsForAI: Build and download documentation with ease.
    
    This tool allows you to:
    1. Build documentation from source using various frameworks
    2. Download pre-built documentation for popular packages
    """
    setup_logging(debug)

@main.command()
@click.argument('package_name', type=str)
@click.option('--version', '-v', type=str, help='Specific version to download')
@click.option('--output', '-o', type=click.Path(), default='./docs', 
              help='Output directory for downloaded documentation')
def download(package_name: str, version: Optional[str], output: str):
    """Download pre-built documentation for a package.
    
    PACKAGE_NAME: Name of the package to download documentation for
    """
    try:
        logger.debug(f"Downloading documentation for {package_name} (version: {version}) to {output}")
        output_path = Path(output)
        result = download_from_github(package_name, version, output_path)
        click.echo(f"Successfully downloaded documentation to: {result}")
    except Exception as e:
        logger.error(f"Error downloading documentation: {str(e)}")
        click.echo(f"Failed to download documentation for {package_name}. Error: {str(e)}", err=True)
        raise click.Abort()

@main.command()
@click.argument('config_path', type=click.Path(exists=True))
def build(config_path: str):
    """Build documentation using a configuration file.
    
    CONFIG_PATH: Path to the YAML configuration file
    """
    try:
        logger.debug(f"Building documentation using config file: {config_path}")
        # Convert string path to Path object
        config_file = Path(config_path)
        
        # Parse the config file
        logger.debug("Parsing configuration file")
        config = parse_config(config_file)
        
        # Build the documentation
        logger.debug("Starting documentation build process")
        result = build_documentation(config)
        click.echo(f"Successfully built documentation: {result}")
    except Exception as e:
        logger.error(f"Error building documentation: {str(e)}")
        click.echo(f"Failed to build documentation. Error: {str(e)}", err=True)
        raise click.Abort()

@main.command()
def init():
    """Initialize a new documentation configuration file."""
    try:
        logger.debug("Initializing new configuration file")
        template_path = Path(__file__).parent / 'templates' / 'config_template.yaml'
        logger.debug(f"Using template from: {template_path}")
        
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        output_path = Path.cwd() / 'docsforai.yaml'
        logger.debug(f"Writing configuration to: {output_path}")
        
        with open(output_path, 'w') as f:
            f.write(template_content)
        
        click.echo(f"Created configuration file at: {output_path}")
    except Exception as e:
        logger.error(f"Error creating configuration file: {str(e)}")
        click.echo(f"Failed to create configuration file. Error: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    main()