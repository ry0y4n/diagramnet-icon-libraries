#!/usr/bin/env python3
"""
Azure Architecture Icons Fetcher

Downloads the latest Azure Architecture Icons from Microsoft's official source.
https://learn.microsoft.com/en-us/azure/architecture/icons/
"""

import re
import zipfile
from pathlib import Path
from typing import Generator

import requests

from .base import BaseFetcher, IconCategory


class AzureFetcher(BaseFetcher):
    """Fetcher for Azure Architecture Icons."""
    
    # Microsoft's official Azure icons page
    ICONS_PAGE_URL = "https://learn.microsoft.com/en-us/azure/architecture/icons/"
    
    # Pattern to find the download link
    DOWNLOAD_PATTERN = r'https://arch-center\.azureedge\.net/icons/Azure_Public_Service_Icons_V\d+\.zip'
    
    def __init__(self, cache_dir: Path):
        super().__init__(cache_dir)
        self._icons_dir: Path | None = None
    
    @property
    def name(self) -> str:
        return "azure"
    
    @property
    def display_name(self) -> str:
        return "Azure Architecture Icons"
    
    def _find_download_url(self) -> str:
        """Find the latest download URL from Microsoft's page."""
        print(f"  Fetching download URL from {self.ICONS_PAGE_URL}...")
        
        response = requests.get(self.ICONS_PAGE_URL, timeout=30)
        response.raise_for_status()
        
        # Find download link in page content
        match = re.search(self.DOWNLOAD_PATTERN, response.text)
        if not match:
            raise RuntimeError("Could not find Azure icons download URL")
        
        url = match.group(0)
        print(f"  Found: {url}")
        return url
    
    def _download_zip(self, url: str) -> Path:
        """Download the ZIP file."""
        zip_path = self.cache_dir / "azure_icons.zip"
        
        # Check if already downloaded (simple cache)
        if zip_path.exists():
            print(f"  Using cached: {zip_path}")
            return zip_path
        
        print(f"  Downloading...")
        response = requests.get(url, timeout=120, stream=True)
        response.raise_for_status()
        
        # Get file size for progress
        total_size = int(response.headers.get('content-length', 0))
        
        with open(zip_path, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size:
                    percent = (downloaded / total_size) * 100
                    print(f"\r  Downloaded: {percent:.1f}%", end='', flush=True)
        
        print(f"\n  Saved: {zip_path} ({zip_path.stat().st_size // 1024 // 1024} MB)")
        return zip_path
    
    def _extract_zip(self, zip_path: Path) -> Path:
        """Extract the ZIP file."""
        extract_dir = self.cache_dir / "azure_icons"
        
        # Check if already extracted
        if extract_dir.exists() and any(extract_dir.iterdir()):
            print(f"  Using cached extraction: {extract_dir}")
            return extract_dir
        
        print(f"  Extracting...")
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(extract_dir)
        
        print(f"  Extracted to: {extract_dir}")
        return extract_dir
    
    def fetch(self) -> Path:
        """Download and extract Azure icons."""
        print(f"[{self.display_name}]")
        
        url = self._find_download_url()
        zip_path = self._download_zip(url)
        self._icons_dir = self._extract_zip(zip_path)
        
        return self._icons_dir
    
    def _find_svg_root(self) -> Path:
        """Find the root directory containing SVG category folders."""
        if not self._icons_dir:
            raise RuntimeError("Must call fetch() first")
        
        # Azure ZIP structure varies, find the directory with category folders
        # Usually something like: Azure_Public_Service_Icons_V*/Icons/
        for path in self._icons_dir.rglob('*'):
            if path.is_dir() and path.name == 'Icons':
                return path
        
        # Fallback: look for directories containing SVG files
        for path in self._icons_dir.iterdir():
            if path.is_dir():
                # Check if it contains subdirectories with SVGs
                subdirs = [d for d in path.iterdir() if d.is_dir()]
                if subdirs and any(list(subdirs[0].glob('*.svg'))):
                    return path
        
        raise RuntimeError(f"Could not find SVG root directory in {self._icons_dir}")
    
    def get_categories(self) -> Generator[IconCategory, None, None]:
        """Get Azure icon categories."""
        if not self._icons_dir:
            raise RuntimeError("Must call fetch() first")
        
        svg_root = self._find_svg_root()
        print(f"  SVG root: {svg_root}")
        
        # Each subdirectory is a category
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
    cache_dir = Path("./temp/azure_cache")
    fetcher = AzureFetcher(cache_dir)
    
    fetcher.fetch()
    
    print("\nCategories found:")
    for category in fetcher.get_categories():
        print(f"  - {category.name}: {len(category.svg_files)} icons")
