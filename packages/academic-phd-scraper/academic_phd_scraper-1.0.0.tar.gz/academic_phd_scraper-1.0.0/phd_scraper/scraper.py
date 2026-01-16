"""
Main scraper module for Academic Positions website.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Optional, Generator, Dict, Any
from urllib.parse import urljoin, urlencode, quote
import time
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from .models import PhDPosition

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AcademicPositionsScraper:
    """
    Scraper for PhD positions from academicpositions.com
    
    This scraper fetches PhD job listings and extracts detailed information
    including title, university, requirements, deadlines, and more.
    
    Usage:
        >>> scraper = AcademicPositionsScraper()
        >>> positions = scraper.get_phd_positions(max_pages=2)
        >>> for pos in positions:
        ...     print(pos.summary())
    """
    
    BASE_URL = "https://academicpositions.com"
    PHD_LISTINGS_URL = f"{BASE_URL}/jobs/position/phd"
    
    # Available fields for filtering
    AVAILABLE_FIELDS = {
        "engineering": "engineering",
        "computer-science": "computer-science-mf",
        "physics": "physics",
        "chemistry": "chemistry",
        "biology": "biology",
        "mathematics": "mathematics",
        "medicine": "medicine",
        "economics": "economics",
        "social-science": "social-science",
        "geosciences": "geosciences",
        "artificial-intelligence": "artificial-intelligence",
        "machine-learning": "machine-learning",
        "psychology": "psychology",
        "law": "law",
    }
    
    # Available countries for filtering
    AVAILABLE_COUNTRIES = {
        "germany": "germany",
        "sweden": "sweden",
        "belgium": "belgium",
        "switzerland": "switzerland",
        "netherlands": "netherlands",
        "finland": "finland",
        "norway": "norway",
        "austria": "austria",
        "france": "france",
        "united-kingdom": "united-kingdom",
        "united-states": "united-states",
        "italy": "italy",
        "spain": "spain",
        "denmark": "denmark",
        "luxembourg": "luxembourg",
    }
    
    def __init__(
        self,
        request_delay: float = 1.0,
        timeout: int = 30,
        max_retries: int = 3,
        user_agent: Optional[str] = None
    ):
        """
        Initialize the scraper.
        
        Args:
            request_delay: Delay between requests in seconds (be respectful)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            user_agent: Custom user agent string
        """
        self.request_delay = request_delay
        self.timeout = timeout
        self.max_retries = max_retries
        
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": user_agent or (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        })
    
    def _make_request(self, url: str) -> Optional[BeautifulSoup]:
        """
        Make an HTTP request with retry logic.
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if request failed
        """
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                return BeautifulSoup(response.text, "html.parser")
            except requests.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.request_delay * (attempt + 1))
        return None
    
    def build_url(
        self,
        country: Optional[str] = None,
        field: Optional[str] = None,
        page: int = 1
    ) -> str:
        """
        Build the URL for fetching PhD listings with optional filters.
        
        Args:
            country: Filter by country (use AVAILABLE_COUNTRIES keys)
            field: Filter by field (use AVAILABLE_FIELDS keys)
            page: Page number for pagination
            
        Returns:
            Constructed URL string
        """
        url = self.PHD_LISTINGS_URL
        
        # Add country filter
        if country:
            country_slug = self.AVAILABLE_COUNTRIES.get(country.lower(), country.lower())
            url = f"{url}/country/{country_slug}"
        
        # Add field filter
        if field:
            field_slug = self.AVAILABLE_FIELDS.get(field.lower(), field.lower())
            url = f"{url}/field/{field_slug}"
        
        # Add pagination
        if page > 1:
            url = f"{url}?page={page}"
        
        return url
    
    def get_listings_page(
        self,
        country: Optional[str] = None,
        field: Optional[str] = None,
        page: int = 1
    ) -> List[Dict[str, str]]:
        """
        Get a page of PhD listings (basic info only).
        
        Args:
            country: Filter by country
            field: Filter by field
            page: Page number
            
        Returns:
            List of dictionaries with basic job info (title, university, url)
        """
        url = self.build_url(country=country, field=field, page=page)
        logger.info(f"Fetching listings from: {url}")
        
        soup = self._make_request(url)
        if not soup:
            return []
        
        listings = []
        
        # Find all job listing links - they typically contain "/ad/" in the URL
        job_links = soup.find_all("a", href=lambda href: href and "/ad/" in href)
        
        seen_urls = set()
        for link in job_links:
            href = link.get("href", "")
            if not href or href in seen_urls:
                continue
            
            # Build full URL
            job_url = urljoin(self.BASE_URL, href)
            seen_urls.add(href)
            
            # Try to extract basic info from the listing
            title = link.get_text(strip=True)
            if not title or len(title) < 10:
                continue
            
            # Find associated employer info by traversing up to find a container
            university = ""
            location = ""
            deadline = ""
            
            # Search up to 5 parent levels for context
            parent = link.parent
            for _ in range(5):
                if parent is None:
                    break
                
                # Look for employer link nearby
                if not university:
                    employer_link = parent.find("a", href=lambda h: h and "/employer/" in h)
                    if employer_link:
                        university = employer_link.get_text(strip=True)
                
                # Look for location info
                if not location:
                    location_links = parent.find_all("a", href=lambda h: h and "/country/" in h)
                    if location_links:
                        locations = [loc.get_text(strip=True) for loc in location_links]
                        location = ", ".join(locations)
                
                # Look for deadline info in text
                if not deadline:
                    text = parent.get_text()
                    deadline_match = re.search(r"Closing (?:on|in)[:\s]*([^\n]+)", text)
                    if deadline_match:
                        deadline = deadline_match.group(1).strip()
                
                # If we found everything, stop
                if university and location:
                    break
                    
                parent = parent.parent
            
            listings.append({
                "title": title[:200],  # Truncate long titles
                "university": university,
                "location": location,
                "deadline": deadline,
                "url": job_url,
            })
        
        return listings
    
    def get_position_details(self, url: str) -> Optional[PhDPosition]:
        """
        Get detailed information about a specific PhD position.
        
        Args:
            url: URL of the job posting
            
        Returns:
            PhDPosition object with full details
        """
        logger.info(f"Fetching details from: {url}")
        
        soup = self._make_request(url)
        if not soup:
            return None
        
        # Extract title
        title_elem = soup.find("h1")
        title = title_elem.get_text(strip=True) if title_elem else ""
        
        # Extract employer/university
        employer_link = soup.find("a", href=lambda h: h and "/employer/" in h)
        university = employer_link.get_text(strip=True) if employer_link else ""
        employer_url = urljoin(self.BASE_URL, employer_link.get("href")) if employer_link else ""
        
        # Extract location
        location_links = soup.find_all("a", href=lambda h: h and "/country/" in h)
        locations = []
        city = ""
        country = ""
        for loc in location_links[:2]:  # Usually city, then country
            loc_text = loc.get_text(strip=True)
            if loc_text:
                locations.append(loc_text)
        location = ", ".join(locations)
        if len(locations) >= 2:
            city = locations[0].rstrip(",")
            country = locations[1]
        elif len(locations) == 1:
            country = locations[0]
        
        # Extract job details from the sidebar/info box
        deadline = ""
        published_date = ""
        job_type = "PhD"
        fields = []
        apply_url = ""
        
        # Find job details table/section
        detail_text = soup.get_text()
        
        # Extract deadline
        deadline_match = re.search(
            r"Application deadline[:\s]*([^\n]+)|Closing (?:on|in)[:\s]*([^\n]+)",
            detail_text,
            re.IGNORECASE
        )
        if deadline_match:
            deadline = deadline_match.group(1) or deadline_match.group(2)
            deadline = deadline.strip()
        
        # Extract published date
        published_match = re.search(r"Published[:\s]*(\d{4}-\d{2}-\d{2}|\d+ \w+ ago)", detail_text)
        if published_match:
            published_date = published_match.group(1)
        
        # Extract fields
        field_links = soup.find_all("a", href=lambda h: h and "/field/" in h)
        fields = list(set(link.get_text(strip=True) for link in field_links if link.get_text(strip=True)))
        
        # Extract apply URL
        apply_link = soup.find("a", string=re.compile(r"Apply", re.IGNORECASE))
        if apply_link:
            apply_url = apply_link.get("href", "")
        
        # Extract main content sections
        description = ""
        requirements = ""
        benefits = ""
        
        # Look for common section headers
        sections = {}
        current_section = "description"
        
        for elem in soup.find_all(["h2", "h3", "p", "ul", "ol"]):
            text = elem.get_text(strip=True)
            tag = elem.name
            
            if tag in ["h2", "h3"]:
                text_lower = text.lower()
                if any(kw in text_lower for kw in ["description", "about", "position", "project"]):
                    current_section = "description"
                elif any(kw in text_lower for kw in ["profile", "requirement", "qualification", "criteria", "candidate"]):
                    current_section = "requirements"
                elif any(kw in text_lower for kw in ["offer", "benefit", "provide", "we offer"]):
                    current_section = "benefits"
                continue
            
            if text and current_section:
                if current_section not in sections:
                    sections[current_section] = []
                sections[current_section].append(text)
        
        description = "\n".join(sections.get("description", []))
        requirements = "\n".join(sections.get("requirements", []))
        benefits = "\n".join(sections.get("benefits", []))
        
        # If no structured sections found, get all main text
        if not description:
            main_content = soup.find("article") or soup.find("main") or soup.find("div", class_=re.compile(r"content|body"))
            if main_content:
                description = main_content.get_text(separator="\n", strip=True)[:5000]
        
        return PhDPosition(
            title=title,
            university=university,
            location=location,
            country=country,
            city=city,
            deadline=deadline,
            published_date=published_date,
            job_type=job_type,
            fields=fields,
            description=description[:5000] if description else "",
            requirements=requirements[:3000] if requirements else "",
            benefits=benefits[:2000] if benefits else "",
            url=url,
            apply_url=apply_url,
            employer_url=employer_url,
        )
    
    def get_phd_positions(
        self,
        max_pages: int = 5,
        country: Optional[str] = None,
        field: Optional[str] = None,
        fetch_details: bool = True,
        max_workers: int = 3
    ) -> List[PhDPosition]:
        """
        Get PhD positions with optional filtering.
        
        Args:
            max_pages: Maximum number of pages to scrape
            country: Filter by country (e.g., "germany", "sweden")
            field: Filter by field (e.g., "computer-science", "physics")
            fetch_details: Whether to fetch detailed info for each position
            max_workers: Number of concurrent workers for fetching details
            
        Returns:
            List of PhDPosition objects
        """
        all_positions = []
        
        for page in range(1, max_pages + 1):
            logger.info(f"Fetching page {page}/{max_pages}")
            
            listings = self.get_listings_page(country=country, field=field, page=page)
            
            if not listings:
                logger.info(f"No more listings found on page {page}")
                break
            
            if fetch_details:
                # Fetch details concurrently
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    future_to_listing = {
                        executor.submit(self.get_position_details, listing["url"]): listing
                        for listing in listings
                    }
                    
                    for future in as_completed(future_to_listing):
                        listing = future_to_listing[future]
                        try:
                            position = future.result()
                            if position:
                                all_positions.append(position)
                        except Exception as e:
                            logger.error(f"Error fetching details for {listing['url']}: {e}")
                        
                        time.sleep(self.request_delay)
            else:
                # Just create positions from basic listing info
                for listing in listings:
                    position = PhDPosition(
                        title=listing["title"],
                        university=listing["university"],
                        location=listing["location"],
                        deadline=listing["deadline"],
                        url=listing["url"],
                    )
                    all_positions.append(position)
            
            # Respect rate limiting
            time.sleep(self.request_delay)
        
        logger.info(f"Total positions found: {len(all_positions)}")
        return all_positions
    
    def search_positions(
        self,
        keywords: Optional[List[str]] = None,
        country: Optional[str] = None,
        field: Optional[str] = None,
        max_pages: int = 5
    ) -> List[PhDPosition]:
        """
        Search for PhD positions matching specific keywords.
        
        Args:
            keywords: List of keywords to search for in titles/descriptions
            country: Filter by country
            field: Filter by field
            max_pages: Maximum number of pages to search
            
        Returns:
            List of matching PhDPosition objects
        """
        positions = self.get_phd_positions(
            max_pages=max_pages,
            country=country,
            field=field,
            fetch_details=True
        )
        
        if not keywords:
            return positions
        
        # Filter by keywords
        keywords_lower = [kw.lower() for kw in keywords]
        matching = []
        
        for pos in positions:
            searchable = f"{pos.title} {pos.description} {pos.requirements}".lower()
            if any(kw in searchable for kw in keywords_lower):
                matching.append(pos)
        
        return matching
    
    def iter_positions(
        self,
        country: Optional[str] = None,
        field: Optional[str] = None,
        fetch_details: bool = True
    ) -> Generator[PhDPosition, None, None]:
        """
        Iterator that yields PhD positions one at a time.
        
        Useful for processing large numbers of positions without
        loading everything into memory.
        
        Args:
            country: Filter by country
            field: Filter by field
            fetch_details: Whether to fetch detailed info
            
        Yields:
            PhDPosition objects
        """
        page = 1
        while True:
            listings = self.get_listings_page(country=country, field=field, page=page)
            
            if not listings:
                break
            
            for listing in listings:
                if fetch_details:
                    position = self.get_position_details(listing["url"])
                    if position:
                        yield position
                else:
                    yield PhDPosition(
                        title=listing["title"],
                        university=listing["university"],
                        location=listing["location"],
                        deadline=listing["deadline"],
                        url=listing["url"],
                    )
                
                time.sleep(self.request_delay)
            
            page += 1
            time.sleep(self.request_delay)
    
    @staticmethod
    def list_available_countries() -> List[str]:
        """Return list of available country filters."""
        return list(AcademicPositionsScraper.AVAILABLE_COUNTRIES.keys())
    
    @staticmethod
    def list_available_fields() -> List[str]:
        """Return list of available field filters."""
        return list(AcademicPositionsScraper.AVAILABLE_FIELDS.keys())
