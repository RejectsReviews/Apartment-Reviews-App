document.addEventListener('DOMContentLoaded', function() {
    // Handle heart button clicks
    document.querySelectorAll('.save-button').forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const apartmentId = this.dataset.apartmentId;
            const isSaved = this.classList.contains('saved');
            
            try {
                const response = await fetch(`/apartments/${apartmentId}/${isSaved ? 'unsave' : 'save'}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Toggle saved state
                    this.classList.toggle('saved');
                    const heartIcon = this.querySelector('i');
                    heartIcon.classList.toggle('fas');
                    heartIcon.classList.toggle('far');
                    
                    // Update tooltip
                    this.title = isSaved ? 'Save apartment' : 'Remove from saved';
                } else {
                    alert(data.error || 'Error saving apartment');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while saving the apartment');
            }
        });
    });

    // Location search functionality
    const searchInput = document.querySelector('.search-bar');
    const dropdownContainer = document.createElement('div');
    dropdownContainer.className = 'location-dropdown';
    searchInput.parentNode.insertBefore(dropdownContainer, searchInput.nextSibling);
    
    let debounceTimer;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        const query = this.value.trim();
        
        if (query.length < 2) {
            dropdownContainer.style.display = 'none';
            return;
        }
        
        // Debounce the API call
        debounceTimer = setTimeout(() => {
            fetch(`/api/locations?query=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(locations => {
                    if (locations.length > 0) {
                        const html = locations.map(location => 
                            `<div class="dropdown-item">${location}</div>`
                        ).join('');
                        dropdownContainer.innerHTML = html;
                        dropdownContainer.style.display = 'block';
                        
                        // Add click handlers to dropdown items
                        dropdownContainer.querySelectorAll('.dropdown-item').forEach(item => {
                            item.addEventListener('click', function() {
                                searchInput.value = this.textContent;
                                dropdownContainer.style.display = 'none';
                            });
                        });
                    } else {
                        dropdownContainer.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('Error fetching locations:', error);
                    dropdownContainer.style.display = 'none';
                });
        }, 300); // 300ms debounce delay
    });
    
    // Hide dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-bar') && !e.target.closest('.location-dropdown')) {
            dropdownContainer.style.display = 'none';
        }
    });
});