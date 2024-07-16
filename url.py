import requests
import datetime

def validate_url(url):
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            print(f"URL {url} is valid at {datetime.datetime.now()}")
        else:
            print(f"URL {url} returned status code {response.status_code} at {datetime.datetime.now()}")
    except requests.RequestException as e:
        print(f"URL {url} is invalid or unreachable: {str(e)} at {datetime.datetime.now()}")

# List of URLs to validate
urls_to_validate = ["https://shop.wegmans.com/api/v2/store_products?fulfillment_type=instore&ads_enabled=true&ads_pagination_improvements=true&limit=60&offset=0&page=1&prophetScorer=frecency&sort=rank&allow_autocorrect=true&search_is_autocomplete=false&search_provider=ic&search_term=apple&secondary_results=true&unified_search_shadow_test_enabled=false"

]

# Function to run URL validation
def run_url_validation():
    for url in urls_to_validate:
        validate_url(url)

# Run URL validation
run_url_validation()
