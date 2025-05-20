from amadeus import Client

try:
    amadeus = Client(
        client_id="udG2uhKycii1ZQdjNGzKE5bRf03PXxTo",
        client_secret="diSwctJGVsReexqL"
    )
    print("Amadeus client initialized successfully!")
except ValueError as e:
    print(f"Error: {str(e)}")