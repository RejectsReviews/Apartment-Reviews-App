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
