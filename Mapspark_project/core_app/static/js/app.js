document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const searchButton = document.getElementById('search-button');
    const backButton = document.getElementById('back-button');
    const hotelResults = document.getElementById('hotel-results');
    const hotelDetails = document.getElementById('hotel-details');
    const hotelInfo = document.getElementById('hotel-info');
    const loadingIndicator = document.getElementById('loading');
    const errorMessage = document.getElementById('error-message');
    
    // Initialize date inputs with default values
    const checkInInput = document.getElementById('check-in');
    const checkOutInput = document.getElementById('check-out');
    
    // Set default dates (today and tomorrow)
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    // Format dates as YYYY-MM-DD
    checkInInput.value = formatDate(today);
    checkOutInput.value = formatDate(tomorrow);
    
    // Initialize Amadeus service
    const amadeusService = new AmadeusService(config.AMADEUS_API_KEY, config.AMADEUS_API_SECRET);
    
    // Event listeners
    searchButton.addEventListener('click', searchHotels);
    backButton.addEventListener('click', showResults);
    
    // Search for hotels
    async function searchHotels() {
      const cityCode = document.getElementById('city-code').value.trim().toUpperCase();
      const checkInDate = checkInInput.value;
      const checkOutDate = checkOutInput.value;
      const adults = document.getElementById('adults').value;
      
      // Validate inputs
      if (!cityCode || !checkInDate || !checkOutDate) {
        showError('Please fill in all required fields');
        return;
      }
      
      // Check if check-out date is after check-in date
      if (new Date(checkOutDate) <= new Date(checkInDate)) {
        showError('Check-out date must be after check-in date');
        return;
      }
      
      try {
        // Show loading indicator
        showLoading();
        
        // Fetch hotels
        const result = await amadeusService.searchHotelsByCity(cityCode, checkInDate, checkOutDate, adults);
        
        // Hide loading indicator
        hideLoading();
        
        // Display results
        displayHotels(result.data);
        showResults();
      } catch (error) {
        hideLoading();
        showError(error.message);
      }
    }
    
    // Display hotels in the result list
    function displayHotels(hotels) {
      if (!hotels || hotels.length === 0) {
        hotelResults.innerHTML = '<div class="no-results">No hotels found for this location and dates.</div>';
        return;
      }
      
      const hotelList = hotels.map(hotel => {
        const hotelData = hotel.hotel;
        const offer = hotel.offers?.[0];
        
        return `
          <div class="hotel-card">
            <h3>${hotelData.name}</h3>
            <p class="hotel-rating">${getStarRating(hotelData.rating)}</p>
            <p class="hotel-address">${hotelData.address?.lines?.join(', ')}, ${hotelData.address?.cityName}</p>
            
            <div class="hotel-price">
              ${offer ? `<strong>${offer.price.currency} ${offer.price.total}</strong> for ${getDurationDays(offer.checkInDate, offer.checkOutDate)} nights` : 'Price not available'}
            </div>
            
            <button class="view-button" data-hotel-id="${hotelData.hotelId}">View Details</button>
          </div>
        `;
      }).join('');
      
      hotelResults.innerHTML = hotelList;
      
      // Add event listeners to view buttons
      document.querySelectorAll('.view-button').forEach(button => {
        button.addEventListener('click', () => {
          const hotelId = button.getAttribute('data-hotel-id');
          getHotelDetails(hotelId);
        });
      });
    }
    
    // Get detailed information for a specific hotel
    async function getHotelDetails(hotelId) {
      try {
        showLoading();
        
        const checkInDate = checkInInput.value;
        const checkOutDate = checkOutInput.value;
        const adults = document.getElementById('adults').value;
        
        const result = await amadeusService.getHotelOffers(hotelId, checkInDate, checkOutDate, adults);
        
        hideLoading();
        displayHotelDetails(result.data);
        showDetails();
      } catch (error) {
        hideLoading();
        showError(error.message);
      }
    }
    
    // Display detailed information for a specific hotel
    function displayHotelDetails(hotelData) {
      const hotel = hotelData.hotel;
      const offers = hotelData.offers || [];
      
      let offersList = '';
      
      if (offers.length > 0) {
        offersList = `
          <h3>Available Rooms</h3>
          <ul class="offers-list">
            ${offers.map(offer => `
              <li class="offer-item">
                <div class="offer-header">
                  <span class="room-type">${offer.room?.typeEstimated?.category || 'Standard Room'}</span>
                  <span class="price">${offer.price.currency} ${offer.price.total}</span>
                </div>
                <div class="offer-details">
                  <p>${offer.room?.description?.text || 'Room description not available'}</p>
                  <p><strong>Board:</strong> ${offer.boardType || 'Not included'}</p>
                  <p><strong>Cancellation:</strong> ${offer.policies?.cancellations?.[0]?.deadline ? 'Free cancellation until ' + formatDateDisplay(offer.policies.cancellations[0].deadline) : 'No free cancellation'}</p>
                </div>
                <button class="book-button" data-offer-id="${offer.id}">Book Now</button>
              </li>
            `).join('')}
          </ul>
        `;
      } else {
        offersList = '<p class="no-offers">No room offers available for the selected dates</p>';
      }
      
      const amenities = hotel.amenities?.map(amenity => `<li>${formatAmenity(amenity)}</li>`).join('') || '';
      
      hotelInfo.innerHTML = `
        <div class="hotel-detail-header">
          <h2>${hotel.name}</h2>
          <p class="hotel-rating">${getStarRating(hotel.rating)}</p>
        </div>
        
        <div class="hotel-location">
          <h3>Location</h3>
          <p>${hotel.address?.lines?.join(', ')}</p>
          <p>${hotel.address?.cityName}, ${hotel.address?.countryCode}</p>
        </div>
        
        ${amenities ? `
          <div class="hotel-amenities">
            <h3>Amenities</h3>
            <ul class="amenities-list">
              ${amenities}
            </ul>
          </div>
        ` : ''}
        
        <div class="hotel-offers">
          ${offersList}
        </div>
      `;
      
      // Add event listeners to book buttons
      document.querySelectorAll('.book-button').forEach(button => {
        button.addEventListener('click', () => {
          const offerId = button.getAttribute('data-offer-id');
          alert(`Booking functionality would go here for offer ID: ${offerId}`);
          // Implement booking functionality here
        });
      });
    }
    
    // Helper functions
    function showLoading() {
      loadingIndicator.classList.remove('hidden');
      errorMessage.classList.add('hidden');
    }
    
    function hideLoading() {
      loadingIndicator.classList.add('hidden');
    }
    
    function showError(message) {
      errorMessage.textContent = message;
      errorMessage.classList.remove('hidden');
    }
    
    function showResults() {
      hotelResults.parentElement.classList.remove('hidden');
      hotelDetails.classList.add('hidden');
    }
    
    function showDetails() {
      hotelResults.parentElement.classList.add('hidden');
      hotelDetails.classList.remove('hidden');
    }
    
    function formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    }
    
    function formatDateDisplay(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    }
    
    function getDurationDays(checkIn, checkOut) {
      const start = new Date(checkIn);
      const end = new Date(checkOut);
      const diffTime = Math.abs(end - start);
      return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    }
    
    function getStarRating(rating) {
      if (!rating) return '';
      const stars = parseInt(rating);
      return '★'.repeat(stars) + '☆'.repeat(5 - stars);
    }
    
    function formatAmenity(amenity) {
      return amenity
        .replace(/_/g, ' ')
        .replace(/\b\w/g, c => c.toUpperCase());
    }
  });