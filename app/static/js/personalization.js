document.querySelectorAll('[data-routine-editor]').forEach((editor) => {
  const list = editor.querySelector('[data-exercise-list]');
  const add = editor.querySelector('[data-add-exercise]');
  const status = editor.querySelector('[data-exercise-status]');
  const renumber = () => {
    const rows = [...list.querySelectorAll('[data-exercise]')];
    rows.forEach((row, index) => {
      row.querySelector('[data-exercise-number]').textContent = index + 1;
      row.querySelectorAll('[name], [id], [for], [aria-describedby]').forEach((control) => {
        ['name', 'id', 'for', 'aria-describedby'].forEach((attribute) => {
          if (control.hasAttribute(attribute)) control.setAttribute(attribute,
            control.getAttribute(attribute).replace(/exercises-\d+-/g, `exercises-${index}-`));
        });
      });
      row.querySelector('[data-remove-exercise]').hidden = rows.length === 1;
    });
    add.disabled = rows.length >= 12;
  };
  add.addEventListener('click', (event) => {
    event.preventDefault();
    if (list.children.length >= 12) return;
    const row = list.querySelector('[data-exercise]').cloneNode(true);
    row.querySelectorAll('.field-error').forEach((error) => error.remove());
    row.querySelectorAll('.field--error').forEach((field) => field.classList.remove('field--error'));
    row.querySelectorAll('input, textarea').forEach((input) => {
      input.value = input.name.endsWith('-sets') ? '1' : input.name.endsWith('-rest_seconds') ? '30' : '';
      input.removeAttribute('aria-invalid');
    });
    row.querySelectorAll('select').forEach((select) => { select.selectedIndex = 0; });
    list.appendChild(row); renumber();
    status.textContent = `Ejercicio ${list.children.length} añadido.`;
    row.querySelector('input').focus();
  });
  list.addEventListener('click', (event) => {
    const remove = event.target.closest('[data-remove-exercise]');
    if (!remove || list.children.length <= 1) return;
    remove.closest('[data-exercise]').remove(); renumber();
    status.textContent = 'Ejercicio retirado del formulario. Guarda para confirmar los cambios.';
    add.focus();
  });
  renumber();
});
document.querySelectorAll('[data-confirm-archive]').forEach((form) => {
  form.addEventListener('submit', (event) => {
    if (!window.confirm('¿Archivar esta rutina? Tu historial y puntos se conservan.')) event.preventDefault();
  });
});

// This optional calculator has no named fields, requests, cookies or persistence.
document.querySelectorAll('[data-bmi-preview]').forEach((preview) => {
  const weightInput = preview.querySelector('[data-bmi-weight]');
  const heightInput = preview.querySelector('[data-bmi-height]');
  const result = preview.querySelector('[data-bmi-result]');
  const readNumber = (input) => {
    const value = input.value.trim();
    return /^\d+(?:[.,]\d+)?$/.test(value) ? Number(value.replace(',', '.')) : NaN;
  };
  const calculate = () => {
    const weight = readNumber(weightInput);
    const height = readNumber(heightInput);
    const bmi = weight / ((height / 100) ** 2);
    result.hidden = false;
    if (!Number.isFinite(weight) || weight < 10 || weight > 500
      || !Number.isFinite(height) || height < 50 || height > 250
      || !Number.isFinite(bmi) || bmi < 5 || bmi > 100) {
      result.textContent = 'Revisa el peso en kilogramos y la altura en centímetros.';
      return;
    }
    result.textContent = `Tu IMC es ${bmi.toLocaleString('es-CO', {
      minimumFractionDigits: 2, maximumFractionDigits: 2,
    })}. Esta consulta no se guarda en tu historial.`;
  };
  preview.querySelector('[data-bmi-calculate]').addEventListener('click', calculate);
  [weightInput, heightInput].forEach((input) => {
    input.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') { event.preventDefault(); calculate(); }
    });
    input.addEventListener('input', () => { result.hidden = true; result.textContent = ''; });
  });
  window.addEventListener('pagehide', () => {
    weightInput.value = ''; heightInput.value = '';
    result.hidden = true; result.textContent = '';
  });
});
