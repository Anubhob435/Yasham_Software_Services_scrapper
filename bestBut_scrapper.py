from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import csv

def extract_store_data(driver, wait):
    """Extract Best Buy store data from the search results"""
    extracted_stores = []
    
    try:
        # Find all store list items
        store_items = driver.find_elements(By.CSS_SELECTOR, "li.store")
        print(f"Found {len(store_items)} store(s)")
        
        for i, store_item in enumerate(store_items, 1):
            try:
                store_data = {}
                
                # Extract store ID
                store_id = store_item.get_attribute("data-store-id")
                store_data["store_id"] = store_id
                
                # Extract store name
                try:
                    store_name_element = store_item.find_element(By.CSS_SELECTOR, "button[data-cy='store-heading']")
                    store_data["store_name"] = store_name_element.text.strip()
                except:
                    store_data["store_name"] = "Store name not found"
                
                # Extract distance
                try:
                    distance_element = store_item.find_element(By.CSS_SELECTOR, "[data-cy='LocationDistance']")
                    store_data["distance"] = distance_element.text.strip()
                except:
                    store_data["distance"] = "Distance not found"
                
                # Extract address
                try:
                    address_element = store_item.find_element(By.CSS_SELECTOR, "[data-cy='AddressComponent']")
                    address_spans = address_element.find_elements(By.TAG_NAME, "span")
                    
                    street_address = address_spans[0].text.strip() if len(address_spans) > 0 else ""
                    city_state_zip = address_spans[1].text.strip() if len(address_spans) > 1 else ""
                    
                    store_data["street_address"] = street_address
                    store_data["city_state_zip"] = city_state_zip
                    store_data["full_address"] = f"{street_address}, {city_state_zip}" if street_address else city_state_zip
                except:
                    store_data["street_address"] = "Address not found"
                    store_data["city_state_zip"] = "City/State/ZIP not found"
                    store_data["full_address"] = "Full address not found"
                
                # Extract hours
                try:
                    hours_element = store_item.find_element(By.CSS_SELECTOR, "[data-cy='BusinessHoursComponent']")
                    store_data["hours"] = hours_element.text.strip()
                except:
                    store_data["hours"] = "Hours not found"
                
                # Extract store details link
                try:
                    details_link = store_item.find_element(By.CSS_SELECTOR, "[data-cy='DetailsComponent']")
                    store_data["details_url"] = details_link.get_attribute("href")
                except:
                    store_data["details_url"] = "Details URL not found"
                
                # Extract phone number from script data if available
                try:
                    script_elements = store_item.find_elements(By.TAG_NAME, "script")
                    for script in script_elements:
                        script_content = script.get_attribute("innerHTML")
                        if "phone" in script_content:
                            # Try to extract phone number from script
                            import re
                            phone_match = re.search(r'"phone":"([^"]+)"', script_content)
                            if phone_match:
                                store_data["phone"] = phone_match.group(1)
                                break
                    
                    if "phone" not in store_data:
                        store_data["phone"] = "Phone not found"
                except:
                    store_data["phone"] = "Phone not found"
                
                extracted_stores.append(store_data)
                print(f"  {i}. Extracted: {store_data.get('store_name', 'Unknown')} - {store_data.get('distance', 'Unknown distance')}")
                
            except Exception as e:
                print(f"  {i}. Error extracting store data: {e}")
                continue
                
    except Exception as e:
        print(f"Error finding store items: {e}")
    
    return extracted_stores

def save_store_data_to_csv(stores):
    """Save extracted store data to CSV file"""
    if not stores:
        print("No store data to save")
        return
    
    # Define CSV headers
    headers = [
        "store_id",
        "store_name", 
        "distance",
        "street_address",
        "city_state_zip",
        "full_address",
        "hours",
        "details_url",
        "phone"
    ]
    
    # Save to CSV file
    with open("bestbuy_stores.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        # Write header row
        writer.writeheader()
        
        # Write store data rows
        for store in stores:
            writer.writerow(store)
    
    print(f"Store data saved to bestbuy_stores.csv with {len(stores)} records")

link = "https://www.bestbuy.com/site/store-locator"

# Get the path to chromedriver in the root directory
chrome_driver_path = os.path.join(os.getcwd(), "chromedriver.exe")

# Create a Service object
service = Service(chrome_driver_path)

# Create Chrome driver instance
driver = webdriver.Chrome(service=service)

try:
    # Visit the Best Buy store locator
    print(f"Opening Best Buy store locator: {link}")
    driver.get(link)
    
    # Wait for the page to load
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    print("Page loaded successfully!")
    
    # Wait 10 seconds
    print("Waiting 10 seconds...")
    time.sleep(10)
    
    # Refresh the page
    print("Refreshing the page...")
    driver.refresh()
    
    # Wait for the page to load after refresh
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("Page refreshed successfully!")
    
    # Wait a bit for any dynamic content to load
    time.sleep(3)
    
    # Find and fill the zip code input field
    try:
        print("Looking for zip code input field...")
        
        # Try multiple selectors to find the zip code input
        zip_input_selectors = [
            "input.zip-code-input",
            "input[data-cy='ZipCodeInputComponent']",
            "input[placeholder*='ZIP']",
            "input[aria-label*='zip code']",
            "input[title*='ZIP']"
        ]
        
        zip_input = None
        for selector in zip_input_selectors:
            try:
                zip_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                print(f"Found zip code input using selector: {selector}")
                break
            except:
                continue
        
        if zip_input:
            # Clear any existing text and enter 10001
            zip_input.clear()
            zip_input.send_keys("10001")
            print("Entered '10001' in the zip code field")
            
            # Find and click the Update button
            try:
                print("Looking for Update button...")
                
                # Try multiple selectors to find the Update button
                update_button_selectors = [
                    "button.location-zip-code-form-update-btn",
                    "button[data-cy='SubmitButton']",
                    "button[type='submit']",
                    "button:contains('Update')",
                    ".location-zip-code-form-update-btn"
                ]
                
                update_button = None
                for selector in update_button_selectors:
                    try:
                        update_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                        print(f"Found Update button using selector: {selector}")
                        break
                    except:
                        continue
                
                if update_button:
                    # Click the Update button
                    update_button.click()
                    print("Clicked the 'Update' button")
                    
                    # Wait 7 seconds for the results to load
                    print("Waiting 7 seconds for store results to load...")
                    time.sleep(7)
                    
                    # Extract store data
                    print("Extracting store data...")
                    store_data = extract_store_data(driver, wait)
                    
                    # Save data to CSV file
                    save_store_data_to_csv(store_data)
                    print(f"Extracted {len(store_data)} stores and saved to bestbuy_stores.csv")
                    
                else:
                    print("Could not find Update button")
                    
            except Exception as e:
                print(f"Error finding or clicking Update button: {e}")
                
        else:
            print("Could not find zip code input field")
            
    except Exception as e:
        print(f"Error finding or filling zip code input: {e}")
    
    # Keep the browser open (remove this line if you want it to close automatically)
    input("Press Enter to close the browser...")
    
finally:
    # Close the browser
    driver.quit()