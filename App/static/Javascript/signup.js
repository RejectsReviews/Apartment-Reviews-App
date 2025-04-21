document.addEventListener("DOMContentLoaded", () => {
    const burger = document.getElementById("burger");
    const navLinks = document.getElementById("navLinks");
    const phoneInput = document.querySelector('input[name="phone"]');
  
    burger.addEventListener("click", () => {
      navLinks.classList.toggle("active");
    });

    // Phone number validation
    phoneInput.addEventListener('input', (e) => {
      e.target.value = e.target.value.replace(/[^0-9]/g, '').slice(0, 10);
    });
});

function toggleTenantFields() {
    const userType = document.getElementById('user_type').value;
    const tenantFields = document.getElementById('tenant-fields');
    
    if (userType === 'Tenant') {
      tenantFields.style.display = 'none';
    } else {
      tenantFields.style.display = 'none';
    }
}
