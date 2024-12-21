"""
Downloader module for DocsForAI.

This module provides functionality to download pre-built documentation from various sources.
"""

from .github_api import download_from_github

__all__ = ['download_from_github']