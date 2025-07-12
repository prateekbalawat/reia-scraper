from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from location_slugs import slug_map
from selenium import webdriver
import sys
import json
import time
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def scrape_price(location):
    slug = slug_map.get(location)
    if not slug:
        return {"error": f"Unsupported location: {location}"}

    city = location.split()[-1].lower()
    url = f"https://housing.com/in/buy/{city}/{slug}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_binary = os.getenv("CHROME_BINARY", "/usr/bin/chromium")
    chrome_options.binary_location = chrome_binary

    # ✅ Use system-installed chromedriver path
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        logging.info(f"Navigating to {url}")
        try:
            driver.get(url)
        except Exception as e:
            driver.quit()
            return {"error": f"Failed to load page: {str(e)}"}

        WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'T_cardV1Style')]"))
        )

        nearby_properties = []
        property_type = None
        cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'T_cardV1Style')]")

        for card in cards[:5]:
            try:
                try:
                    name_elem = card.find_element(By.XPATH, ".//div[contains(@class, 'title-style')]")
                    name = name_elem.text.strip()
                except:
                    name = "Unnamed Property"

                if not property_type:
                    try:
                        type_line = card.find_element(By.XPATH, ".//h2[contains(@class, 'subtitle-style')]").text.strip()
                        if 'Flat' in type_line or 'apartment' in type_line:
                            property_type = "Apartment"
                        elif 'villa' in type_line:
                            property_type = "Villa"
                        elif 'plot' in type_line:
                            property_type = "Plot"
                        else:
                            property_type = "Other"
                    except:
                        property_type = "Unknown"

                price_elem = None
                price_text = ""

                try:
                    price_elem = card.find_element(By.XPATH, ".//div[contains(text(), 'Avg. Price')]")
                except:
                    pass

                if not price_elem:
                    try:
                        price_elem = card.find_element(By.XPATH, ".//div[contains(text(), 'Price')]")
                    except:
                        pass

                if not price_elem:
                    try:
                        for elem in card.find_elements(By.XPATH, ".//div"):
                            if "₹" in elem.text and "sq.ft" in elem.text:
                                price_elem = elem
                                break
                    except:
                        pass

                if price_elem:
                    price_text = price_elem.text.strip().lower()
                else:
                    continue

                if "₹" in price_text and "k/sq.ft" in price_text:
                    price_val = price_text.split("₹")[-1].split("k")[0].strip()
                    price_per_sqft = float(price_val) * 1000

                    if 1000 <= price_per_sqft <= 50000:
                        nearby_properties.append({
                            "name": name,
                            "price_per_sqft": int(price_per_sqft)
                        })
            except Exception as e:
                logging.warning(f"Skipping card due to unexpected error: {e}")
                continue

        if not nearby_properties:
            return {
                "location": location,
                "current_price_per_sqft": 8500,
                "property_type": property_type or "Unknown",
                "nearby_properties": [],
                "rental_yield_percent": 3.0,
                "note": "Used fallback due to scraping issue"
            }

        avg_price = sum(p["price_per_sqft"] for p in nearby_properties) // len(nearby_properties)

        return {
            "location": location,
            "current_price_per_sqft": avg_price,
            "property_type": property_type or "Unknown",
            "nearby_properties": nearby_properties,
            "rental_yield_percent": 3.0
        }

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No location provided"}))
        sys.exit(1)

    location = sys.argv[1]
    result = scrape_price(location)
    print(json.dumps(result, indent=2))