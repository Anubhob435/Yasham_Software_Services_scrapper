# Web Scrapping Tools Collection

This repository contains automated web scrapping tools for extracting data from different websites. Currently includes two specialized scrappers for environmental and retail data extraction.

## 📋 Table of Contents

- [Overview](#overview)
- [Scrappers](#scrappers)
  - [Earth911 Electronics Recycling Scrapper](#earth911-electronics-recycling-scrapper)
  - [Best Buy Store Locator Scrapper](#best-buy-store-locator-scrapper)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Output Files](#output-files)
- [Features](#features)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Overview

This collection provides automated tools for extracting valuable data from web sources:
- **Environmental Data**: Electronics recycling facilities from Earth911.com
- **Retail Data**: Best Buy store locations and details

Both tools use Selenium WebDriver for robust web automation and export data in CSV format for easy analysis.

## 🔧 Scrappers

### Earth911 Electronics Recycling Scrapper (`earth911_scrapper.py`)

Extracts electronics recycling facility data from Earth911.com search results.

**What it does:**
- Searches for electronics recycling facilities near ZIP code 10001
- Extracts data from multiple pages (up to 5 pages)
- Handles popups and dynamic content automatically
- Sets search distance to 100 miles for comprehensive coverage

**Data Extracted:**
- Business Name
- Last Update Date (26-07-2025)
- Street Address (full address with city/state)
- Materials Accepted (semicolon-separated list)

**Output:** `data.csv` + `extraction_metadata.json`

### Best Buy Store Locator Scrapper (`bsestBut_scrapper.py`)

Extracts Best Buy store location data from their store locator.

**What it does:**
- Navigates to Best Buy store locator
- Searches for stores near ZIP code 10001
- Extracts comprehensive store information
- Handles dynamic content loading

**Data Extracted:**
- Store ID
- Store Name
- Distance from search location
- Street Address
- City, State, ZIP
- Full Address (combined)
- Business Hours
- Store Details URL
- Phone Number (when available)

**Output:** `bestbuy_stores.csv`

## 📋 Prerequisites

- **Python 3.7+**
- **Google Chrome Browser** (latest version recommended)
- **ChromeDriver** (included in repository)
- **Internet Connection**

## 🚀 Installation

1. **Clone or download this repository**
   ```bash
   git clone [repository-url]
   cd Yasham_Software_Services_scrapper
   ```

2. **Install required Python packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify ChromeDriver**
   - ChromeDriver executable (`chromedriver.exe`) should be in the root directory
   - Ensure it matches your Chrome browser version

## 💻 Usage

### Running Earth911 Scrapper

```bash
python earth911_scrapper.py
```

**Process:**
1. Opens Earth911.com search page
2. Fills search form (Electronics, ZIP: 10001)
3. Sets distance to 100 miles
4. Handles any popups that appear
5. Extracts data from up to 5 pages
6. Saves results to CSV file

### Running Best Buy Scrapper

```bash
python bsestBut_scrapper.py
```

**Process:**
1. Opens Best Buy store locator
2. Enters ZIP code 10001
3. Clicks Update button
4. Waits for results to load
5. Extracts all store data
6. Saves results to CSV file

## 📄 Output Files

### Earth911 Scrapper Output

**`data.csv`** - Main data file with columns:
- `business_name`: Name of recycling facility
- `last_update_date`: Date of data extraction (26-07-2025)
- `street_address`: Complete address
- `materials_accepted`: Accepted materials (semicolon-separated)

**`extraction_metadata.json`** - Metadata file containing:
- Source information
- Extraction parameters
- Total records count
- Field descriptions

### Best Buy Scrapper Output

**`bestbuy_stores.csv`** - Store data with columns:
- `store_id`: Unique Best Buy store identifier
- `store_name`: Store name/location
- `distance`: Distance from search ZIP code
- `street_address`: Store street address
- `city_state_zip`: City, state, and ZIP code
- `full_address`: Complete formatted address
- `hours`: Current business hours
- `details_url`: Link to store details page
- `phone`: Store phone number (when available)

## ✨ Features

### Common Features (Both Scrappers)
- **Robust Error Handling**: Continues extraction even if individual items fail
- **Multiple Selector Fallbacks**: Uses backup CSS selectors for reliability
- **Debug Screenshots**: Captures screenshots for troubleshooting
- **CSV Output**: Easy-to-analyze data format
- **UTF-8 Encoding**: Proper handling of special characters
- **Progress Reporting**: Real-time extraction status updates

### Earth911 Specific Features
- **Multi-page Extraction**: Automatically navigates through result pages
- **Popup Management**: Detects and closes advertising popups
- **Distance Control**: Sets search radius to 100 miles
- **Material Parsing**: Extracts and formats accepted materials list
- **Metadata Generation**: Creates detailed extraction log

### Best Buy Specific Features
- **Form Automation**: Automatically fills search forms
- **Dynamic Content Handling**: Waits for AJAX-loaded content
- **Phone Number Extraction**: Parses phone numbers from embedded scripts
- **Store Detail Links**: Captures direct links to individual store pages

## 🔧 Technical Details

### Dependencies
- `selenium`: Web automation framework
- `csv`: CSV file handling
- `json`: JSON data processing
- `time`: Timing and delays
- `os`: File system operations
- `re`: Regular expressions for data parsing

### Browser Configuration
- Uses Chrome WebDriver in normal mode (not headless)
- Includes explicit waits for element loading
- Handles dynamic content with appropriate delays

### Error Handling Strategy
- Individual item failures don't stop the entire process
- Multiple selector strategies for element finding
- Screenshot capture for debugging failed operations
- Graceful degradation when optional data isn't available

## 🔍 Troubleshooting

### Common Issues

**ChromeDriver Version Mismatch**
- Solution: Download ChromeDriver matching your Chrome version from [ChromeDriver Downloads](https://chromedriver.chromium.org/)

**No Data Extracted**
- Check internet connection
- Verify target websites are accessible
- Review console output for specific error messages

**Popup Blocking Extraction**
- Earth911 scrapper includes multiple popup-closing strategies
- Check `popup_debug.png` screenshots for manual popup identification

**Page Navigation Failures**
- Verify website structure hasn't changed
- Check for anti-bot measures on target sites
- Review browser console for JavaScript errors

---

