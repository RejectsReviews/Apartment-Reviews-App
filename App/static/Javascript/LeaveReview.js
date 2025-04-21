document.getElementById('mediaInput')?.addEventListener('change', function () {
    const fileList = Array.from(this.files);
    if (fileList.length > 0) {
      alert(`${fileList.length} file(s) selected.`);
    }
});
