"""
Utility functions and exporters for PhD scraper.
"""

import json
import csv
from typing import List, Optional
from pathlib import Path
from datetime import datetime

from .models import PhDPosition


def export_to_json(
    positions: List[PhDPosition],
    filepath: str,
    indent: int = 2
) -> str:
    """
    Export PhD positions to a JSON file.
    
    Args:
        positions: List of PhDPosition objects
        filepath: Output file path
        indent: JSON indentation level
        
    Returns:
        Path to the exported file
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        "exported_at": datetime.now().isoformat(),
        "total_positions": len(positions),
        "positions": [pos.to_dict() for pos in positions]
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    
    return str(filepath)


def export_to_csv(
    positions: List[PhDPosition],
    filepath: str,
    fields: Optional[List[str]] = None
) -> str:
    """
    Export PhD positions to a CSV file.
    
    Args:
        positions: List of PhDPosition objects
        filepath: Output file path
        fields: Optional list of fields to include (defaults to all)
        
    Returns:
        Path to the exported file
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    if not positions:
        return str(filepath)
    
    # Default fields if not specified
    if fields is None:
        fields = [
            "title", "university", "location", "country", "city",
            "deadline", "published_date", "fields", "url", "apply_url"
        ]
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        
        for pos in positions:
            row = pos.to_dict()
            # Convert list fields to strings
            if "fields" in row and isinstance(row["fields"], list):
                row["fields"] = "; ".join(row["fields"])
            writer.writerow(row)
    
    return str(filepath)


def export_to_markdown(
    positions: List[PhDPosition],
    filepath: str
) -> str:
    """
    Export PhD positions to a Markdown file.
    
    Args:
        positions: List of PhDPosition objects
        filepath: Output file path
        
    Returns:
        Path to the exported file
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    lines = [
        "# PhD Positions from Academic Positions",
        "",
        f"*Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        f"*Total positions: {len(positions)}*",
        "",
        "---",
        ""
    ]
    
    for i, pos in enumerate(positions, 1):
        lines.extend([
            f"## {i}. {pos.title}",
            "",
            f"**University:** {pos.university}",
            f"**Location:** {pos.location}" if pos.location else "",
            f"**Deadline:** {pos.deadline}" if pos.deadline else "",
            f"**Fields:** {', '.join(pos.fields)}" if pos.fields else "",
            "",
            f"[View Position]({pos.url})" if pos.url else "",
            "",
            "---",
            ""
        ])
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(line for line in lines if line or lines[lines.index(line)-1] == ""))
    
    return str(filepath)


def filter_positions(
    positions: List[PhDPosition],
    keywords: Optional[List[str]] = None,
    countries: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
    has_deadline: bool = False
) -> List[PhDPosition]:
    """
    Filter PhD positions based on various criteria.
    
    Args:
        positions: List of PhDPosition objects
        keywords: Keywords to search in title/description
        countries: Filter by countries
        fields: Filter by research fields
        has_deadline: Only include positions with deadlines
        
    Returns:
        Filtered list of PhDPosition objects
    """
    result = positions
    
    if keywords:
        keywords_lower = [kw.lower() for kw in keywords]
        result = [
            p for p in result
            if any(kw in p.title.lower() or kw in p.description.lower() for kw in keywords_lower)
        ]
    
    if countries:
        countries_lower = [c.lower() for c in countries]
        result = [
            p for p in result
            if p.country.lower() in countries_lower or 
               any(c in p.location.lower() for c in countries_lower)
        ]
    
    if fields:
        fields_lower = [f.lower() for f in fields]
        result = [
            p for p in result
            if any(f in [pf.lower() for pf in p.fields] for f in fields_lower) or
               any(f in p.title.lower() or f in p.description.lower() for f in fields_lower)
        ]
    
    if has_deadline:
        result = [p for p in result if p.deadline]
    
    return result


def deduplicate_positions(positions: List[PhDPosition]) -> List[PhDPosition]:
    """
    Remove duplicate positions based on URL.
    
    Args:
        positions: List of PhDPosition objects
        
    Returns:
        Deduplicated list of PhDPosition objects
    """
    seen_urls = set()
    unique = []
    
    for pos in positions:
        if pos.url not in seen_urls:
            seen_urls.add(pos.url)
            unique.append(pos)
    
    return unique


def sort_positions(
    positions: List[PhDPosition],
    by: str = "title",
    reverse: bool = False
) -> List[PhDPosition]:
    """
    Sort PhD positions by a specific field.
    
    Args:
        positions: List of PhDPosition objects
        by: Field to sort by (title, university, deadline, country)
        reverse: Sort in descending order
        
    Returns:
        Sorted list of PhDPosition objects
    """
    key_funcs = {
        "title": lambda p: p.title.lower(),
        "university": lambda p: p.university.lower(),
        "deadline": lambda p: p.deadline or "zzz",  # Put empty deadlines at end
        "country": lambda p: p.country.lower(),
        "published": lambda p: p.published_date or "",
    }
    
    key_func = key_funcs.get(by, key_funcs["title"])
    return sorted(positions, key=key_func, reverse=reverse)
