"""
CHARUSAT University Data Collector
Phase-based web crawler to collect and structure official university information.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import time
import json
import os
import re
from datetime import datetime
from pathlib import Path
import hashlib

class CHARUSATCrawler:
    """Web crawler for CHARUSAT University official website."""
    
    def __init__(self, base_dir):
        """Initialize crawler with project base directory."""
        self.base_url = "https://charusat.ac.in"
        self.allowed_domains = ["charusat.ac.in"]
        self.base_dir = Path(base_dir)
        
        # Create directory structure
        self.data_dir = self.base_dir / "data"
        self.raw_dir = self.data_dir / "raw"
        self.text_dir = self.data_dir / "text"
        self.text_raw_dir = self.text_dir / "raw"
        self.text_meta_dir = self.text_dir / "meta"
        self.processed_dir = self.data_dir / "processed"
        self.structured_dir = self.data_dir / "structured"
        self.embeddings_dir = self.data_dir / "embeddings"
        self.knowledge_dir = self.base_dir / "backend" / "knowledge"
        self.logs_dir = self.data_dir / "logs"
        self.review_dir = self.data_dir / "review"
        
        for dir_path in [self.raw_dir, self.text_raw_dir, self.text_meta_dir, 
                         self.processed_dir, self.structured_dir, self.embeddings_dir,
                         self.logs_dir, self.review_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Crawler settings
        self.max_concurrent = 2
        self.delay = 1.0  # seconds between requests
        self.max_depth = 6
        self.user_agent = "CHARUSAT-Helpdesk-Crawler/1.0"
        
        # State
        self.visited_urls = set()
        self.discovery_manifest = []
        self.robots_parser = None
        
        # Initialize logging
        self.log_file = self.logs_dir / "collection.log"
        self.log("Crawler initialized", "INFO")
    
    def log(self, message, level="INFO"):
        """Log message to file and console."""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def check_robots_txt(self):
        """Load and parse robots.txt."""
        try:
            self.robots_parser = RobotFileParser()
            self.robots_parser.set_url(urljoin(self.base_url, '/robots.txt'))
            self.robots_parser.read()
            self.log("robots.txt loaded successfully")
            return True
        except Exception as e:
            self.log(f"Failed to load robots.txt: {str(e)}", "WARNING")
            return False
    
    def is_allowed_url(self, url):
        """Check if URL is allowed to crawl."""
        parsed = urlparse(url)
        
        # Check domain
        if not any(domain in parsed.netloc for domain in self.allowed_domains):
            return False
        
        # Check robots.txt
        if self.robots_parser and not self.robots_parser.can_fetch(self.user_agent, url):
            self.log(f"Blocked by robots.txt: {url}", "WARNING")
            return False
        
        return True
    
    def url_to_slug(self, url):
        """Convert URL to safe filename slug."""
        # Create hash of URL for uniqueness
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        
        # Extract path and clean it
        parsed = urlparse(url)
        path = parsed.path.strip('/').replace('/', '_')
        
        # Remove unsafe characters
        safe_path = re.sub(r'[^\w\-]', '_', path)
        safe_path = safe_path[:100]  # Limit length
        
        # Combine clean path with hash
        slug = f"{safe_path}_{url_hash}" if safe_path else url_hash
        
        return slug
    
    def download_file(self, url):
        """Download a file (HTML, PDF, etc.) and save to raw directory."""
        if url in self.visited_urls:
            return None
        
        if not self.is_allowed_url(url):
            self.log(f"URL not allowed: {url}", "WARNING")
            return None
        
        try:
            self.log(f"Downloading: {url}")
            
            headers = {'User-Agent': self.user_agent}
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code != 200:
                self.log(f"HTTP {response.status_code}: {url}", "WARNING")
                return None
            
            # Generate filename
            slug = self.url_to_slug(url)
            content_type = response.headers.get('content-type', '').lower()
            
            if 'pdf' in content_type:
                ext = '.pdf'
            elif 'html' in content_type:
                ext = '.html'
            else:
                ext = '.bin'
            
            filename = f"{slug}{ext}"
            filepath = self.raw_dir / filename
            
            # Save file
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            # Record in manifest
            manifest_entry = {
                "url": url,
                "status_code": response.status_code,
                "content_type": content_type,
                "retrieved_at": datetime.now().isoformat(),
                "last_modified": response.headers.get('last-modified'),
                "file_path": str(filepath.relative_to(self.base_dir)),
                "slug": slug
            }
            
            self.discovery_manifest.append(manifest_entry)
            self.visited_urls.add(url)
            
            self.log(f"Saved: {filename}")
            
            # Respect rate limit
            time.sleep(self.delay)
            
            return manifest_entry
            
        except Exception as e:
            self.log(f"Error downloading {url}: {str(e)}", "ERROR")
            return None
    
    def extract_links(self, html_content, base_url):
        """Extract all internal links from HTML content."""
        links = set()
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            for tag in soup.find_all(['a', 'link']):
                href = tag.get('href')
                if not href:
                    continue
                
                # Make absolute URL
                abs_url = urljoin(base_url, href)
                
                # Clean URL (remove fragment)
                abs_url = abs_url.split('#')[0]
                
                # Check if internal
                if self.is_allowed_url(abs_url):
                    links.add(abs_url)
            
        except Exception as e:
            self.log(f"Error extracting links: {str(e)}", "ERROR")
        
        return links
    
    def crawl_phase_1(self, max_pages=100):
        """
        PHASE 1: Discovery & Crawl
        Crawl the website and collect all pages and documents.
        """
        self.log("=" * 60)
        self.log("STARTING PHASE 1: DISCOVERY & CRAWL")
        self.log("=" * 60)
        
        # Check robots.txt
        self.check_robots_txt()
        
        # Seed URLs
        seed_paths = [
            '/',
            '/admissions',
            '/admission/',
            '/academics',
            '/examination',
            '/student-section',
            '/departments',
            '/news',
            '/notice',
            '/circular',
            '/downloads',
            '/contact',
            '/calendar',
            '/events'
        ]
        
        queue = [urljoin(self.base_url, path) for path in seed_paths]
        pages_crawled = 0
        
        while queue and pages_crawled < max_pages:
            url = queue.pop(0)
            
            if url in self.visited_urls:
                continue
            
            # Download page
            manifest_entry = self.download_file(url)
            
            if not manifest_entry:
                continue
            
            pages_crawled += 1
            
            # If HTML, extract links for further crawling
            if manifest_entry['content_type'] and 'html' in manifest_entry['content_type']:
                try:
                    with open(self.raw_dir / f"{manifest_entry['slug']}.html", 'r', encoding='utf-8', errors='ignore') as f:
                        html_content = f.read()
                    
                    new_links = self.extract_links(html_content, url)
                    
                    for link in new_links:
                        if link not in self.visited_urls and link not in queue:
                            queue.append(link)
                    
                    self.log(f"Found {len(new_links)} links on {url}")
                
                except Exception as e:
                    self.log(f"Error processing HTML: {str(e)}", "ERROR")
            
            self.log(f"Progress: {pages_crawled}/{max_pages} pages crawled, {len(queue)} in queue")
        
        # Save discovery manifest
        manifest_path = self.raw_dir / "discovery_manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(self.discovery_manifest, f, indent=2)
        
        self.log(f"Phase 1 complete. Crawled {len(self.discovery_manifest)} items")
        self.log(f"Manifest saved to: {manifest_path}")
        
        return len(self.discovery_manifest)

def main():
    """Main entry point for crawler."""
    # Use current project directory
    base_dir = Path(__file__).parent
    
    crawler = CHARUSATCrawler(base_dir)
    
    # Run Phase 1
    items_collected = crawler.crawl_phase_1(max_pages=50)  # Start with 50 pages
    
    print(f"\n{'=' * 60}")
    print(f"PHASE 1 COMPLETE")
    print(f"{'=' * 60}")
    print(f"Items collected: {items_collected}")
    print(f"Check: {crawler.raw_dir}/discovery_manifest.json")
    print(f"Logs: {crawler.log_file}")

if __name__ == "__main__":
    main()
