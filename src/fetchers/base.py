#!/usr/bin/env python3
"""
Base class for icon fetchers.

Each cloud provider (Azure, AWS, GCP, etc.) should implement this interface.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generator


class IconCategory:
    """Represents a category of icons."""
    
    def __init__(self, name: str, svg_files: list[Path]):
        self.name = name
        self.svg_files = svg_files
    
    def __repr__(self) -> str:
        return f"IconCategory(name='{self.name}', count={len(self.svg_files)})"


class BaseFetcher(ABC):
    """Abstract base class for icon fetchers."""
    
    def __init__(self, cache_dir: Path):
        """
        Initialize fetcher.
        
        Args:
            cache_dir: Directory to cache downloaded files
        """
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this icon source (e.g., 'azure', 'aws')."""
        pass
    
    @property
    @abstractmethod
    def display_name(self) -> str:
        """Return the display name (e.g., 'Azure Architecture Icons')."""
        pass
    
    @abstractmethod
    def fetch(self) -> Path:
        """
        Download and extract icons to cache directory.
        
        Returns:
            Path to the extracted icons directory
        """
        pass
    
    @abstractmethod
    def get_categories(self) -> Generator[IconCategory, None, None]:
        """
        Get all icon categories.
        
        Yields:
            IconCategory objects containing category name and SVG files
        """
        pass
    
    def cleanup(self) -> None:
        """Clean up temporary files (optional override)."""
        pass
