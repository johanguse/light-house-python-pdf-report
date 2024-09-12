import requests

API_URL = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'

def fetch_lighthouse_data(url, api_key, strategy='mobile'):
    params = {
        'url': url,
        'key': api_key,
        'strategy': strategy,
        'category': ['performance', 'accessibility', 'best-practices', 'seo']
    }
    
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}")