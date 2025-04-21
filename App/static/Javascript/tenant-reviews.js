document.addEventListener('DOMContentLoaded', function() {
  // Modal elements
  const deleteModal = document.getElementById('deleteModal');
  const deleteForm = document.getElementById('deleteForm');
  const cancelButton = document.querySelector('.cancel-button');
  
  // Find all delete buttons
  const deleteButtons = document.querySelectorAll('[data-action="delete"]');
  
  // Add click event to all delete buttons
  deleteButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const reviewId = this.getAttribute('data-review-id');
      
      // Set the form action to the correct delete URL
      deleteForm.action = `/review/${reviewId}/delete`;
      
      // Show the modal
      deleteModal.style.display = 'flex';
    });
  });
  
  // Close modal when cancel button is clicked
  cancelButton.addEventListener('click', function() {
    deleteModal.style.display = 'none';
  });
  
  // Close modal when clicking outside of it
  window.addEventListener('click', function(event) {
    if (event.target === deleteModal) {
      deleteModal.style.display = 'none';
    }
  });
  
  // Close modal on escape key
  document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' && deleteModal.style.display === 'flex') {
      deleteModal.style.display = 'none';
    }
  });
}); 