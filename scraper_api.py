from flask import Flask, request, jsonify
from price_scraper import scrape_price

app = Flask(__name__)

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json()
    location = data.get("location")

    if not location:
        return jsonify({"error": "Location is required"}), 400

    result = scrape_price(location)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)