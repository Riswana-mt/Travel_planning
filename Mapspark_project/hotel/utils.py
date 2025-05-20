import requests
from django.conf import settings

def fetch_hotels(location="New York"):
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring = {"q": location, "locale": "en_US"}
    
    headers = {
        "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    return response.json() if response.status_code == 200 else None