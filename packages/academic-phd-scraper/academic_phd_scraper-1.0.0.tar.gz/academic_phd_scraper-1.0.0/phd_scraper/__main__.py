"""
Command-line interface for the PhD scraper.
"""

import argparse
import sys
import logging
from typing import Optional

from .scraper import AcademicPositionsScraper
from .utils import (
    export_to_json,
    export_to_csv,
    export_to_markdown,
    filter_positions,
    deduplicate_positions,
    sort_positions
)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Scrape PhD positions from academicpositions.com",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get 2 pages of PhD positions
  python -m phd_scraper --pages 2

  # Filter by country and field
  python -m phd_scraper --country germany --field computer-science

  # Export to JSON
  python -m phd_scraper --output positions.json --format json

  # Export to CSV with specific fields
  python -m phd_scraper --output positions.csv --format csv

  # Search with keywords
  python -m phd_scraper --keywords "machine learning" "AI" --pages 3

  # List available countries and fields
  python -m phd_scraper --list-filters
        """
    )
    
    parser.add_argument(
        "--pages", "-p",
        type=int,
        default=1,
        help="Number of pages to scrape (default: 1)"
    )
    
    parser.add_argument(
        "--country", "-c",
        type=str,
        help="Filter by country (e.g., germany, sweden, switzerland)"
    )
    
    parser.add_argument(
        "--field", "-f",
        type=str,
        help="Filter by field (e.g., computer-science, physics, biology)"
    )
    
    parser.add_argument(
        "--keywords", "-k",
        nargs="+",
        help="Keywords to search for in positions"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file path"
    )
    
    parser.add_argument(
        "--format",
        choices=["json", "csv", "markdown", "text"],
        default="text",
        help="Output format (default: text)"
    )
    
    parser.add_argument(
        "--no-details",
        action="store_true",
        help="Skip fetching detailed information (faster)"
    )
    
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between requests in seconds (default: 1.0)"
    )
    
    parser.add_argument(
        "--sort",
        choices=["title", "university", "deadline", "country"],
        help="Sort results by field"
    )
    
    parser.add_argument(
        "--list-filters",
        action="store_true",
        help="List available country and field filters"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress output"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    if args.quiet:
        logging.disable(logging.CRITICAL)
    elif args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    # List filters and exit
    if args.list_filters:
        print("\nAvailable Countries:")
        for country in sorted(AcademicPositionsScraper.list_available_countries()):
            print(f"  - {country}")
        
        print("\nAvailable Fields:")
        for field in sorted(AcademicPositionsScraper.list_available_fields()):
            print(f"  - {field}")
        return 0
    
    # Create scraper
    scraper = AcademicPositionsScraper(request_delay=args.delay)
    
    # Fetch positions
    try:
        positions = scraper.get_phd_positions(
            max_pages=args.pages,
            country=args.country,
            field=args.field,
            fetch_details=not args.no_details
        )
    except Exception as e:
        print(f"Error fetching positions: {e}", file=sys.stderr)
        return 1
    
    # Filter by keywords if specified
    if args.keywords:
        positions = filter_positions(positions, keywords=args.keywords)
    
    # Remove duplicates
    positions = deduplicate_positions(positions)
    
    # Sort if specified
    if args.sort:
        positions = sort_positions(positions, by=args.sort)
    
    # Output results
    if not positions:
        print("No positions found.", file=sys.stderr)
        return 0
    
    if args.output:
        if args.format == "json":
            filepath = export_to_json(positions, args.output)
            print(f"Exported {len(positions)} positions to {filepath}")
        elif args.format == "csv":
            filepath = export_to_csv(positions, args.output)
            print(f"Exported {len(positions)} positions to {filepath}")
        elif args.format == "markdown":
            filepath = export_to_markdown(positions, args.output)
            print(f"Exported {len(positions)} positions to {filepath}")
        else:
            with open(args.output, "w") as f:
                for pos in positions:
                    f.write(str(pos) + "\n\n")
            print(f"Exported {len(positions)} positions to {args.output}")
    else:
        # Print to stdout
        print(f"\n{'='*60}")
        print(f"Found {len(positions)} PhD positions")
        print(f"{'='*60}\n")
        
        for i, pos in enumerate(positions, 1):
            print(f"[{i}] {pos.title}")
            print(f"    University: {pos.university}")
            if pos.location:
                print(f"    Location: {pos.location}")
            if pos.deadline:
                print(f"    Deadline: {pos.deadline}")
            if pos.fields:
                print(f"    Fields: {', '.join(pos.fields[:3])}")
            print(f"    URL: {pos.url}")
            print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
