# Medspa Lead Generation Project

This project automates the process of generating and qualifying leads for medspa businesses, focusing on treatments like RF microneedling, Morpheus8, Potenza, Sylfirm, Kybella, and other fat reduction procedures.

## Overview

The lead generation pipeline consists of four main phases:

1. **Data Collection (Phase 1)**: Fetches medspa business data from Google Places using the Apify API for specified locations.

2. **Data Enrichment (Phase 3)**: Enhances existing business data by extracting contact information (emails, Instagram handles) from business websites.

3. **Lead Filtering (Phase 2)**: Filters businesses based on relevant keywords related to medspa treatments and services.

4. **Lead Scoring (Phase 4)**: Assigns scores to qualified leads based on various criteria including qualification status and contact information availability.

## Features

- Automated data enrichment from business websites
- Keyword-based filtering for medspa-relevant businesses
- Lead scoring system for prioritization
- Integration with Baserow database for data storage and management
- Robust error handling and retry mechanisms

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd medspa_lead_gen_project
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your credentials:
   ```
   BASEROW_API_KEY=your_api_key_here
   TABLE_ID=your_table_id_here
   APIFY_API_TOKEN=your_apify_token_here
   ```

## Usage

Run the complete pipeline using the main script:

```bash
python final_main.py
```

This will execute the pipeline in the following order:
- Phase 3: Data enrichment
- Phase 2: Lead filtering
- Phase 4: Lead scoring

To run the initial data collection phase separately:

```bash
python main.py
```

This fetches medspa data from Google Places and saves it to your Baserow table.

## Requirements

- Python 3.7+
- Baserow account and API access
- Internet connection for web scraping

## Dependencies

- requests: For HTTP requests
- beautifulsoup4: For HTML parsing
- python-dotenv: For environment variable management
- urllib3: For HTTP handling

## Environment Variables

- `BASEROW_API_KEY`: Your Baserow API token
- `TABLE_ID`: The ID of your Baserow table for storing lead data
- `APIFY_API_TOKEN`: Your Apify API token for Google Places data fetching
