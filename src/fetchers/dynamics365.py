#!/usr/bin/env python3
"""
Microsoft Dynamics 365 Icons Fetcher

Downloads the latest Dynamics 365 icons from Microsoft's official source.
https://learn.microsoft.com/en-us/dynamics365/get-started/icons
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path
from typing import Generator

import requests

from .base import BaseFetcher, IconCategory


class Dynamics365Fetcher(BaseFetcher):
    """Fetcher for Microsoft Dynamics 365 Icons."""

    ICONS_PAGE_URL = "https://learn.microsoft.com/en-us/dynamics365/get-started/icons"
    
    # Known direct download URL pattern
    DOWNLOAD_PATTERN = r'https://download\.microsoft\.com/download/[0-9a-f-]+/Dynamics-365-icons-scalable\.zip'

    def __init__(self, cache_dir: Path):
        super().__init__(cache_dir)
        self._icons_dir: Path | None = None

    @property
    def name(self) -> str:
        return "dynamics365"

    @property
    def display_name(self) -> str:
        return "Microsoft Dynamics 365 Icons"

    def _find_download_url(self) -> str:
        """Find the latest download URL from Microsoft's page."""
        print(f"  Fetching download URL from {self.ICONS_PAGE_URL}...")

        response = requests.get(self.ICONS_PAGE_URL, timeout=30)
        response.raise_for_status()

        # Find download link in page content
        match = re.search(self.DOWNLOAD_PATTERN, response.text)
        if match:
            url = match.group(0)
            print(f"  Found: {url}")
            return url

        # Fallback: look for any .zip file from download.microsoft.com
        zip_urls = re.findall(
            r'https://download\.microsoft\.com/download/[^"\'<>\s]+\.zip',
            response.text,
            flags=re.IGNORECASE
        )
        
        if zip_urls:
            # Filter for Dynamics-related URLs
            dynamics_urls = [url for url in zip_urls if 'dynamics' in url.lower()]
            if dynamics_urls:
                url = dynamics_urls[0]
                print(f"  Found: {url}")
                return url
            # Use first .zip found
            url = zip_urls[0]
            print(f"  Found: {url}")
            return url

        raise RuntimeError("Could not find Dynamics 365 icons download URL")

    def _download_zip(self, url: str) -> Path:
        """Download the ZIP file."""
        zip_path = self.cache_dir / "dynamics365_icons.zip"

        # Check if already downloaded (simple cache)
        if zip_path.exists():
            print(f"  Using cached: {zip_path}")
            return zip_path

        print("  Downloading...")
        response = requests.get(url, timeout=120, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))

        with open(zip_path, "wb") as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if not chunk:
                    continue
                f.write(chunk)
                downloaded += len(chunk)
                if total_size:
                    percent = (downloaded / total_size) * 100
                    print(f"\r  Downloaded: {percent:.1f}%", end="", flush=True)

        print(f"\n  Saved: {zip_path} ({zip_path.stat().st_size // 1024 // 1024} MB)")
        return zip_path

    def _extract_zip(self, zip_path: Path) -> Path:
        """Extract the ZIP file."""
        extract_dir = self.cache_dir / "dynamics365_icons"

        # Check if already extracted
        if extract_dir.exists() and any(extract_dir.iterdir()):
            print(f"  Using cached extraction: {extract_dir}")
            return extract_dir

        print("  Extracting...")
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_dir)

        print(f"  Extracted to: {extract_dir}")
        return extract_dir

    def fetch(self) -> Path:
        """Download and extract Dynamics 365 icons."""
        print(f"[{self.display_name}]")

        url = self._find_download_url()
        zip_path = self._download_zip(url)
        self._icons_dir = self._extract_zip(zip_path)

        return self._icons_dir

    def _find_svg_root(self) -> Path:
        """Find the root directory containing SVG category folders."""
        if not self._icons_dir:
            raise RuntimeError("Must call fetch() first")

        # Look for SVG files recursively
        svg_files = list(self._icons_dir.rglob('*.svg'))
        if not svg_files:
            raise RuntimeError(f"No SVG files found in {self._icons_dir}")

        # Find the common parent directory
        # Typically, the structure might be flat or in subdirectories
        possible_roots = set()
        for svg_file in svg_files[:10]:  # Check first 10 files
            possible_roots.add(svg_file.parent)

        # If all SVGs are in the same directory, that's the root
        if len(possible_roots) == 1:
            return possible_roots.pop()

        # Otherwise, find the shallowest common ancestor
        common_depth = min(len(p.relative_to(self._icons_dir).parts) for p in possible_roots)
        for depth in range(common_depth + 1):
            candidates = set()
            for svg_file in svg_files:
                rel_path = svg_file.relative_to(self._icons_dir)
                if len(rel_path.parts) > depth:
                    candidates.add(self._icons_dir / Path(*rel_path.parts[:depth]))
                else:
                    candidates.add(svg_file.parent)
            
            if len(candidates) > 1:
                # Multiple categories at this level - this is likely the root
                if depth == 0:
                    return self._icons_dir
                return self._icons_dir / Path(*list(candidates)[0].relative_to(self._icons_dir).parts[:depth-1])

        return self._icons_dir

    def get_categories(self) -> Generator[IconCategory, None, None]:
        """Get Dynamics 365 icon categories."""
        if not self._icons_dir:
            raise RuntimeError("Must call fetch() first")

        svg_root = self._find_svg_root()
        print(f"  SVG root: {svg_root}")

        # Check if all SVGs are in a flat structure (no subdirectories)
        direct_svgs = list(svg_root.glob('*.svg'))
        subdirs = [d for d in svg_root.iterdir() if d.is_dir()]

        if direct_svgs and not subdirs:
            # Flat structure - all icons in one category
            yield IconCategory(name="Dynamics 365", svg_files=direct_svgs)
        else:
            # Hierarchical structure - each subdirectory is a category
            for category_dir in sorted(svg_root.iterdir()):
                if not category_dir.is_dir():
                    continue

                # Find all SVG files (may be in subdirectories)
                svg_files = list(category_dir.rglob('*.svg'))

                if svg_files:
                    # Clean up category name
                    category_name = category_dir.name.replace('-', ' ').replace('_', ' ')
                    yield IconCategory(name=category_name, svg_files=svg_files)

    def cleanup(self) -> None:
        """Remove cached files."""
        import shutil
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)


if __name__ == "__main__":
    # Test the fetcher
    cache_dir = Path("./temp/dynamics365_cache")
    fetcher = Dynamics365Fetcher(cache_dir)

    fetcher.fetch()

    print("\nCategories found:")
    for category in fetcher.get_categories():
        print(f"  - {category.name}: {len(category.svg_files)} icons")
