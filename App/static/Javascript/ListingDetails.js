let images = [];
let currentIndex = 0;

document.getElementById("imageUpload")?.addEventListener("change", function (e) {
  images = Array.from(e.target.files).map(file => URL.createObjectURL(file));
  currentIndex = 0;
  displayImage();
});

function displayImage() {
  const display = document.getElementById("imageDisplay");
  if (!display) return;
  
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
  const featuredImage = document.getElementById('featured-image');
  if (!featuredImage) return;
  
  featuredImage.src = src;
  
  const thumbnails = document.querySelectorAll('.thumbnail');
  thumbnails.forEach(thumb => {
    if (thumb.querySelector('img').src === src) {
      thumb.classList.add('active');
    } else {
      thumb.classList.remove('active');
    }
  });
}

// Map globals
let map = null;
let marker = null;
let isFullscreen = false;
let exitBtn = null;

// OpenStreetMap Implementation
document.addEventListener('DOMContentLoaded', function() {
  setTimeout(initMap, 100);
  setupSaveButtonListeners();
});

function initMap() {
  const mapContainer = document.getElementById('map');
  if (!mapContainer) return;
  
  mapContainer.style.minHeight = '300px';
  mapContainer.style.display = 'block';
  
  mapContainer.innerHTML = '<div class="map-loading">Loading map...</div>';
  
  const address = mapContainer.getAttribute('data-address');
  if (!address) {
    mapContainer.innerHTML = '<div class="map-error">No address provided</div>';
    return;
  }
  
  //Fullscreen button
  exitBtn = document.createElement('button');
  exitBtn.className = 'map-fullscreen-exit';
  exitBtn.innerHTML = '<i class="fas fa-compress"></i>';
  exitBtn.style.display = 'none';
  document.body.appendChild(exitBtn);
  
  exitBtn.addEventListener('click', toggleFullscreen);
  
  const fullscreenBtn = document.getElementById('fullscreen-btn');
  if (fullscreenBtn) {
    fullscreenBtn.addEventListener('click', toggleFullscreen);
  }
  
  mapContainer.innerHTML = '';
  
  try {
    //Initialize map with Trinidad and Tobago as default
    map = L.map(mapContainer, {
      center: [10.6918, -61.2225], 
      zoom: 9, 
      zoomControl: true,
    });
    
    setTimeout(function() {
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
      }).addTo(map);
      
      map.invalidateSize(true);
      geocodeAddress(address);
    }, 50);
    
    [100, 500, 1000].forEach(delay => {
      setTimeout(() => map && map.invalidateSize(true), delay);
    });
    
    window.addEventListener('load', () => {
      if (map) {
        map.invalidateSize(true);
        setTimeout(() => map.invalidateSize(true), 500);
      }
    });
    
    window.addEventListener('resize', () => map && map.invalidateSize(true));
    
  } catch (error) {
    mapContainer.innerHTML = '<div class="map-error">Error initializing map</div>';
  }
}

function geocodeAddress(address) {
  //Trinidad and Tobago coords for fallback
  const fallbackLat = 10.6918;
  const fallbackLon = -61.2225;
  
  fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`)
    .then(response => response.json())
    .then(data => {
      if (data && data.length > 0) {
        const lat = parseFloat(data[0].lat);
        const lon = parseFloat(data[0].lon);
        
        map.setView([lat, lon], 15);
        
        // Add marker
        if (marker) {
          marker.setLatLng([lat, lon]);
        } else {
          marker = L.marker([lat, lon]).addTo(map)
            .bindPopup(address);
        }
        
        marker.openPopup();
        map.invalidateSize(true);
      } else {
        map.setView([fallbackLat, fallbackLon], 13);
        
        if (marker) {
          marker.setLatLng([fallbackLat, fallbackLon]);
        } else {
          marker = L.marker([fallbackLat, fallbackLon]).addTo(map)
            .bindPopup('Location not found: ' + address);
        }
        
        marker.openPopup();
        map.invalidateSize(true);
      }
    })
    .catch(error => {
      map.setView([fallbackLat, fallbackLon], 13);
      
      if (marker) {
        marker.setLatLng([fallbackLat, fallbackLon]);
      } else {
        marker = L.marker([fallbackLat, fallbackLon]).addTo(map)
          .bindPopup('Error finding location');
      }
      
      marker.openPopup();
      map.invalidateSize(true);
    });
}

function toggleFullscreen() {
  const mapContainer = document.getElementById('map');
  if (!mapContainer || !map) return;
  
  const fullscreenBtn = document.getElementById('fullscreen-btn');
  
  if (!isFullscreen) {
    mapContainer.classList.add('fullscreen-map');
    if (fullscreenBtn) fullscreenBtn.style.display = 'none';
    if (exitBtn) exitBtn.style.display = 'flex';
    isFullscreen = true;
  } else {
    mapContainer.classList.remove('fullscreen-map');
    if (fullscreenBtn) fullscreenBtn.style.display = 'flex';
    if (exitBtn) exitBtn.style.display = 'none';
    isFullscreen = false;
  }
  
  setTimeout(() => map.invalidateSize(true), 300);
}

function setupSaveButtonListeners() {
  const saveButton = document.querySelector('.save-button');
  if (!saveButton) return;
  
  saveButton.addEventListener('click', async function(e) {
    e.preventDefault();
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
      alert('Error saving apartment');
    }
  });
}