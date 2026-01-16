# PhD Scraper for Academic Positions

A Python module to scrape PhD offers from [academicpositions.com](https://academicpositions.com).

## Features

- 🔍 Scrape PhD positions with filtering by country and field
- 📋 Extract detailed information: title, university, requirements, deadlines, etc.
- 💾 Export to JSON, CSV, or Markdown formats
- 🔄 Iterator support for memory-efficient processing
- ⚡ Concurrent fetching with rate limiting
- 🖥️ Command-line interface included

## Installation

```bash
# Clone or navigate to the project directory
cd PhDFinder

# Install dependencies
pip install -e .

# Or install dependencies directly
pip install requests beautifulsoup4
```

## Quick Start

### Python API

```python
from phd_scraper import AcademicPositionsScraper, PhDPosition

# Create scraper instance
scraper = AcademicPositionsScraper()

# Get PhD positions (basic usage)
positions = scraper.get_phd_positions(max_pages=2)

# Print results
for pos in positions:
    print(f"{pos.title} at {pos.university}")
    print(f"  Location: {pos.location}")
    print(f"  Deadline: {pos.deadline}")
    print(f"  URL: {pos.url}")
    print()
```

### Filter by Country and Field

```python
# Get Computer Science PhDs in Germany
positions = scraper.get_phd_positions(
    max_pages=3,
    country="germany",
    field="computer-science"
)

# Get Physics PhDs in Switzerland
positions = scraper.get_phd_positions(
    country="switzerland",
    field="physics"
)
```

### Search with Keywords

```python
# Search for specific keywords
positions = scraper.search_positions(
    keywords=["machine learning", "deep learning", "AI"],
    country="germany",
    max_pages=5
)
```

### Export Results

```python
from phd_scraper.utils import export_to_json, export_to_csv, export_to_markdown

# Get positions
positions = scraper.get_phd_positions(max_pages=2)

# Export to different formats
export_to_json(positions, "phd_positions.json")
export_to_csv(positions, "phd_positions.csv")
export_to_markdown(positions, "phd_positions.md")
```

### Memory-Efficient Iterator

```python
# Process positions one at a time (good for large datasets)
for position in scraper.iter_positions(country="sweden"):
    print(position.summary())
    # Process each position without loading all into memory
```

## Command-Line Interface

```bash
# Basic usage - get 2 pages of positions
python -m phd_scraper --pages 2

# Filter by country and field
python -m phd_scraper --country germany --field computer-science

# Export to JSON
python -m phd_scraper --output positions.json --format json --pages 3

# Export to CSV
python -m phd_scraper --output positions.csv --format csv

# Search with keywords
python -m phd_scraper --keywords "machine learning" "neural networks" --pages 5

# List available filters
python -m phd_scraper --list-filters

# Fast mode (skip detailed info)
python -m phd_scraper --no-details --pages 10

# Verbose output
python -m phd_scraper --verbose --pages 1
```

## Available Filters

### Countries
- germany, sweden, belgium, switzerland, netherlands, finland
- norway, austria, france, united-kingdom, united-states
- italy, spain, denmark, luxembourg

### Fields
- computer-science, physics, chemistry, biology, mathematics
- engineering, medicine, economics, social-science, geosciences
- artificial-intelligence, machine-learning, psychology, law

## Data Model

Each `PhDPosition` object contains:

| Field | Description |
|-------|-------------|
| `title` | Position title |
| `university` | University/employer name |
| `location` | Full location (city, country) |
| `country` | Country name |
| `city` | City name |
| `deadline` | Application deadline |
| `published_date` | When the position was published |
| `job_type` | Type of position (PhD) |
| `fields` | Research fields/disciplines |
| `description` | Full job description |
| `requirements` | Qualifications needed |
| `benefits` | What the position offers |
| `url` | Link to the job posting |
| `apply_url` | Direct application link |

## Configuration

```python
scraper = AcademicPositionsScraper(
    request_delay=1.5,      # Delay between requests (seconds)
    timeout=30,             # Request timeout (seconds)
    max_retries=3,          # Number of retry attempts
    user_agent="Custom UA"  # Custom user agent string
)
```

## Utility Functions

```python
from phd_scraper.utils import (
    filter_positions,
    deduplicate_positions,
    sort_positions
)

# Filter positions
filtered = filter_positions(
    positions,
    keywords=["AI", "robotics"],
    countries=["germany", "switzerland"],
    has_deadline=True
)

# Remove duplicates
unique = deduplicate_positions(positions)

# Sort by field
sorted_pos = sort_positions(positions, by="deadline")
```

## Example Output

```
[1] PhD Position in AI and Strategy
    University: ETH Zürich
    Location: Zurich, Switzerland
    Deadline: Unspecified
    Fields: Business Administration, Management, Artificial Intelligence
    URL: https://academicpositions.com/ad/eth-zurich/2026/...

[2] Doctoral student in Radiofrequency ranging for Lunar orbits
    University: KTH Royal Institute of Technology
    Location: Stockholm, Sweden
    Deadline: 2026-01-31 (Europe/Stockholm)
    Fields: Physics, Space Science
    URL: https://academicpositions.com/ad/kth-royal-institute-of-technology/2025/...
```

## Important Notes

- **Rate Limiting**: The scraper includes built-in delays to be respectful of the server
- **Terms of Service**: Please review academicpositions.com's terms before scraping
- **Data Accuracy**: Always verify position details on the original website
- **Updates**: Website structure may change; report issues if scraping fails

## License

MIT License
