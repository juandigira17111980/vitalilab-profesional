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
