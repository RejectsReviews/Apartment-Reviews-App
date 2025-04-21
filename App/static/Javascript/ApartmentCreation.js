$(document).ready(function() {
  $('.horizontal-layout').each(function(index) {
    $(this).css('opacity', '0');
    $(this).css('transform', 'translateY(20px)');
    
    setTimeout(() => {
      $(this).css('transition', 'all 0.4s ease');
      $(this).css('opacity', '1');
      $(this).css('transform', 'translateY(0)');
    }, index * 120);
  });

  adjustLayout();
  $(window).resize(adjustLayout);

  $('.location-select').select2({ 
    placeholder: "Select location", 
    width: "100%",
    dropdownCssClass: "animated-dropdown"
  });
  
  $('.amenities-select').select2({
    placeholder: "Select amenities available at your property",
    width: "100%",
    closeOnSelect: false,
    allowClear: false,
    tags: false,
    dropdownCssClass: "animated-dropdown"
  }).on("select2:open", function() {
    $(".select2-results__options").css({
      "padding": "8px"
    });
    
    setTimeout(() => {
      $(".select2-results__option").each(function(index) {
        $(this).css('opacity', '0');
        $(this).css('transform', 'translateY(8px)');
        
        setTimeout(() => {
          $(this).css('transition', 'all 0.3s ease');
          $(this).css('opacity', '1');
          $(this).css('transform', 'translateY(0)');
        }, index * 30);
      });
    }, 100);
  });

  $('.select2-selection--multiple').css('position', 'relative');
  
  $(document).on('mouseenter', '.select2-selection__clear', function() {
    $(this).attr('title', 'Clear all amenities');
  });

  const selectedAmenities = $('.amenities-select').data('selected') || [];
  if (selectedAmenities.length > 0) {
    $('.amenities-select').val(selectedAmenities).trigger('change');
  }
  
  fixSelect2Spacing();
  $('.amenities-select').on('change', function() {
    fixSelect2Spacing();
    $('.select2-selection--multiple').css('position', 'relative');
  });

  $('input[type="file"]').each(function() {
    const $input = $(this);
    const $container = $input.closest('.file-upload-container');
    
    $container.on('dragover', function(e) {
      e.preventDefault();
      e.stopPropagation();
      $(this).addClass('drag-over');
    });
    
    $container.on('dragleave', function(e) {
      e.preventDefault();
      e.stopPropagation();
      $(this).removeClass('drag-over');
    });
    
    $container.on('drop', function(e) {
      e.preventDefault();
      e.stopPropagation();
      $(this).removeClass('drag-over');
      
      if (e.originalEvent.dataTransfer.files.length) {
        $input[0].files = e.originalEvent.dataTransfer.files;
        $input.trigger('change');
      }
    });
  });

  $('input[name="cover_image"]').change(function() {
    previewImage(this, 'cover-image-preview');
  });

  $('input[name="additional_images"]').change(function() {
    const files = this.files;
    const previewContainer = $('#additional-images-preview');
    
    previewContainer.empty();
    
    if (files.length > 0) {
      previewContainer.css('display', 'flex');
      previewContainer.css('flex-wrap', 'wrap');
      previewContainer.css('justify-content', 'flex-start');
    }
    
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      if (file && file.type.match('image.*')) {
        const reader = new FileReader();
        reader.onload = function(e) {
          const imgHtml = `<div class="preview-thumbnail" style="opacity: 0; transform: scale(0.8);">
                            <img src="${e.target.result}" alt="Preview image">
                          </div>`;
          const $thumbnail = $(imgHtml);
          previewContainer.append($thumbnail);
          
          setTimeout(() => {
            $thumbnail.css('transition', 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)');
            $thumbnail.css('opacity', '1');
            $thumbnail.css('transform', 'scale(1)');
          }, 100 * i);
        };
        reader.readAsDataURL(file);
      }
    }
  });

  $('form').on('submit', function() {
    $('button[type="submit"]').addClass('submitting');
    $('button[type="submit"]').text('Creating...');
    return true;
  });

  $('input, textarea, select').on('focus', function() {
    $(this).closest('.form-group').addClass('focused');
  }).on('blur', function() {
    $(this).closest('.form-group').removeClass('focused');
  });
});

function adjustLayout() {
  const windowWidth = $(window).width();
  
  if (windowWidth > 1400) {
    $('.horizontal-layout .form-section-title').css('min-width', '140px');
    $('.image-preview').css('height', '160px');
  } else if (windowWidth > 992) {
    $('.horizontal-layout .form-section-title').css('min-width', '120px');
    $('.image-preview').css('height', '180px');
  } else {
    $('.horizontal-layout .form-section-title').css('min-width', '');
    $('.image-preview').css('height', '200px');
  }
}

function fixSelect2Spacing() {
  setTimeout(function() {
    $(".select2-container--default .select2-selection--multiple .select2-selection__rendered").css({
      "display": "block",
      "padding": "0",
      "margin": "0",
      "line-height": "1.5"
    });
  }, 50);
}

function previewImage(input, previewElementId) {
  const preview = $(`#${previewElementId}`);
  
  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = function(e) {
      preview.html(`<img src="${e.target.result}" alt="Preview image" style="opacity: 0; transform: scale(0.95);">`);
      preview.show();
      
      setTimeout(() => {
        preview.find('img').css('transition', 'all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)');
        preview.find('img').css('opacity', '1');
        preview.find('img').css('transform', 'scale(1)');
      }, 100);
    };
    reader.readAsDataURL(input.files[0]);
  } else {
    preview.hide();
  }
}

document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const form = document.getElementById('apartment-form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Required fields
            const required = ['title', 'description', 'address', 'city', 'price', 'bedrooms', 'bathrooms'];
            
            required.forEach(field => {
                const input = document.getElementById(field);
                if (input && !input.value.trim()) {
                    isValid = false;
                    highlightError(input);
                } else if (input) {
                    removeError(input);
                }
            });
            
            // Price validation
            const price = document.getElementById('price');
            if (price && (isNaN(price.value) || parseFloat(price.value) <= 0)) {
                isValid = false;
                highlightError(price);
            }
            
            if (!isValid) {
                e.preventDefault();
                document.getElementById('error-message').classList.remove('d-none');
                window.scrollTo(0, 0);
            }
        });
        
        // Amenity checkboxes
        const amenitiesContainer = document.getElementById('amenities-container');
        if (amenitiesContainer) {
            const searchBox = document.getElementById('amenity-search');
            if (searchBox) {
                searchBox.addEventListener('input', function() {
                    const query = this.value.toLowerCase();
                    const amenities = amenitiesContainer.querySelectorAll('.amenity-item');
                    
                    amenities.forEach(item => {
                        const text = item.textContent.toLowerCase();
                        if (text.includes(query)) {
                            item.style.display = '';
                        } else {
                            item.style.display = 'none';
                        }
                    });
                });
            }
        }
    }
    
    // Helper functions
    function highlightError(element) {
        element.classList.add('is-invalid');
    }
    
    function removeError(element) {
        element.classList.remove('is-invalid');
    }
    
    // Initialize map if available
    function initMap() {
        const mapElement = document.getElementById('map');
        
        if (mapElement && window.google && window.google.maps) {
            // Initialize map with geocoding capabilities
            const addressInput = document.getElementById('address');
            const cityInput = document.getElementById('city');
            
            if (addressInput && cityInput) {
                // Combine for geocoding
                const updateMap = () => {
                    const address = `${addressInput.value}, ${cityInput.value}`;
                    // Geocoding would happen here
                };
                
                addressInput.addEventListener('blur', updateMap);
                cityInput.addEventListener('blur', updateMap);
            }
        } else if (mapElement) {
            // Fallback for no Google Maps
            mapElement.innerHTML = '<div class="p-3 bg-light text-center">Map loading...</div>';
        }
    }
    
    // Call map init
    if (document.getElementById('map')) {
        // This would normally be called by the Google Maps script
        if (window.google && window.google.maps) {
            initMap();
        } else {
            // Mock for now
            initMap();
        }
    }
}); 