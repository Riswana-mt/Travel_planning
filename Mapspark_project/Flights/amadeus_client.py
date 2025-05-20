from amadeus import Client, ResponseError

# Initialize Amadeus API
amadeus = Client(
    client_id="udG2uhKycii1ZQdjNGzKE5bRf03PXxTo",      # Replace with your API Key
    client_secret="diSwctJGVsReexqL"  # Replace with your Secret Key
)

def search_flights(origin, destination, date):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=date,
            adults=1
        )
        return response.data  # Returns JSON response
    except ResponseError as error:
        return {"error": str(error)}
