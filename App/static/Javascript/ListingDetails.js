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
  if (featuredImage) {
    featuredImage.src = src;
    
    // Update active thumbnail
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach(thumbnail => {
      if (thumbnail.querySelector('img').src === src) {
        thumbnail.classList.add('active');
      } else {
        thumbnail.classList.remove('active');
      }
    });
  }
}

// Map globals
let map = null;
let marker = null;
let isFullscreen = false;
let exitBtn = null;

document.addEventListener('DOMContentLoaded', function() {
  setTimeout(initMap, 100);
  setupSaveButtonListeners();
  setupImageFullscreen();
  
  document.addEventListener('fullscreenchange', function() {
    if (!document.fullscreenElement) {
      const fullscreenBtn = document.getElementById('fullscreen-btn');
      if (fullscreenBtn) fullscreenBtn.style.display = 'flex';
      
      const exitFullscreenBtn = document.getElementById('fullscreen-exit-btn');
      if (exitFullscreenBtn) exitFullscreenBtn.style.display = 'none';
      
      isFullscreen = false;
      
      setTimeout(() => {
        if (map) {
          console.log("Resizing map after fullscreen exit");
          map.invalidateSize(true);
        }
      }, 300);
    }
  });
});

function initMap() {
  const mapContainer = document.getElementById('map');
  if (!mapContainer) {
    console.error("Map container not found");
    return;
  }
  
  mapContainer.style.minHeight = '300px';
  mapContainer.style.display = 'block';
  
  mapContainer.innerHTML = '<div class="map-loading">Loading map...</div>';
  
  const address = mapContainer.getAttribute('data-address');
  if (!address) {
    mapContainer.innerHTML = '<div class="map-error">No address provided</div>';
    return;
  }
  
  const existingExitBtn = document.querySelector('.map-fullscreen-exit');
  if (existingExitBtn) {
    existingExitBtn.remove();
  }
  
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
    console.log("Initializing map with Leaflet");
    
    //Initialize map with Trinidad and Tobago as default
    if (typeof L !== 'undefined') {
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
    } else {
      console.error("Leaflet (L) is not defined");
      mapContainer.innerHTML = '<div class="map-error">Map library not loaded</div>';
    }
  } catch (error) {
    console.error("Error initializing map:", error);
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
  if (!mapContainer || !map) {
    console.error("Map container or map not available");
    return;
  }
  
  let exitFullscreenBtn = document.getElementById('fullscreen-exit-btn');
  if (!exitFullscreenBtn) {
    exitFullscreenBtn = document.createElement('button');
    exitFullscreenBtn.id = 'fullscreen-exit-btn';
    exitFullscreenBtn.className = 'fullscreen-exit-btn';
    exitFullscreenBtn.innerHTML = '<i class="fas fa-compress"></i>';
    exitFullscreenBtn.title = 'Exit Fullscreen';
    exitFullscreenBtn.addEventListener('click', function() {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
      } else if (document.msExitFullscreen) {
        document.msExitFullscreen();
      }
    });
    mapContainer.appendChild(exitFullscreenBtn);
  }
  
  if (!document.fullscreenElement) {
    console.log("Requesting fullscreen mode");
    
    if (mapContainer.requestFullscreen) {
      mapContainer.requestFullscreen();
    } else if (mapContainer.webkitRequestFullscreen) { 
      mapContainer.webkitRequestFullscreen();
    } else if (mapContainer.msRequestFullscreen) { 
      mapContainer.msRequestFullscreen();
    }
    
    const fullscreenBtn = document.getElementById('fullscreen-btn');
    if (fullscreenBtn) fullscreenBtn.style.display = 'none';
    
    if (exitFullscreenBtn) exitFullscreenBtn.style.display = 'flex';
    
    isFullscreen = true;
  } else {
    console.log("Exiting fullscreen mode");
    
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.webkitExitFullscreen) { 
      document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) { 
      document.msExitFullscreen();
    }
    
    isFullscreen = false;
  }
  
  setTimeout(() => {
    if (map) {
      console.log("Resizing map after fullscreen toggle");
      map.invalidateSize(true);
      
      if (isFullscreen && marker) {
        map.setView(marker.getLatLng(), map.getZoom());
      }
    }
  }, 300);
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

function setupImageFullscreen() {
  const mainImage = document.querySelector('.main-image');
  const featuredImage = document.getElementById('featured-image');
  const thumbnails = document.querySelectorAll('.thumbnail img');
  
  if (mainImage && featuredImage) {
    const allImages = [featuredImage.src];
    let currentImageIndex = 0;
    
    thumbnails.forEach(img => {
      if (img.src !== featuredImage.src) {
        allImages.push(img.src);
      }
    });
    
    const prevButton = document.createElement('button');
    prevButton.className = 'image-nav prev-image';
    prevButton.innerHTML = '<i class="fas fa-chevron-left"></i>';
    
    const nextButton = document.createElement('button');
    nextButton.className = 'image-nav next-image';
    nextButton.innerHTML = '<i class="fas fa-chevron-right"></i>';
    
    const pagination = document.createElement('div');
    pagination.className = 'image-pagination';
    pagination.innerHTML = `<span id="current-index">1</span>/<span id="total-images">${allImages.length}</span>`;
    
    mainImage.appendChild(prevButton);
    mainImage.appendChild(nextButton);
    mainImage.appendChild(pagination);
    
    function updateMainImage() {
      featuredImage.src = allImages[currentImageIndex];
      document.getElementById('current-index').textContent = currentImageIndex + 1;
      
      thumbnails.forEach((thumb, i) => {
        const thumbnailParent = thumb.closest('.thumbnail');
        if (thumb.src === allImages[currentImageIndex]) {
          thumbnailParent.classList.add('active');
        } else {
          thumbnailParent.classList.remove('active');
        }
      });
    }
    
    prevButton.addEventListener('click', function(e) {
      e.stopPropagation(); 
      currentImageIndex = (currentImageIndex - 1 + allImages.length) % allImages.length;
      updateMainImage();
    });
    
    nextButton.addEventListener('click', function(e) {
      e.stopPropagation(); 
      currentImageIndex = (currentImageIndex + 1) % allImages.length;
      updateMainImage();
    });
    
    thumbnails.forEach((thumbnail, index) => {
      thumbnail.addEventListener('click', function() {
        for (let i = 0; i < allImages.length; i++) {
          if (allImages[i] === this.src) {
            currentImageIndex = i;
            break;
          }
        }
        updateMainImage();
      });
    });
    
    document.addEventListener('keydown', function(e) {
      if (e.key === 'ArrowLeft') {
        currentImageIndex = (currentImageIndex - 1 + allImages.length) % allImages.length;
        updateMainImage();
      } else if (e.key === 'ArrowRight') {
        currentImageIndex = (currentImageIndex + 1) % allImages.length;
        updateMainImage();
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', function() {
    // Map initialization function
    initializeMap();
    
    // Initialize image gallery
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', function() {
            const mainImg = document.getElementById('main-image');
            mainImg.src = this.src;
        });
    });
});

// Initialize the map
function initializeMap() {
    const mapElement = document.getElementById('map');
    
    // If map element exists
    if (mapElement) {
        const addressElement = document.getElementById('apartment-address');
        const address = addressElement ? addressElement.textContent : '';
        
        // Display a static map if no interactive map is available
        if (!window.google || !window.google.maps) {
            mapElement.innerHTML = `
                <div class="static-map-fallback">
                    <p>Map location: ${address}</p>
                    <p class="small text-muted">Interactive map unavailable</p>
                </div>
            `;
        }
    }
}