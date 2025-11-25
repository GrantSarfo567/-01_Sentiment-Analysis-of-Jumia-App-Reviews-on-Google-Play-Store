import serpapi
import os
import pandas as pd

# Load environment variables from .env file (where your API key is stored)
from dotenv import load_dotenv
load_dotenv()

# Get SerpAPI key from environment variables
api_key = os.getenv('SERPAPI_KEY')

# Create a SerpAPI client using your API key
client = serpapi.Client(api_key=api_key)

# ---------------------------------------------
# FIRST API CALL: Fetch initial batch of reviews
# ---------------------------------------------
results = client.search(
    engine="google_play_product",      # Use SerpAPI's Google Play scraper
    product_id="com.jumia.android",    # App ID of Jumia Ghana
    store="apps",
    all_reviews="true",                # Request reviews, not just metadata
    num=199                            # Max results per request (SerpAPI limit)
)

# Extract only the review objects from the response
data = results['reviews']

print("Total reviews fetched so far:", len(results["reviews"]))

# ---------------------------------------------------
# PAGINATION LOOP: Continue fetching additional pages
# ---------------------------------------------------
while 'serpapi_pagination' in results and len(data) < 2000:
    # Get the next page of results using SerpAPI's pagination token
    results = client.search(
        engine="google_play_product",
        product_id="com.jumia.android",
        store="apps",
        all_reviews="true",
        num=199,
        next_page_token=results['serpapi_pagination']['next_page_token']
    )

    # Add new reviews to the existing list
    data.extend(results['reviews'])

    print("Total reviews fetched so far:", len(data))

    # Stop when we hit your limit of 2000 reviews
    if len(data) >= 2000:
        print("Reached 2000 reviews limit. Stopping extraction...")
        break

print("Scraping complete.")

# ---------------------------------------------
# CONVERT TO DATAFRAME AND EXPORT AS CSV FILE
# ---------------------------------------------
df = pd.DataFrame(data)

# Save results to CSV (same folder as the script)
df.to_csv('jumia_reviews.csv', index=False)

print("CSV file saved as 'jumia_reviews.csv'")

