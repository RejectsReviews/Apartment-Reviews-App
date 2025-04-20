$(document).ready(function() {
  $('.location-select').select2({ 
    placeholder: "Select location", 
    width: "100%" 
  });
  
  $('.amenities-select').select2({ 
    placeholder: "Select amenities", 
    width: "100%" 
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