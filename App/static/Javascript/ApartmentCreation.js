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
            
            additionalPreviewArea.style.display = 'flex';
            additionalPreviewArea.style.flexWrap = 'wrap';
            additionalPreviewArea.style.justifyContent = 'flex-start';
            additionalPreviewArea.style.gap = '10px';
            
            const files = Array.from(this.files);
            
            files.forEach((file, index) => {
                const previewContainer = document.createElement('div');
                previewContainer.className = 'preview-thumbnail';
                previewContainer.style.opacity = '0';
                previewContainer.style.transform = 'scale(0.8)';
                
                const img = document.createElement('img');
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    img.src = e.target.result;
                    
                    setTimeout(() => {
                        previewContainer.style.transition = 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
                        previewContainer.style.opacity = '1';
                        previewContainer.style.transform = 'scale(1)';
                    }, 100 * index);
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
            img.style.opacity = '0';
            img.style.transform = 'scale(0.95)';
            
            previewElement.appendChild(img);
            
            setTimeout(() => {
                img.style.transition = 'all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
                img.style.opacity = '1';
                img.style.transform = 'scale(1)';
            }, 100);
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

    // Enhance form validation
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('invalid');
                    
                    const formGroup = field.closest('.form-group');
                    if (formGroup && !formGroup.querySelector('.validation-message')) {
                        const message = document.createElement('div');
                        message.className = 'validation-message';
                        message.textContent = 'This field is required';
                        message.style.color = '#e74c3c';
                        message.style.fontSize = '12px';
                        message.style.marginTop = '5px';
                        formGroup.appendChild(message);
                        
                        // Animate the form group
                        formGroup.style.animation = 'shake 0.5s ease';
                    }
                } else {
                    field.classList.remove('invalid');
                    const formGroup = field.closest('.form-group');
                    const message = formGroup?.querySelector('.validation-message');
                    if (message) {
                        message.remove();
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
        
        form.addEventListener('keyup', function(e) {
            if (e.target.hasAttribute('required')) {
                if (e.target.value.trim()) {
                    e.target.classList.remove('invalid');
                    const formGroup = e.target.closest('.form-group');
                    const message = formGroup?.querySelector('.validation-message');
                    if (message) {
                        message.remove();
                    }
                }
            }
        });
    }
    
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
        
        .drag-over {
            border-color: #3498db !important;
            background-color: rgba(52, 152, 219, 0.1) !important;
            transform: scale(1.02) !important;
        }
        
        .focused {
            transform: translateY(-3px);
        }
        
        .submitting {
            pointer-events: none;
            opacity: 0.8;
        }
        
        /* Additional styles for horizontal layout */
        .preview-thumbnail {
            margin: 5px;
            flex: 0 0 auto;
        }
    `;
    document.head.appendChild(style);
}); 