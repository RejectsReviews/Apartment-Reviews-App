// Modal functionality for delete confirmation
function openDeleteModal(reviewId) {
    const modal = document.getElementById('deleteModal');
    const deleteForm = document.getElementById('deleteForm');
    deleteForm.action = `/review/${reviewId}/delete`;
    modal.style.display = 'block';
}

function closeDeleteModal() {
    const modal = document.getElementById('deleteModal');
    modal.style.display = 'none';
}

// Filter reviews
function filterReviews() {
    const filterValue = document.getElementById('reviewFilter').value;
    const reviewCards = document.querySelectorAll('.review-card');
    
    reviewCards.forEach(card => {
        const rating = parseInt(card.getAttribute('data-rating'));
        
        if (filterValue === 'all' || 
            (filterValue === 'positive' && rating >= 4) || 
            (filterValue === 'neutral' && rating === 3) || 
            (filterValue === 'negative' && rating <= 2)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
    
    // Check if any reviews are visible after filtering
    const visibleReviews = Array.from(reviewCards).filter(card => 
        card.style.display !== 'none'
    );
    
    const noReviewsMessage = document.getElementById('noReviewsAfterFilter');
    if (visibleReviews.length === 0 && reviewCards.length > 0) {
        noReviewsMessage.style.display = 'block';
    } else {
        noReviewsMessage.style.display = 'none';
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Set up delete button click listeners
    const deleteButtons = document.querySelectorAll('[data-action="delete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const reviewId = this.getAttribute('data-review-id');
            openDeleteModal(reviewId);
        });
    });
    
    // Set up cancel button click listener
    const cancelButton = document.querySelector('.cancel-button[data-action="cancel"]');
    if (cancelButton) {
        cancelButton.addEventListener('click', closeDeleteModal);
    }
    
    // Set up click listeners for modal background
    window.addEventListener('click', function(event) {
        const modal = document.getElementById('deleteModal');
        if (event.target === modal) {
            closeDeleteModal();
        }
    });
    
    // Set up filter change listener
    const filterDropdown = document.getElementById('rating-filter');
    if (filterDropdown) {
        filterDropdown.addEventListener('change', function() {
            sortReviews(this.value);
        });
    }
    
    // Initialize amenities toggles
    const showMoreBtn = document.getElementById('show-more-amenities');
    const extraAmenities = document.getElementById('extra-amenities');
    
    if (showMoreBtn && extraAmenities) {
        showMoreBtn.addEventListener('click', function() {
            if (extraAmenities.style.display === 'none' || !extraAmenities.style.display) {
                extraAmenities.style.display = 'block';
                showMoreBtn.textContent = 'Show Less';
            } else {
                extraAmenities.style.display = 'none';
                showMoreBtn.textContent = 'Show More';
            }
        });
    }
    
    // Initialize reviews section
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function(e) {
            // Form validation would go here
        });
    }
    
    // Rating stars functionality
    const ratingInputs = document.querySelectorAll('.rating-input');
    const ratingLabels = document.querySelectorAll('.rating-label');
    
    if (ratingInputs.length && ratingLabels.length) {
        ratingLabels.forEach(label => {
            label.addEventListener('mouseover', function() {
                const ratingValue = parseInt(this.getAttribute('for').split('-')[1]);
                highlightStars(ratingValue);
            });
            
            label.addEventListener('mouseout', function() {
                resetStars();
                const selectedRating = getSelectedRating();
                if (selectedRating) {
                    highlightStars(selectedRating);
                }
            });
        });
    }
    
    function highlightStars(rating) {
        ratingLabels.forEach(label => {
            const labelRating = parseInt(label.getAttribute('for').split('-')[1]);
            if (labelRating <= rating) {
                label.classList.add('active');
            } else {
                label.classList.remove('active');
            }
        });
    }
    
    function resetStars() {
        ratingLabels.forEach(label => {
            label.classList.remove('active');
        });
    }
    
    function getSelectedRating() {
        for (let input of ratingInputs) {
            if (input.checked) {
                return parseInt(input.value);
            }
        }
        return null;
    }
});

// Reviews sorting functionality
document.addEventListener('DOMContentLoaded', function() {
  // Handle modal click outside
  window.onclick = function(event) {
    const modal = document.getElementById('deleteModal');
    if (event.target === modal) {
      closeDeleteModal();
    }
  };

  // Set up review filtering
  const filterDropdown = document.getElementById('rating-filter');
  
  if (filterDropdown) {
    console.log("Filter dropdown found, adding event listener");
    
    filterDropdown.addEventListener('change', function() {
      console.log("Filter changed to: " + this.value);
      sortReviews(this.value);
    });
    
    // Initial sort (optional)
    // sortReviews('default');
  } else {
    console.log("Filter dropdown not found");
  }
  
  function sortReviews(sortOption) {
    const reviewsContainer = document.querySelector('.reviews-container');
    if (!reviewsContainer) {
      console.error("Reviews container not found");
      return;
    }
    
    const reviewCards = Array.from(reviewsContainer.querySelectorAll('.review-card'));
    if (reviewCards.length === 0) {
      console.log("No review cards found");
      return;
    }
    
    console.log("Found " + reviewCards.length + " review cards");
    
    reviewCards.sort(function(a, b) {
      // Count filled stars for rating (only the solid ones, not the empty ones)
      const aRating = a.querySelectorAll('.fas.fa-star').length;
      const bRating = b.querySelectorAll('.fas.fa-star').length;
      
      // Parse dates from the text content
      const aDateText = a.querySelector('.review-date').textContent.trim();
      const bDateText = b.querySelector('.review-date').textContent.trim();
      
      // Handle date parsing, extract date parts
      const aDateMatch = aDateText.match(/(\w+) (\d+), (\d+)/);
      const bDateMatch = bDateText.match(/(\w+) (\d+), (\d+)/);
      
      let aDate, bDate;
      if (aDateMatch && bDateMatch) {
        aDate = new Date(aDateMatch[0]);
        bDate = new Date(bDateMatch[0]);
      } else {
        // Fallback if date format doesn't match
        aDate = new Date();
        bDate = new Date();
      }
      
      console.log(`Comparing: A(${aRating} stars, ${aDateText}) - B(${bRating} stars, ${bDateText})`);
      
      switch(sortOption) {
        case 'high-to-low':
          return bRating - aRating;
        case 'low-to-high':
          return aRating - bRating;
        case 'newest':
          return bDate - aDate;
        case 'oldest':
          return aDate - bDate;
        default:
          return 0;
      }
    });
    
    // Remove all existing cards
    reviewCards.forEach(card => card.remove());
    
    // Add the sorted cards back
    reviewCards.forEach(card => reviewsContainer.appendChild(card));
    
    console.log("Reviews sorted by: " + sortOption);
    
    // Check if any reviews are visible
    if (reviewCards.length === 0) {
      const noReviewsElement = document.createElement('p');
      noReviewsElement.className = 'no-reviews';
      noReviewsElement.textContent = 'No reviews match your filter criteria.';
      reviewsContainer.appendChild(noReviewsElement);
    }
  }
}); 