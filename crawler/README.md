# CHARUSAT Data Collector

Automated web crawler to collect official information from CHARUSAT University website and populate the helpdesk knowledge base.

## Features

- ✅ Respects robots.txt
- ✅ Rate-limited (1 second between requests)
- ✅ Crawls only charusat.ac.in domain
- ✅ Downloads HTML pages and PDFs
- ✅ Extracts and categorizes content
- ✅ Generates structured knowledge files

## Quick Start

**1. Install dependencies:**
```bash
cd crawler
pip install -r requirements.txt
```

**2. Run Phase 1 (Discovery & Crawl):**
```bash
python charusat_crawler.py
```

This will:
- Crawl up to 50 pages from charusat.ac.in
- Save raw HTML/PDF files to `data/raw/`
- Generate `data/raw/discovery_manifest.json`
- Create logs in `data/logs/collection.log`

**3. Check results:**
- Manifest: `data/raw/discovery_manifest.json`
- Raw files: `data/raw/*.html`, `data/raw/*.pdf`
- Logs: `data/logs/collection.log`

## Directory Structure

```
university-helpdesk/
├── crawler/
│   ├── charusat_crawler.py      # Main crawler script
│   ├── requirements.txt          # Dependencies
│   └── README.md                 # This file
│
├── data/                         # Collected data
│   ├── raw/                     # Raw downloaded files
│   │   ├── discovery_manifest.json
│   │   ├── *.html
│   │   └── *.pdf
│   ├── text/                    # Extracted text
│   │   ├── raw/                 # Raw extracted text
│   │   └── meta/                # Metadata JSON files
│   ├── processed/               # Categorized data
│   ├── structured/              # Structured JSON data
│   ├── embeddings/              # Chunked data for RAG
│   ├── logs/                    # Crawler logs
│   └── review/                  # Human review batches
│
└── backend/knowledge/           # Final knowledge base
    ├── text/                    # Text knowledge files
    └── pdfs/                    # PDF knowledge files
```

## Phased Execution

### Phase 1: Discovery & Crawl ✅ IMPLEMENTED
- Crawls charusat.ac.in
- Downloads HTML and PDF files
- Creates discovery manifest
- **Output:** `data/raw/discovery_manifest.json`

### Phase 2: Extract & Store Text (TODO)
- Extract text from HTML and PDFs
- Save as UTF-8 .txt files
- Generate metadata
- **Output:** `data/text/raw/*.txt`, `data/text/meta/*.json`

### Phase 3: Categorize & Map (TODO)
- Classify content (admissions, exams, fees, etc.)
- Keyword-based categorization
- **Output:** `data/processed/categorization.csv`

### Phase 4: Clean & Normalize (TODO)
- Remove boilerplate
- Normalize dates and names
- Extract key fields
- **Output:** `data/structured/*.jsonl`

### Phase 5: Summarize & Structure (TODO)
- Generate summaries
- Extract key facts
- **Output:** `data/structured/*.jsonl`

### Phase 6: Prepare for RAG (TODO)
- Chunk documents
- Generate embeddings input
- Create knowledge files
- **Output:** `data/embeddings/chunks.jsonl`, `backend/knowledge/text/*.txt`

### Phase 7: Review & Continuous Collection (TODO)
- Human review batches
- Incremental updates
- **Output:** `data/review/*.csv`

## Configuration

Edit `charusat_crawler.py` to adjust:
- `max_concurrent`: Concurrent requests (default: 2)
- `delay`: Delay between requests in seconds (default: 1.0)
- `max_depth`: Maximum crawl depth (default: 6)
- `max_pages`: Maximum pages to crawl (default: 50)

## Safety Features

- ✅ Respects robots.txt directives
- ✅ Rate limiting to avoid server overload
- ✅ Domain whitelisting (only charusat.ac.in)
- ✅ Comprehensive logging
- ✅ Error handling and retry logic

## Usage Examples

**Crawl limited pages (testing):**
```python
crawler.crawl_phase_1(max_pages=10)
```

**Crawl full site:**
```python
crawler.crawl_phase_1(max_pages=500)
```

**Change rate limit:**
```python
crawler.delay = 2.0  # 2 seconds between requests
```

## Monitoring

**Check logs:**
```bash
tail -f data/logs/collection.log
```

**View manifest:**
```bash
cat data/raw/discovery_manifest.json | python -m json.tool
```

**Count collected items:**
```bash
# Windows PowerShell
(Get-Content data/raw/discovery_manifest.json | ConvertFrom-Json).Count
```

## Troubleshooting

**Issue: "Connection refused"**
- Check internet connection
- Verify charusat.ac.in is accessible
- Check if behind firewall/proxy

**Issue: "Blocked by robots.txt"**
- Normal behavior - respecting site rules
- Check logs for allowed paths

**Issue: "Too many requests"**
- Increase delay: `crawler.delay = 2.0`
- Reduce max_concurrent: `crawler.max_concurrent = 1`

## Next Steps

After Phase 1 completes:
1. Review `data/raw/discovery_manifest.json`
2. Check sample downloaded files
3. Proceed to Phase 2 (text extraction)
4. Implement remaining phases

## Legal & Ethical

- Only collects publicly available information
- Respects robots.txt
- Rate-limited to avoid server stress
- For educational/academic use only
- Content belongs to CHARUSAT University

## Contact

For issues or questions about the crawler, check the logs first.
