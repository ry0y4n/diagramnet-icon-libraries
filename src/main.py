#!/usr/bin/env python3
"""
diagrams.net Icon Library Generator

Main script to fetch icons from various sources and generate
diagrams.net custom library XML files.
"""

import argparse
import shutil
from pathlib import Path

from src.fetchers.azure import AzureFetcher
from src.fetchers.dynamics365 import Dynamics365Fetcher
from src.fetchers.entra import EntraFetcher
from src.fetchers.fabric import FabricFetcher
from src.fetchers.microsoft365 import Microsoft365Fetcher
from src.converters.svg_to_drawio import (
    create_library_entry_from_file,
    create_library_xml,
)


def _safe_filename(name: str) -> str:
    safe = name.lower().strip()
    safe = safe.replace("&", "and").replace("+", "and")
    safe = "-".join(safe.split())
    safe = "".join(c for c in safe if c.isalnum() or c == "-")
    return safe.strip("-") or "category"


def generate_libraries(fetcher, output_dir: Path) -> dict:
    """Generate diagrams.net libraries for all categories of a fetcher."""
    fetcher.fetch()

    provider_output = output_dir / fetcher.name
    provider_output.mkdir(parents=True, exist_ok=True)

    stats = {
        "categories": 0,
        "icons": 0,
        "files": [],
    }

    print("\nGenerating libraries...")

    for category in fetcher.get_categories():
        safe_name = _safe_filename(category.name)
        output_path = provider_output / f"{safe_name}.xml"

        entries = []
        for svg_file in category.svg_files:
            try:
                entry = create_library_entry_from_file(svg_file)
                entries.append(entry)
            except Exception as e:
                print(f"    ✗ {svg_file.name}: {e}")

        if entries:
            library_xml = create_library_xml(entries)
            output_path.write_text(library_xml, encoding="utf-8")

            stats["categories"] += 1
            stats["icons"] += len(entries)
            stats["files"].append(str(output_path.relative_to(output_dir.parent)))

            print(f"  ✓ {category.name}: {len(entries)} icons → {output_path.name}")

    return stats


def generate_index_json(output_dir: Path, providers: dict) -> None:
    """Generate an index.json file listing all available libraries."""
    import json

    index_path = output_dir / "index.json"
    index_path.write_text(json.dumps(providers, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Generated index: {index_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Draw.io custom icon libraries"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path("output"),
        help="Output directory for generated XML files"
    )
    parser.add_argument(
        "--cache", "-c",
        type=Path,
        default=Path("temp"),
        help="Cache directory for downloaded files"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean cache after generation"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Draw.io Icon Library Generator")
    print("=" * 60)

    providers_index: dict[str, dict] = {}

    # Generate Azure libraries
    azure_stats = generate_libraries(
        AzureFetcher(args.cache / "azure"),
        args.output,
    )
    providers_index["azure"] = {
        "name": "Azure Architecture Icons",
        "categories": azure_stats["files"],
        "total_icons": azure_stats["icons"],
    }

    # Generate Microsoft 365 libraries
    m365_stats = generate_libraries(
        Microsoft365Fetcher(args.cache / "microsoft365"),
        args.output,
    )
    providers_index["microsoft365"] = {
        "name": "Microsoft 365 Architecture Icons",
        "categories": m365_stats["files"],
        "total_icons": m365_stats["icons"],
    }

    # Generate Dynamics 365 libraries
    dynamics365_stats = generate_libraries(
        Dynamics365Fetcher(args.cache / "dynamics365"),
        args.output,
    )
    providers_index["dynamics365"] = {
        "name": "Microsoft Dynamics 365 Icons",
        "categories": dynamics365_stats["files"],
        "total_icons": dynamics365_stats["icons"],
    }

    # Generate Fabric libraries
    fabric_stats = generate_libraries(
        FabricFetcher(args.cache / "fabric"),
        args.output,
    )
    providers_index["fabric"] = {
        "name": "Microsoft Fabric Icons",
        "categories": fabric_stats["files"],
        "total_icons": fabric_stats["icons"],
    }

    # Generate Entra libraries
    entra_stats = generate_libraries(
        EntraFetcher(args.cache / "entra"),
        args.output,
    )
    providers_index["entra"] = {
        "name": "Microsoft Entra Architecture Icons",
        "categories": entra_stats["files"],
        "total_icons": entra_stats["icons"],
    }

    # Generate index
    generate_index_json(args.output, providers_index)

    print("\n" + "=" * 60)
    print("Summary:")
    for provider_id, meta in providers_index.items():
        print(f"  {provider_id}: {meta['total_icons']} icons, {len(meta['categories'])} categories")
    print(f"  Output: {args.output.absolute()}")
    print("=" * 60)
    
    if args.clean:
        print("\nCleaning cache...")
        shutil.rmtree(args.cache, ignore_errors=True)
        print("  Done.")


if __name__ == "__main__":
    main()
