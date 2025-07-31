# 🏠 Real Estate Price Scraper (Python + Selenium)

- This project scrapes **property price per square foot** data from [Housing.com](https://housing.com) for specified locations in Bangalore. It's built using **Python + Selenium** and can optionally be used with a Flask API.

## 📦 Features

- Scrapes top 5 property listings from Housing.com for a given location
- Extracts:
  - `current_price_per_sqft` (average of nearby listings)
  - `nearby_properties` (name + price per sq.ft)
  - `property_type` (Apartment / Villa / Plot / Other)
  - `rental_yield_percent` (fixed at 3%)
- Can run as a **standalone CLI** or be exposed via a **Flask API**

## ⚙️ Requirements

- Python 3.7+
- Google Chrome / Chromium installed
- Matching ChromeDriver (script uses `/usr/bin/chromedriver`)
- `pip` for installing dependencies

---

## 📥 Installation

```bash
# Clone this repo
git clone https://github.com/yourusername/reia-scraper.git
cd reia-scraper

# (Optional) Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt


---

🚀 Running the Scraper via CLI

python3 price_scraper.py "Whitefield Bangalore"

✅ Sample Output:

{
  "location": "Whitefield Bangalore",
  "current_price_per_sqft": 9514,
  "nearby_properties": [
    {
      "name": "Ishtika Anahata",
      "price_per_sqft": 7000
    },
    {
      "name": "Pavani Mirabilia",
      "price_per_sqft": 9500
    },
    {
      "name": "Sumadhura Capitol Residences",
      "price_per_sqft": 14500
    },
    {
      "name": "Sakthi Tranquilis Phase 2",
      "price_per_sqft": 7570
    },
    {
      "name": "DSR Elixir",
      "price_per_sqft": 9000
    }
  ],
  "property_type": "Apartment",
  "rental_yield_percent": 3.0
}


---

🌐 Running as an API (Optional)

1. Start the Flask server:

python3 scraper_api.py

2. Make a POST request to:

http://localhost:5000/scrape

With body:

{
  "location": "Whitefield Bangalore"
}

Example with curl:

curl -X POST http://localhost:5000/scrape \
  -H "Content-Type: application/json" \
  -d '{"location": "Whitefield Bangalore"}'


---

📍 Location Slugs

The file location_slugs.py contains a mapping of readable location names to Housing.com URL slugs. For example:

slug_map = {
  "Whitefield Bangalore": "whitefield-psouth-bangalore",
  "JP Nagar Bangalore": "jp-nagar-psouth-bangalore",
  ...
}

If a location is not in the map, the script returns an "Unsupported location" error.


---

```
