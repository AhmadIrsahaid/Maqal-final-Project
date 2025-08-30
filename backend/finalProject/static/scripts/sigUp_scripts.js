// Theme management
let currentTheme = "light";

// Initialize from localStorage
document.addEventListener("DOMContentLoaded", function () {
  const savedTheme = localStorage.getItem("theme") || "light";
  setTheme(savedTheme, false);

  // Initialize password strength checker
  const passwordField = document.querySelector('input[name="password1"]');
  if (passwordField) {
    passwordField.addEventListener("input", checkPasswordStrength);
    passwordField.addEventListener("focus", showPasswordRequirements);
  }
});

// Theme switching
function toggleTheme() {
  const newTheme = currentTheme === "light" ? "dark" : "light";
  setTheme(newTheme);
}

function setTheme(theme, animate = true) {
  currentTheme = theme;
  const body = document.body;
  const themeIcon = document.getElementById("themeIcon");

  if (animate) {
    body.style.transition = "all 0.3s ease";
  }

  if (theme === "dark") {
    document.documentElement.setAttribute("data-theme", "dark");
    themeIcon.className = "fas fa-moon";
  } else {
    document.documentElement.removeAttribute("data-theme");
    themeIcon.className = "fas fa-sun";
  }

  localStorage.setItem("theme", theme);

  setTimeout(() => {
    body.style.transition = "";
  }, 300);
}

// Toggle password visibility
function togglePassword(fieldId) {
  const passwordInput = document.getElementById(fieldId);
  const toggleIcon = document.querySelector(`.toggle-icon-${fieldId}`);

  if (passwordInput && toggleIcon) {
    if (passwordInput.type === "password") {
      passwordInput.type = "text";
      toggleIcon.classList.remove("fa-eye");
      toggleIcon.classList.add("fa-eye-slash");
    } else {
      passwordInput.type = "password";
      toggleIcon.classList.remove("fa-eye-slash");
      toggleIcon.classList.add("fa-eye");
    }
  }
}

// Password strength checker
function checkPasswordStrength() {
  const password = this.value;
  const strengthBar = document.getElementById("passwordStrengthBar");
  const strengthContainer = document.getElementById("passwordStrength");

  if (!strengthBar || !strengthContainer) return;

  let strength = 0;
  let strengthClass = "";

  // Check requirements
  const requirements = {
    length: password.length >= 8,
    upper: /[A-Z]/.test(password),
    lower: /[a-z]/.test(password),
    number: /\d/.test(password),
  };

  // Update requirement indicators
  updateRequirement("lengthReq", requirements.length);
  updateRequirement("upperReq", requirements.upper);
  updateRequirement("lowerReq", requirements.lower);
  updateRequirement("numberReq", requirements.number);

  // Calculate strength
  Object.values(requirements).forEach((met) => {
    if (met) strength++;
  });

  // Set strength class
  if (strength === 1) strengthClass = "strength-weak";
  else if (strength === 2) strengthClass = "strength-fair";
  else if (strength === 3) strengthClass = "strength-good";
  else if (strength === 4) strengthClass = "strength-strong";

  // Update UI
  strengthContainer.style.display = password ? "block" : "none";
  strengthBar.className = `password-strength-bar ${strengthClass}`;
}

function updateRequirement(id, met) {
  const element = document.getElementById(id);
  if (element) {
    const icon = element.querySelector("i");
    if (met) {
      element.classList.add("met");
      icon.classList.remove("fa-times");
      icon.classList.add("fa-check");
    } else {
      element.classList.remove("met");
      icon.classList.remove("fa-check");
      icon.classList.add("fa-times");
    }
  }
}

function showPasswordRequirements() {
  const requirements = document.getElementById("passwordRequirements");
  if (requirements) {
    requirements.style.display = "block";
  }
}

// Form submission handling
document.getElementById("signupForm").addEventListener("submit", function (e) {
  // Don't prevent default for actual Django form submission
  // e.preventDefault(); // Remove this in actual implementation

  const form = this;
  const button = form.querySelector(".btn-signup");
  const buttonSpan = button.querySelector("span");

  // Add loading state
  form.classList.add("loading");
  const originalText = buttonSpan.textContent;
  buttonSpan.textContent = "Creating Account...";

  // For demo purposes only - remove in actual implementation
  e.preventDefault();
  setTimeout(() => {
    showSuccessMessage();
  }, 2000);
});

// Show success message
// function showSuccessMessage() {
//   const card = document.getElementById("signupCard");
//   card.innerHTML = `
//                 <div class="success-animation">
//                     <div class="success-icon">
//                         <i class="fas fa-check"></i>
//                     </div>
//                     <h2 style="color: var(--success-color); margin-bottom: 1rem;">Account Created!</h2>
//                     <p style="color: var(--text-light); margin-bottom: 2rem;">
//                         Your account has been successfully created.
//                         Please check your email to verify your account.
//                     </p>
//                     <a href="{%%}" class="btn btn-signup" style="display: inline-block; width: auto; padding: 0.7rem 2rem;">
//                         <i class="fas fa-sign-in-alt me-2"></i>
//                         Go to Login
//                     </a>
//                 </div>
//             `;
// }

// Show message function
function showMessage(message, type) {
  const alertDiv = document.createElement("div");
  alertDiv.className = `alert alert-${
    type === "success" ? "success" : "danger"
  } alert-dismissible fade show position-fixed`;
  alertDiv.style.cssText =
    "top: 20px; left: 20px; z-index: 9999; max-width: 300px;";
  alertDiv.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;

  document.body.appendChild(alertDiv);

  setTimeout(() => {
    alertDiv.remove();
  }, 5000);
}

// Add input animations
document.querySelectorAll("input, select, textarea").forEach((input) => {
  input.addEventListener("focus", function () {
    this.parentElement.classList.add("focused");
  });

  input.addEventListener("blur", function () {
    if (!this.value) {
      this.parentElement.classList.remove("focused");
    }
  });
});

// Add smooth scrolling and animations
window.addEventListener("load", function () {
  document.body.style.opacity = "1";
});

// Keyboard shortcuts
document.addEventListener("keydown", function (e) {
  if (e.key === "Enter" && e.ctrlKey) {
    document.getElementById("signupForm").dispatchEvent(new Event("submit"));
  }
});
