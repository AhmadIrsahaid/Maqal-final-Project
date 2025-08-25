let currentLang = "ar";
let currentTheme = "light";

document.addEventListener("DOMContentLoaded", function () {
  const savedLang = localStorage.getItem("language") || "ar";
  const savedTheme = localStorage.getItem("theme") || "light";

  setLanguage(savedLang, false);
  setTheme(savedTheme, false);


  document.querySelectorAll(".form-control").forEach((input) => {
    input.addEventListener("focus", function () {
      this.parentElement.classList.add("focused");
    });
    input.addEventListener("blur", function () {
      if (!this.value) this.parentElement.classList.remove("focused");
    });
  });

  const form = document.getElementById("loginForm");
  if (form) {
    form.addEventListener("submit", function (e) {
      const isDemo = this.dataset.demo === "true";
      const button = this.querySelector(".btn-login");
      const buttonSpan = button ? button.querySelector("span") : null;
      const originalText = buttonSpan ? buttonSpan.textContent : "";

      this.classList.add("loading");
      if (buttonSpan) {
        buttonSpan.textContent =
          currentLang === "ar" ? "جاري تسجيل الدخول..." : "Signing in...";
      }

      if (isDemo) {

        e.preventDefault();
        setTimeout(() => {
          this.classList.remove("loading");
          if (buttonSpan) buttonSpan.textContent = originalText;
          showMessage(
            currentLang === "ar" ? "تم تسجيل الدخول بنجاح!" : "Login successful!",
            "success"
          );
        }, 1500);
      }
    });
  }
});

function syncLangButtons(lang) {
  const arBtn = document.getElementById("arabicBtn");
  const enBtn = document.getElementById("englishBtn");
  if (arBtn && enBtn) {
    arBtn.classList.toggle("active", lang === "ar");
    enBtn.classList.toggle("active", lang === "en");
  }
}

function syncDirAwareIcons() {
  const rtl = document.documentElement.dir === "rtl";
  document.querySelectorAll(".dir-arrow").forEach((i) => {
    // Bootstrap Icons
    i.classList.toggle("bi-arrow-right-short", rtl);
    i.classList.toggle("bi-arrow-left-short", !rtl);
    i.classList.toggle("fa-arrow-right", rtl);
    i.classList.toggle("fa-arrow-left", !rtl);
  });
}

function setLanguage(lang, animate = true) {
  currentLang = lang;
  const html = document.documentElement;
  const body = document.body;

  if (animate) body.style.transition = "all 0.3s ease";

  html.setAttribute("lang", lang);
  html.setAttribute("dir", lang === "ar" ? "rtl" : "ltr");
  body.setAttribute("dir", lang === "ar" ? "rtl" : "ltr");


  const loginIcon = document.getElementById("loginIcon");
  if (loginIcon) {
    if (lang === "ar") {
      loginIcon.className = "bi bi-box-arrow-in-left me-2";
    } else {
      loginIcon.className = "bi bi-box-arrow-in-right ms-2";
    }
  }

  updateTexts();
  syncLangButtons(lang);
  syncDirAwareIcons();

  localStorage.setItem("language", lang);
  setTimeout(() => (body.style.transition = ""), 300);
}

function toggleTheme() {
  const newTheme = currentTheme === "light" ? "dark" : "light";
  setTheme(newTheme);
}

function setTheme(theme, animate = true) {
  currentTheme = theme;
  const body = document.body;
  const icon = document.getElementById("themeIcon");

  if (animate) body.style.transition = "all 0.3s ease";

  if (theme === "dark") {
    document.documentElement.setAttribute("data-theme", "dark");
    if (icon) {
      if (icon.classList.contains("bi")) {
        icon.classList.add("bi-moon");
        icon.classList.remove("bi-brightness-high");
      } else {
        icon.classList.add("fa-moon");
        icon.classList.remove("fa-sun");
      }
    }
  } else {
    document.documentElement.removeAttribute("data-theme");
    if (icon) {
      if (icon.classList.contains("bi")) {
        icon.classList.add("bi-brightness-high");
        icon.classList.remove("bi-moon");
      } else {
        icon.classList.add("fa-sun");
        icon.classList.remove("fa-moon");
      }
    }
  }

  localStorage.setItem("theme", theme);
  setTimeout(() => (body.style.transition = ""), 300);
}

function updateTexts() {
  // نصوص العناصر
  document.querySelectorAll("[data-ar],[data-en]").forEach((el) => {
    const arText = el.getAttribute("data-ar");
    const enText = el.getAttribute("data-en");
    if (arText != null || enText != null) {
      el.textContent = currentLang === "ar" ? arText ?? enText : enText ?? arText;
    }
  });

  // Placeholders
  document.querySelectorAll("[data-placeholder-ar],[data-placeholder-en]").forEach((el) => {
    const arPh = el.getAttribute("data-placeholder-ar");
    const enPh = el.getAttribute("data-placeholder-en");
    if (arPh != null || enPh != null) {
      el.setAttribute("placeholder", currentLang === "ar" ? arPh ?? enPh : enPh ?? arPh);
    }
  });
}

function togglePassword(fieldId = null) {
  const inputs = fieldId
    ? [document.getElementById(fieldId)].filter(Boolean)
    : Array.from(document.querySelectorAll('input[type="password"], input[type="text"]')).filter(
        (el) => el.type === "password" || el.dataset.togglePw === "true"
      );

  inputs.forEach((input) => {
    const id = input.id;
    const icon =
      document.querySelector(`.toggle-icon-${id}`) || document.getElementById("toggleIcon");

    if (input.type === "password") {
      input.type = "text";
      if (icon) {
        if (icon.classList.contains("bi")) {
          icon.classList.remove("bi-eye");
          icon.classList.add("bi-eye-slash");
        } else {
          icon.classList.remove("fa-eye");
          icon.classList.add("fa-eye-slash");
        }
      }
    } else {
      input.type = "password";
      if (icon) {
        if (icon.classList.contains("bi")) {
          icon.classList.remove("bi-eye-slash");
          icon.classList.add("bi-eye");
        } else {
          icon.classList.remove("fa-eye-slash");
          icon.classList.add("fa-eye");
        }
      }
    }
  });
}

function showMessage(message, type) {
  const alertDiv = document.createElement("div");
  alertDiv.className = `alert alert-${type === "success" ? "success" : "danger"} alert-dismissible fade show position-fixed`;
  alertDiv.style.cssText = "top: 20px; right: 20px; z-index: 9999; max-width: 320px;";
  alertDiv.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  `;
  document.body.appendChild(alertDiv);
  setTimeout(() => alertDiv.remove(), 5000);
}


window.addEventListener("load", function () {
  document.body.style.opacity = "1";
});


document.addEventListener("keydown", function (e) {
  if (e.key === "Enter" && e.ctrlKey) {
    const form = document.getElementById("loginForm");
    if (form) form.dispatchEvent(new Event("submit", { cancelable: true }));
  }
});
