let images = [];
let currentIndex = 0;

document.getElementById("imageUpload").addEventListener("change", function (e) {
  images = Array.from(e.target.files).map(file => URL.createObjectURL(file));
  currentIndex = 0;
  displayImage();
});

function displayImage() {
  const display = document.getElementById("imageDisplay");
  if (images.length === 0) {
    display.innerHTML = "No image selected";
    display.style.background = "#ddd";
  } else {
    display.innerHTML = `<img src="${images[currentIndex]}" style="width:100%; height:100%; object-fit:cover; border-radius:8px;">`;
    display.style.background = "transparent";
  }
}

function prevImage() {
  if (images.length === 0) return;
  currentIndex = (currentIndex - 1 + images.length) % images.length;
  displayImage();
}

function nextImage() {
  if (images.length === 0) return;
  currentIndex = (currentIndex + 1) % images.length;
  displayImage();
}

function changeImage(src) {
  document.getElementById('featured-image').src = src;
  
  const thumbnails = document.querySelectorAll('.thumbnail');
  thumbnails.forEach(thumb => {
    if (thumb.querySelector('img').src === src) {
      thumb.classList.add('active');
    } else {
      thumb.classList.remove('active');
    }
  });
}

// Initialize the map with OpenStreetMap and Leaflet
document.addEventListener('DOMContentLoaded', function() {
  const mapElement = document.getElementById('map');
  if (!mapElement) return;
  
  const address = mapElement.getAttribute('data-address');
  
  // Initialize the map centered at a default location (will be updated)
  const map = L.map('map').setView([0, 0], 15);
  
  // Add OpenStreetMap tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);
  
  // Use the Nominatim service to geocode the address
  fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`)
    .then(response => response.json())
    .then(data => {
      if (data && data.length > 0) {
        // Get the coordinates
        const lat = parseFloat(data[0].lat);
        const lon = parseFloat(data[0].lon);
        
        // Update map view
        map.setView([lat, lon], 15);
        
        L.marker([lat, lon]).addTo(map)
          .bindPopup(address)
          .openPopup();
      } else {
        // If geocoding fails
        mapElement.innerHTML = '<div class="map-error">Could not locate this address on the map</div>';
      }
    })
    .catch(error => {
      console.error('Error geocoding address:', error);
      mapElement.innerHTML = '<div class="map-error">Error loading map</div>';
    });
}); 