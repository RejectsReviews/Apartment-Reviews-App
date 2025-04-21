$(document).ready(function() {
  $('.location-select').select2({ 
    placeholder: "Select location", 
    width: "100%" 
  });
  
  $('.amenities-select').select2({
    placeholder: "Select amenities available at your property",
    width: "100%",
    closeOnSelect: false,
    allowClear: false,
    tags: false
  }).on("select2:open", function() {
    $(".select2-results__options").css({
      "padding": "4px"
    });
  });

  // Fix for the clear button positioning
  $('.select2-selection--multiple').css('position', 'relative');
  
  // Add tooltip for clear button
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

  $('input[name="cover_image"]').change(function() {
    previewImage(this, 'cover-image-preview');
  });

  $('input[name="additional_images"]').change(function() {
    const files = this.files;
    const previewContainer = $('#additional-images-preview');
    
    previewContainer.empty();
    
    for (let i = 0; i < Math.min(files.length, 4); i++) {
      const file = files[i];
      if (file && file.type.match('image.*')) {
        const reader = new FileReader();
        reader.onload = function(e) {
          const imgHtml = `<div class="preview-thumbnail">
                            <img src="${e.target.result}" alt="Preview image">
                          </div>`;
          previewContainer.append(imgHtml);
        };
        reader.readAsDataURL(file);
      }
    }
  });
});

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
      preview.html(`<img src="${e.target.result}" alt="Preview image">`);
      preview.show();
    };
    reader.readAsDataURL(input.files[0]);
  } else {
    preview.hide();
  }
}

document.addEventListener('DOMContentLoaded', function() {
    if (typeof $.fn.select2 === 'function') {
        $('.amenities-select').select2({
            placeholder: "Select amenities...",
            allowClear: true,
            width: '100%'
        });
    }

    const coverImageInput = document.querySelector('input[name="cover_image"]');
    const coverPreviewArea = document.getElementById('cover-image-preview');
    
    if (coverImageInput && coverPreviewArea) {
        coverImageInput.addEventListener('change', function() {
            showImagePreview(this.files[0], coverPreviewArea);
        });
    }
    
    const additionalImagesInput = document.querySelector('input[name="additional_images"]');
    const additionalPreviewArea = document.getElementById('additional-images-preview');
    
    if (additionalImagesInput && additionalPreviewArea) {
        additionalImagesInput.addEventListener('change', function() {
            additionalPreviewArea.innerHTML = '';
            
            const files = Array.from(this.files).slice(0, 4);
            
            files.forEach(file => {
                const previewContainer = document.createElement('div');
                previewContainer.className = 'preview-thumbnail';
                
                const img = document.createElement('img');
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    img.src = e.target.result;
                }
                
                reader.readAsDataURL(file);
                previewContainer.appendChild(img);
                additionalPreviewArea.appendChild(previewContainer);
            });
        });
    }
    
    function showImagePreview(file, previewElement) {
        if (!file || !previewElement) return;
        
        const reader = new FileReader();
        
        reader.onload = function(e) {
            previewElement.innerHTML = '';
            const img = document.createElement('img');
            img.src = e.target.result;
            previewElement.appendChild(img);
        }
        
        reader.readAsDataURL(file);
    }
    
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        const label = checkbox.closest('label');
        if (label) {
            label.classList.add('checkbox-label');
        }
    });
}); 