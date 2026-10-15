const navToggle = document.querySelector("[data-nav-toggle]");
const nav = document.querySelector("[data-nav]");

if (navToggle && nav) {
  const setNavigationState = (open) => {
    navToggle.setAttribute("aria-expanded", String(open));
    navToggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
    nav.classList.toggle("primary-nav--open", open);
  };
  navToggle.addEventListener("click", () => {
    setNavigationState(navToggle.getAttribute("aria-expanded") !== "true");
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && navToggle.getAttribute("aria-expanded") === "true") {
      setNavigationState(false);
      navToggle.focus();
    }
  });
}

document.querySelectorAll("[data-dismiss-flash]").forEach((button) => {
  button.addEventListener("click", () => button.closest(".flash")?.remove());
});

const bmiForm = document.querySelector("[data-bmi-form]");
const profileForm = document.querySelector("[data-profile-form]");
if (profileForm) {
  const institutionalFields = profileForm.querySelector("[data-institution-fields]");
  const syncProfileMode = () => {
    if (!institutionalFields) return;
    const institutional = profileForm.querySelector('[name="usage_mode"]:checked')?.value === "institutional";
    institutionalFields.hidden = !institutional;
    institutionalFields.disabled = !institutional;
  };
  profileForm.querySelectorAll('[name="usage_mode"]').forEach((radio) => {
    radio.addEventListener("change", syncProfileMode);
  });
  window.addEventListener("pageshow", syncProfileMode);
  syncProfileMode();
}

if (bmiForm) {
  bmiForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const weight = Number(bmiForm.elements.weight.value);
    const heightCm = Number(bmiForm.elements.height.value);
    const result = bmiForm.querySelector("[data-bmi-result]");
    if (!result || weight < 20 || weight > 500 || heightCm < 80 || heightCm > 250) {
      if (result) result.textContent = "Revisa los valores: peso de 20 a 500 kg y altura de 80 a 250 cm.";
      return;
    }
    const bmi = weight / ((heightCm / 100) ** 2);
    let label = "Por debajo del rango orientativo";
    if (bmi >= 30) label = "Rango elevado: busca orientación profesional";
    else if (bmi >= 25) label = "Por encima del rango orientativo";
    else if (bmi >= 18.5) label = "Dentro del rango orientativo";
    result.innerHTML = `<strong>${bmi.toFixed(1)}</strong><span>${label}</span>`;
  });
}

document.querySelectorAll("[data-bar-value]").forEach((bar) => {
  const maximum = Math.max(1, Number(bar.closest('[data-bar-max]')?.dataset.barMax || 8));
  const value = Math.min(Number(bar.dataset.barValue || 0), maximum);
  bar.style.height = `${value / maximum * 100}%`;
});
