from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import json
import re
import csv

def extract_recycling_data(driver):
    """Extract recycling facility data from the search results page"""
    extracted_data = []
    
    try:
        # Wait for results to be present
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.result-item")))
        
        # Find all result items
        result_items = driver.find_elements(By.CSS_SELECTOR, "li.result-item")
        print(f"Found {len(result_items)} result items on this page")
        
        for i, item in enumerate(result_items, 1):
            try:
                # Extract business name
                title_element = item.find_element(By.CSS_SELECTOR, "h2.title a")
                business_name = title_element.text.strip()
                
                # Extract street address
                street_address = ""
                try:
                    address1_element = item.find_element(By.CSS_SELECTOR, "p.address1")
                    address3_element = item.find_element(By.CSS_SELECTOR, "p.address3")
                    
                    address1 = address1_element.text.strip()
                    address3 = address3_element.text.strip()
                    
                    if address1:
                        street_address = f"{address1}, {address3}"
                    else:
                        street_address = address3
                except:
                    street_address = "Address not available"
                
                # Extract materials accepted
                materials_accepted = []
                try:
                    material_elements = item.find_elements(By.CSS_SELECTOR, "span.material")
                    for material_element in material_elements:
                        material_text = material_element.text.strip()
                        # Skip empty, "Materials accepted:", "+X more" entries
                        if (material_text and 
                            not material_text.startswith('+') and 
                            "more" not in material_text and
                            "Materials accepted" not in material_text):
                            materials_accepted.append(material_text)
                    
                    if not materials_accepted:
                        materials_accepted = ["Materials not specified"]
                except:
                    materials_accepted = ["Materials not specified"]
                
                # last_update_date is not available in the HTML, set to today's date
                last_update_date = "26-07-2025"
                
                # Create data entry
                data_entry = {
                    "business_name": business_name,
                    "last_update_date": last_update_date,
                    "street_address": street_address,
                    "materials_accepted": materials_accepted
                }
                
                extracted_data.append(data_entry)
                print(f"  {i}. Extracted: {business_name}")
                
            except Exception as e:
                print(f"  {i}. Error extracting data from item: {e}")
                continue
                
    except Exception as e:
        print(f"Error finding result items: {e}")
    
    return extracted_data

def save_data_to_csv(data):
    """Save extracted data to data.csv file"""
    filename = "data.csv"
    
    # Define CSV headers
    headers = [
        "business_name",
        "last_update_date", 
        "street_address",
        "materials_accepted"
    ]
    
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        # Write headers
        writer.writeheader()
        
        # Write data rows
        for item in data:
            # Convert materials_accepted list to a semicolon-separated string
            csv_item = item.copy()
            csv_item["materials_accepted"] = "; ".join(item["materials_accepted"])
            writer.writerow(csv_item)
    
    # Also create a metadata file
    metadata = {
        "source": "earth911.com search results",
        "extraction_date": "2025-07-26",
        "total_programs_extracted": len(data),
        "data_structure_version": "2.0",
        "search_parameters": {
            "what": "Electronics",
            "where": "10001",
            "max_distance": 100,
            "pages_extracted": "Multiple pages (up to 5)"
        },
        "fields_extracted": headers,
        "notes": {
            "materials_accepted": "Multiple materials separated by semicolons (;)",
            "csv_filename": filename
        }
    }
    
    with open("extraction_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

# Get the path to chromedriver in the root directory
chrome_driver_path = os.path.join(os.getcwd(), "chromedriver.exe")

# Create a Service object
service = Service(chrome_driver_path)

# Create Chrome driver instance
driver = webdriver.Chrome(service=service)

try:
    # Visit the website
    driver.get("https://search.earth911.com/")
    
    # Wait for the page to load and find the form elements
    wait = WebDriverWait(driver, 20)
    
    # Find and fill the "what" field with "Electronics"
    what_field = wait.until(EC.presence_of_element_located((By.ID, "what")))
    what_field.clear()
    what_field.send_keys("Electronics")
    
    # Find and fill the "where" field with "10001"
    where_field = wait.until(EC.presence_of_element_located((By.ID, "where")))
    where_field.clear()
    where_field.send_keys("10001")
    
    # Find and click the search button
    search_button = wait.until(EC.element_to_be_clickable((By.ID, "submit-location-search")))
    search_button.click()
    
    # Wait 10 seconds for the results to load
    time.sleep(10)
    
    # Find the distance dropdown and select 100 miles
    distance_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select[onchange*='max_distance']")))
    
    # Create a Select object to interact with the dropdown
    select = Select(distance_dropdown)
    select.select_by_value("100")
    
    # Wait 15 seconds for popup to appear, then close it
    print("Waiting for popup to appear...")
    time.sleep(15)
    
    # Wait 15 seconds for popup to appear, then close it
    print("Waiting for popup to appear...")
    time.sleep(15)
    
    # Wait 15 seconds for popup to appear, then close it
    print("Waiting for popup to appear...")
    time.sleep(15)
    
    try:
        # Look for the popup close button - try multiple selectors
        close_button = None
        close_selectors = [
            "i._close-icon",
            "._close-icon", 
            ".close-icon",
            "[class*='close-icon']",
            "[class*='close']",
            "button[aria-label*='close']",
            ".modal-close",
            ".popup-close"
        ]
        
        print("Looking for popup close button...")
        for i, selector in enumerate(close_selectors, 1):
            try:
                print(f"Trying selector {i}: {selector}")
                close_button = driver.find_element(By.CSS_SELECTOR, selector)
                if close_button.is_displayed() and close_button.is_enabled():
                    close_button.click()
                    print(f"Popup closed successfully using selector: {selector}")
                    time.sleep(2)  # Wait a bit after closing popup
                    break
            except:
                continue
        
        if not close_button or not close_button.is_displayed():
            print("Could not find or click popup close button")
            # Take a screenshot for debugging
            try:
                driver.save_screenshot("popup_debug.png")
                print("Screenshot saved as 'popup_debug.png' for debugging")
            except:
                pass
            
    except Exception as e:
        print(f"Error handling popup: {e}")
        print("Continuing with extraction...")
    
    # Wait for the page to reload with new results
    time.sleep(5)
    
    # Extract data from multiple pages (5 pages total)
    all_extracted_data = []
    max_pages = 5
    
    for page_num in range(1, max_pages + 1):
        print(f"Extracting data from page {page_num}...")
        
        # Extract data from current page
        page_data = extract_recycling_data(driver)
        all_extracted_data.extend(page_data)
        print(f"Extracted {len(page_data)} items from page {page_num}")
        
        # If this is not the last page, click Next button
        if page_num < max_pages:
            try:
                # Scroll to the bottom of the page first
                print("Scrolling to bottom of page to find Next button...")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Wait for scroll to complete
                
                # Alternative scroll method if the first doesn't work
                try:
                    # Try to find pagination area and scroll to it
                    pagination_area = driver.find_element(By.CSS_SELECTOR, ".pagination, .pager, .page-navigation")
                    driver.execute_script("arguments[0].scrollIntoView(true);", pagination_area)
                    time.sleep(1)
                except:
                    # If no pagination area found, try scrolling to footer
                    try:
                        footer = driver.find_element(By.CSS_SELECTOR, "footer, .footer")
                        driver.execute_script("arguments[0].scrollIntoView(true);", footer)
                        time.sleep(1)
                    except:
                        pass
                
                # Wait a bit before looking for Next button
                time.sleep(3)
                
                # Check if Next button exists and is clickable
                next_buttons = driver.find_elements(By.CSS_SELECTOR, "a.next")
                if not next_buttons:
                    print("No Next button found - reached end of results")
                    # Take a screenshot to see what's on the page
                    try:
                        driver.save_screenshot(f"page_{page_num}_no_next_button.png")
                        print(f"Screenshot saved: page_{page_num}_no_next_button.png")
                    except:
                        pass
                    break
                
                next_button = next_buttons[0]
                print(f"Found Next button: {next_button.get_attribute('href')}")
                
                # Check if the Next button is actually clickable (not disabled)
                if next_button.get_attribute("href"):
                    # Scroll to the Next button to ensure it's visible
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    time.sleep(1)
                    
                    # Click the Next button
                    next_button.click()
                    print(f"Clicked Next button to go to page {page_num + 1}")
                    
                    # Wait for the next page to load and verify we moved to a new page
                    time.sleep(5)
                    
                    # Verify we successfully moved to the next page
                    current_url = driver.current_url
                    if f"page={page_num + 1}" in current_url:
                        print(f"Successfully navigated to page {page_num + 1}")
                    else:
                        print(f"Page navigation may have failed - URL: {current_url}")
                else:
                    print("Next button is disabled - reached end of results")
                    break
                    
            except Exception as e:
                print(f"Could not navigate to page {page_num + 1}: {e}")
                print("Stopping pagination - might have reached the last page or encountered an error")
                break
    
    # Save all collected data to CSV file
    save_data_to_csv(all_extracted_data)
    print(f"Total extracted {len(all_extracted_data)} items from {page_num} pages and saved to data.csv")
    
    # Keep the browser open (remove this line if you want it to close automatically)
    input("Press Enter to close the browser...")
    
finally:
    # Close the browser
    driver.quit()
