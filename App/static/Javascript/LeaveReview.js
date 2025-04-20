document.getElementById('mediaInput')?.addEventListener('change', function () {
    const fileList = Array.from(this.files);
    if (fileList.length > 0) {
      alert(`${fileList.length} file(s) selected.`);
    }
  });
  
  document.querySelector('.submit-btn')?.addEventListener('click', function () {
    alert('Review submitted (functionality to be implemented)');
  });
  