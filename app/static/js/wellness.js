// One timer per routine. A deadline avoids drift when the browser throttles tabs.
document.querySelectorAll('[data-timer]').forEach((timer) => {
  const total = Number(timer.dataset.duration);
  const display = timer.querySelector('[data-timer-display]');
  const status = timer.querySelector('[data-timer-status]');
  const button = timer.querySelector('[data-timer-start]');
  let remaining = total;
  let deadline = 0;
  let interval = null;

  const render = () => {
    display.textContent = `${String(Math.floor(remaining / 60)).padStart(2, '0')}:${String(remaining % 60).padStart(2, '0')}`;
  };
  const stop = () => { clearInterval(interval); interval = null; };
  const tick = () => {
    remaining = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
    render();
    if (remaining === 0) {
      stop();
      status.textContent = 'La pausa terminó. Tómate un momento antes de continuar.';
      button.textContent = 'Volver a empezar';
    }
  };
  button.addEventListener('click', () => {
    if (interval !== null) {
      tick();
      stop();
      status.textContent = 'En pausa. Continúa cuando quieras.';
      button.textContent = 'Continuar';
      return;
    }
    if (remaining === 0) remaining = total;
    deadline = Date.now() + remaining * 1000;
    interval = setInterval(tick, 250);
    button.textContent = 'Pausar';
    status.textContent = 'La rutina está en marcha. Puedes detenerla en cualquier momento.';
    render();
  });
  timer.querySelector('[data-timer-reset]').addEventListener('click', () => {
    stop(); remaining = total; render();
    button.textContent = 'Comenzar';
    status.textContent = 'Reloj reiniciado. Empieza cuando lo decidas.';
  });
  document.addEventListener('visibilitychange', () => { if (interval !== null) tick(); });
});

document.querySelectorAll('[data-confirm-goal]').forEach((form) => {
  form.addEventListener('submit', (event) => {
    if (!window.confirm('¿Retirar esta meta? Tus hábitos ya registrados se conservan.')) event.preventDefault();
  });
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') document.querySelectorAll('.account-menu[open]').forEach((menu) => {
    menu.open = false; menu.querySelector('summary').focus();
  });
});
