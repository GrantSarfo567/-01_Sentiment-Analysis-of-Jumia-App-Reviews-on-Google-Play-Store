import serpapi
import os
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('SERPAPI_KEY')
client = serpapi.Client(api_key=api_key)

results = client.search(
    engine = "google_play_product",
    product_id = "com.jumia.android",
    store = "apps", 
    all_reviews = "true",
    num = 199
)

data = results['reviews']

print("Total reviews: ", len(results["reviews"]))

# Pagination Logic
while 'serpapi_pagination' in results and len(data) < 2000:
    results = client.search(
        engine = "google_play_product",
        product_id = "com.jumia.android",
        store = "apps", 
        all_reviews = "true",
        num = 199,
        next_page_token = results['serpapi_pagination']['next_page_token']
    )
    data.extend(results['reviews'])
    print("Total reviews: ", len(data))
    if len(data) >= 2000:
        print("Reached 2000 reviews limit. Stopping extraction...")
        break

print("All done...")
df = pd.DataFrame(data)
df.to_csv('jumia_reviews.csv', index=False)
