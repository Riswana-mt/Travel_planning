import requests
from django.conf import settings

def search_hotels(city_code, check_in, check_out, adults, rooms=1):
    """Connect to Amadeus/Expedia/Booking.com API"""
    try:
        # Example for Amadeus API
        url = "https://test.api.amadeus.com/v3/shopping/hotel-offers"
        
        params = {
            'cityCode': city_code,
            'checkInDate': check_in,
            'checkOutDate': check_out,
            'adults': adults,
            'roomQuantity': rooms,
            'bestRateOnly': 'true',
            'currency': 'USD'
        }
        
        headers = {
            'Authorization': f'Bearer {settings.API_KEYS["AMADEUS"]}',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        # Transform API response to your format
        hotels = []
        for offer in response.json().get('data', []):
            hotel = offer['hotel']
            price = offer['offers'][0]['price']['total']
            
            hotels.append({
                'id': hotel['hotelId'],
                'name': hotel['name'],
                'price': price,
                'rating': hotel.get('rating', 4),
                'address': hotel['address']['lines'][0],
                'photo': hotel.get('media', [{}])[0].get('uri', '')
            })
            
        return hotels
        
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None