class AmadeusService {
    constructor(apiKey, apiSecret) {
      this.apiKey = apiKey;
      this.apiSecret = apiSecret;
      this.token = null;
      this.tokenExpiry = null;
      this.baseUrl = 'https://api.amadeus.com/v2'; // Use 'https://api.amadeus.com/v2' for production
    }
  
    // Get or refresh the access token
    async getAccessToken() {
      // Check if token exists and is still valid
      if (this.token && this.tokenExpiry > Date.now()) {
        return this.token;
      }
  
      // Get new token if none exists or current one is expired
      try {
        const response = await fetch('https://test.api.amadeus.com/v1/security/oauth2/token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: `grant_type=client_credentials&client_id=${this.apiKey}&client_secret=${this.apiSecret}`
        });
  
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(`Authentication failed: ${errorData.error_description || 'Unknown error'}`);
        }
  
        const data = await response.json();
        this.token = data.access_token;
        // Set expiry time (convert seconds to milliseconds)
        this.tokenExpiry = Date.now() + (data.expires_in * 1000);
        
        return this.token;
      } catch (error) {
        console.error('Error getting access token:', error);
        throw error;
      }
    }
  
    // Search for hotels by city code
    async searchHotelsByCity(cityCode, checkInDate, checkOutDate, adults = 1) {
      try {
        const token = await this.getAccessToken();
        
        const url = new URL(`${this.baseUrl}/shopping/hotel-offers`);
        url.searchParams.append('cityCode', cityCode);
        url.searchParams.append('checkInDate', checkInDate);
        url.searchParams.append('checkOutDate', checkOutDate);
        url.searchParams.append('adults', adults);
        url.searchParams.append('includeClosed', 'false');
        url.searchParams.append('bestRateOnly', 'true');
        
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
  
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(`Hotel search failed: ${errorData.errors?.[0]?.detail || 'Unknown error'}`);
        }
  
        return await response.json();
      } catch (error) {
        console.error('Error searching hotels:', error);
        throw error;
      }
    }
    
    // Get detailed information for a specific hotel
    async getHotelOffers(hotelId, checkInDate, checkOutDate, adults = 1) {
      try {
        const token = await this.getAccessToken();
        
        const url = new URL(`${this.baseUrl}/shopping/hotel-offers/by-hotel`);
        url.searchParams.append('hotelId', hotelId);
        url.searchParams.append('checkInDate', checkInDate);
        url.searchParams.append('checkOutDate', checkOutDate);
        url.searchParams.append('adults', adults);
        
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
  
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(`Getting hotel details failed: ${errorData.errors?.[0]?.detail || 'Unknown error'}`);
        }
  
        return await response.json();
      } catch (error) {
        console.error('Error getting hotel details:', error);
        throw error;
      }
    }
  }