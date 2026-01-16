"""
PhD Scraper Module for Academic Positions

This module provides tools to scrape PhD offers from academicpositions.com
and extract relevant information such as title, university, requirements,
deadlines, and other details.
"""

from .scraper import AcademicPositionsScraper
from .models import PhDPosition

__version__ = "1.0.0"
__all__ = ["AcademicPositionsScraper", "PhDPosition"]
