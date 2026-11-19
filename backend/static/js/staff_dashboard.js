/**
 * Скрипты АРМ Администратора клуба «Strike & Pocket»
 * Вариант 4 (FR-15, FR-16)
 */

document.addEventListener('DOMContentLoaded', function () {
  const audioToggle = document.getElementById('audioToggle');
  let audioEnabled = true;

  if (audioToggle) {
    audioToggle.addEventListener('click', function () {
      audioEnabled = !audioEnabled;
      this.classList.toggle('btn-cyan', audioEnabled);
      this.classList.toggle('btn-outline-secondary', !audioEnabled);
      this.innerHTML = audioEnabled 
        ? '<i class="fa-solid fa-volume-high me-1"></i> Звук вкл' 
        : '<i class="fa-solid fa-volume-xmark me-1"></i> Звук выкл';
    });
  }

  // Звуковой сигнал веб-аудио при появлении новых заказов (FR-16)
  function playAlertBeep() {
    if (!audioEnabled) return;
    try {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(880, ctx.currentTime); // нота Ля
      osc.frequency.exponentialRampToValueAtTime(1760, ctx.currentTime + 0.15);

      gain.gain.setValueAtTime(0.3, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.25);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start();
      osc.stop(ctx.currentTime + 0.25);
    } catch (e) {
      console.log("AudioContext blocked by browser policy");
    }
  }

  // Модальное окно смены статуса
  window.openStatusModal = function (bookingId, bookingNumber, currentStatus) {
    document.getElementById('modalBookingId').value = bookingId;
    document.getElementById('modalBookingNumber').innerText = '#' + bookingNumber;
    document.getElementById('modalStatusSelect').value = currentStatus;
    document.getElementById('statusChangeForm').action = `/staff/booking/${bookingId}/status/`;

    const modal = new bootstrap.Modal(document.getElementById('statusModal'));
    modal.show();
  };
});
