document.addEventListener("DOMContentLoaded", () => {
    const burger = document.getElementById("burger");
    const navLinks = document.getElementById("navLinks");
  
    burger.addEventListener("click", () => {
      navLinks.classList.toggle("active");
    });
  });

  function toggleTenantFields() {
    const userType = document.getElementById('user_type').value;
    const tenantFields = document.getElementById('tenant-fields');
    
    if (userType === 'Tenant') {
      tenantFields.style.display = 'block';
      const inputs = tenantFields.querySelectorAll('input');
      inputs.forEach(input => input.required = true);
    } else {
      tenantFields.style.display = 'none';
      const inputs = tenantFields.querySelectorAll('input');
      inputs.forEach(input => input.required = false);
    }
  }
  