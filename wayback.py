import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from waybackpy import WaybackMachineCDXServerAPI

# List of websites to scrape
websites = [
    "https://carta.com/",
    "https://ledgy.com/"
]

# Store results in a list
data = []

for site in websites:
    print(f"\nFetching the most recent snapshot for: {site}")

    try:
        # Initialize the Wayback Machine API
        cdx_api = WaybackMachineCDXServerAPI(site)

        # Get the most recent snapshot
        snapshot = cdx_api.newest().archive_url

        print(f"Found snapshot: {snapshot}")

        # Scrape the archived page
        print(f"\nScraping: {snapshot}")
        response = requests.get(snapshot, timeout=10)
        response.raise_for_status()  # Raise an error for failed requests

        # Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract Title
        title = soup.title.text.strip() if soup.title else "No Title"

        # Extract H1
        h1 = soup.find("h1")
        h1_text = h1.text.strip() if h1 else "No H1 Found"

        # Extract first <p> after H1
        first_p = h1.find_next("p").text.strip() if h1 and h1.find_next("p") else "No Paragraph Found"

        # Extract all H2s (joined as a string for table readability)
        h2_tags = [h2.text.strip() for h2 in soup.find_all("h2")]
        h2_text = ", ".join(h2_tags) if h2_tags else "No H2s Found"

        # Append data to list
        data.append([site, snapshot, title, h1_text, first_p, h2_text])

        # Delay to avoid rate limiting
        time.sleep(2)

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {snapshot}: {e}")
    except Exception as e:
        print(f"An error occurred while processing {site}: {e}")

# Create the 'wayback_results' directory if it doesn't exist
os.makedirs("wayback_results", exist_ok=True)

# Create a DataFrame
df = pd.DataFrame(data, columns=["Website", "Snapshot URL", "Title", "H1", "First Paragraph", "H2s"])

# Generate a timestamp for unique filenames
timestamp = time.strftime("%Y-%m-%d")

# Save to CSV with timestamp in filename
csv_path = os.path.join("wayback_results", f"wayback_scraped_data_{timestamp}.csv")
df.to_csv(csv_path, index=False)
print(f"\nData saved to '{csv_path}'")
