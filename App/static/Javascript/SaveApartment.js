document.addEventListener('DOMContentLoaded', function() {
    const saveButtons = document.querySelectorAll('.save-button');
    saveButtons.forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            e.stopPropagation();
            const apartmentId = this.dataset.apartmentId;
            const apartmentCard = this.closest('.apartment-card');
            
            try {
                const response = await fetch(`/apartments/${apartmentId}/unsave`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Remove the apartment card with animation
                    apartmentCard.style.transition = 'opacity 0.3s, transform 0.3s';
                    apartmentCard.style.opacity = '0';
                    apartmentCard.style.transform = 'scale(0.9)';
                    
                    setTimeout(() => {
                        apartmentCard.remove();
                        
                        // Check if there are no more apartments
                        const remainingCards = document.querySelectorAll('.apartment-card');
                        if (remainingCards.length === 0) {
                            const grid = document.querySelector('.apartments-grid');
                            grid.innerHTML = `
                                <div class="no-apartments">
                                    <p>You haven't saved any apartments yet.</p>
                                    <a href="/apartments" class="view-details">Browse Listings</a>
                                </div>
                            `;
                        }
                    }, 300);
                } else {
                    alert(data.error || 'Error removing apartment from saved list');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error removing apartment from saved list');
            }
        });
    });
});