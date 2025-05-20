document.addEventListener('DOMContentLoaded', function() {
    // Toggle packing item status
    document.querySelectorAll('.packing-item-toggle').forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            fetch(`/toggle-packed/${itemId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    }
                });
        });
    });
    
    // Budget chart (if you want to add charts)
    const budgetCtx = document.getElementById('budgetChart');
    if (budgetCtx) {
        new Chart(budgetCtx, {
            type: 'doughnut',
            data: {
                labels: ['Accommodation', 'Transportation', 'Food', 'Activities'],
                datasets: [{
                    data: [
                        budgetCtx.dataset.accommodation,
                        budgetCtx.dataset.transportation,
                        budgetCtx.dataset.food,
                        budgetCtx.dataset.activities
                    ],
                    backgroundColor: [
                        '#4e73df',
                        '#1cc88a',
                        '#36b9cc',
                        '#f6c23e'
                    ],
                    hoverBackgroundColor: [
                        '#2e59d9',
                        '#17a673',
                        '#2c9faf',
                        '#dda20a'
                    ],
                    hoverBorderColor: "rgba(234, 236, 244, 1)",
                }],
            },
            options: {
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                },
                cutout: '70%',
            },
        });
    }
});



//for hotel adding 


// Initialize tooltips
$(function () {
    $('[data-bs-toggle="tooltip"]').tooltip();
});

// Add animation to price change
function animatePriceChange() {
    const totalPrice = $('#totalPrice');
    totalPrice.addClass('changed');
    setTimeout(() => {
        totalPrice.removeClass('changed');
    }, 1000);
}

// Handle date picker interactions
$(document).ready(function() {
    // Set minimum check-out date based on check-in date
    $('#id_check_in').change(function() {
        const checkInDate = $(this).val();
        $('#id_check_out').attr('min', checkInDate);
        
        // If current check-out is before new check-in, reset it
        if ($('#id_check_out').val() && $('#id_check_out').val() < checkInDate) {
            $('#id_check_out').val('');
        }
        
        animatePriceChange();
    });
    
    // Add smooth scrolling to all links
    $("a").on('click', function(event) {
        if (this.hash !== "") {
            event.preventDefault();
            const hash = this.hash;
            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 800, function(){
                window.location.hash = hash;
            });
        }
    });
    
    // Add loading spinner to form submissions
    $('form').submit(function() {
        const submitBtn = $(this).find('button[type="submit"]');
        submitBtn.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...');
        submitBtn.prop('disabled', true);
    });
    
    // Initialize image hover effect
    $('.hotel-img').hover(
        function() {
            $(this).css('transform', 'scale(1.03)');
        },
        function() {
            $(this).css('transform', 'scale(1)');
        }
    );
});

// Handle booking form validation
function validateBookingForm() {
    const checkIn = $('#id_check_in').val();
    const checkOut = $('#id_check_out').val();
    const guests = $('#id_guests').val();
    
    if (!checkIn || !checkOut) {
        alert('Please select both check-in and check-out dates.');
        return false;
    }
    
    if (new Date(checkOut) <= new Date(checkIn)) {
        alert('Check-out date must be after check-in date.');
        return false;
    }
    
    if (!guests || guests < 1) {
        alert('Please enter a valid number of guests.');
        return false;
    }
    
    return true;
}






// hoteel data //



