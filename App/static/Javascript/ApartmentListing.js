document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navToggle.classList.toggle('active');
            navLinks.classList.toggle('active');
        });
    }
    
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 10) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    if (jQuery && jQuery.fn && jQuery.fn.select2) {
        $('.amenities-filter').select2({
            placeholder: "Filter by Amenities",
            allowClear: true,
            closeOnSelect: false,
            templateSelection: function(data) {
                return $('<span>').text(data.text.replace(/^x/, '')).html();
            }
        });
    }

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
                    this.classList.toggle('saved');
                    const heartIcon = this.querySelector('i');
                    heartIcon.classList.toggle('fas');
                    heartIcon.classList.toggle('far');
                    
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

    const searchInput = document.querySelector('.search-bar');
    if (searchInput) {
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
            }, 300); 
        });
        
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.search-bar') && !e.target.closest('.location-dropdown')) {
                dropdownContainer.style.display = 'none';
            }
        });
    }
});