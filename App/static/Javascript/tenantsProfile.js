document.addEventListener("DOMContentLoaded", () => {
    const allStars = document.querySelectorAll(".stars");
  
    allStars.forEach(group => {
      const stars = group.querySelectorAll(".star");
      stars.forEach(star => {
        star.addEventListener("click", () => {
          const value = parseInt(star.dataset.value);
          stars.forEach(s => {
            s.classList.toggle("selected", parseInt(s.dataset.value) <= value);
          });
        });
      });
    });
  });
  