/**
 * Интерактивный мастер бронирования «Strike & Pocket»
 * Вариант 4 (FR-03, FR-05, FR-06, FR-07, FR-08, FR-10, FR-17)
 */

document.addEventListener('DOMContentLoaded', function () {
  const resourceSelect = document.getElementById('resourceSelect');
  const dateInput = document.getElementById('dateInput');
  const startTimeInput = document.getElementById('startTimeInput');
  const endTimeInput = document.getElementById('endTimeInput');
  const playersInput = document.getElementById('playersInput');
  const cardInput = document.getElementById('cardInput');
  const applyCardBtn = document.getElementById('applyCardBtn');
  const cardStatus = document.getElementById('cardStatus');

  const capacityAlert = document.getElementById('capacityAlert');
  const priceBreakdown = document.getElementById('priceBreakdown');
  const barItemsJson = document.getElementById('barItemsJson');

  let appliedCardNumber = '';
  let selectedBarItems = {}; // { itemId: { name, price, qty } }

  // 1. Обработка контроля вместимости (FR-05)
  function checkCapacity() {
    const opt = resourceSelect.options[resourceSelect.selectedIndex];
    if (!opt) return;

    const categoryCode = opt.dataset.category;
    const players = parseInt(playersInput.value) || 1;

    if (categoryCode === 'BOWLING' && players > 6) {
      capacityAlert.classList.remove('d-none');
      capacityAlert.innerHTML = `
        <div class="alert alert-warning mb-0 border-0 p-3">
          <i class="fa-solid fa-triangle-exclamation me-2 fs-5"></i>
          <strong>Внимание (FR-05):</strong> На одну дорожку боулинга допускается до 6 игроков. 
          Для вашей компании из <strong>${players} чел.</strong> рекомендуется забронировать <strong>2 соседние дорожки</strong>.
        </div>
      `;
    } else if ((categoryCode === 'RUSSIAN_BILLIARD' || categoryCode === 'AMERICAN_POOL' || categoryCode === 'SNOOKER') && players > 4) {
      capacityAlert.classList.remove('d-none');
      capacityAlert.innerHTML = `
        <div class="alert alert-warning mb-0 border-0 p-3">
          <i class="fa-solid fa-triangle-exclamation me-2 fs-5"></i>
          <strong>Внимание:</strong> На один бильярдный стол допускается до 4 игроков.
        </div>
      `;
    } else {
      capacityAlert.classList.add('d-none');
    }
  }

  // 2. Динамический пересчет стоимости через API (FR-06, FR-07)
  async function updatePriceCalculation() {
    const resourceId = resourceSelect.value;
    const dateVal = dateInput.value;
    const startTime = startTimeInput.value;
    const endTime = endTimeInput.value;

    if (!resourceId || !dateVal || !startTime || !endTime) {
      return;
    }

    // Индикатор загрузки при асинхронном запросе через fetch (требование 4* Занятия 9)
    priceBreakdown.innerHTML = `
      <div class="text-center py-3 text-muted">
        <span class="spinner-border spinner-border-sm text-cyan me-2" role="status" aria-hidden="true"></span>
        <span>Идет расчет сметы по тарифам клуба...</span>
      </div>
    `;

    try {
      const url = `/api/calculate-price/?resource_id=${resourceId}&date=${dateVal}&time_start=${startTime}&time_end=${endTime}&club_card=${appliedCardNumber}`;
      const response = await fetch(url);
      const data = await response.json();

      if (data.status === 'success') {
        renderPriceBreakdown(data);
      } else {
        priceBreakdown.innerHTML = `<div class="text-danger small py-2"><i class="fa-solid fa-circle-exclamation me-1"></i>${data.error}</div>`;
      }
    } catch (e) {
      console.error("Ошибка запроса расчета цены:", e);
      priceBreakdown.innerHTML = `<div class="text-danger small py-2">Сбой связи с сервером при расчете. Попробуйте обновить страницу.</div>`;
    }
  }

  // 3. Отрисовка детализации сметы
  function renderPriceBreakdown(data) {
    let barTotal = 0;
    for (let id in selectedBarItems) {
      barTotal += selectedBarItems[id].price * selectedBarItems[id].qty;
    }

    // Учет скидки по карте на бар
    let barDiscount = 0;
    if (data.discount_percent > 0) {
      barDiscount = barTotal * (data.discount_percent / 100);
    }
    const finalBarTotal = barTotal - barDiscount;
    const grandTotal = data.total_cost + finalBarTotal;
    const depositTotal = (grandTotal * 0.5).toFixed(2);

    let html = `
      <div class="price-split-row">
        <span>День недели:</span>
        <strong class="text-light">${data.day_type_display}</strong>
      </div>
      <div class="price-split-row">
        <span>Общее время аренды:</span>
        <strong class="text-light">${data.total_hours} ч.</strong>
      </div>
    `;

    if (data.day_hours > 0) {
      html += `
        <div class="price-split-row">
          <span>Дневные часы (до 18:00):</span>
          <span>${data.day_hours} ч. &times; ${data.day_rate} ₽ = <strong class="text-cyan">${data.day_cost} ₽</strong></span>
        </div>
      `;
    }

    if (data.evening_hours > 0) {
      html += `
        <div class="price-split-row">
          <span>Вечерние часы (после 18:00):</span>
          <span>${data.evening_hours} ч. &times; ${data.evening_rate} ₽ = <strong class="text-amber">${data.evening_cost} ₽</strong></span>
        </div>
      `;
    }

    html += `
      <div class="price-split-row">
        <span>Базовая аренда:</span>
        <span class="fw-bold">${data.rental_cost} ₽</span>
      </div>
    `;

    if (data.discount_percent > 0) {
      html += `
        <div class="price-split-row text-success">
          <span>Скидка по карте (${data.card_tier_display}):</span>
          <strong>-${data.discount_amount} ₽ (${data.discount_percent}%)</strong>
        </div>
      `;
    }

    if (finalBarTotal > 0) {
      html += `
        <div class="price-split-row text-warning">
          <span>Предзаказ кухни и бара:</span>
          <strong>+${finalBarTotal.toFixed(2)} ₽</strong>
        </div>
      `;
    }

    html += `
      <div class="price-split-row border-0 pt-2 fs-5">
        <span class="text-light fw-bold">Итоговая сумма:</span>
        <strong class="text-cyan">${grandTotal.toFixed(2)} ₽</strong>
      </div>
      <div class="price-split-row border-0 text-amber fs-6">
        <span>Обязательный депозит 50%:</span>
        <strong>${depositTotal} ₽</strong>
      </div>
    `;

    priceBreakdown.innerHTML = html;
  }

  // 4. Проверка клубной карты через API (FR-17)
  if (applyCardBtn) {
    applyCardBtn.addEventListener('click', async function () {
      const cardVal = cardInput.value.trim();
      if (!cardVal) {
        cardStatus.innerHTML = '<span class="text-warning small">Введите номер карты</span>';
        return;
      }

      try {
        const response = await fetch(`/api/check-card/?card_number=${encodeURIComponent(cardVal)}`);
        const data = await response.json();

        if (data.valid) {
          appliedCardNumber = data.card_number;
          cardStatus.innerHTML = `
            <span class="text-success small">
              <i class="fa-solid fa-check me-1"></i> Карта активна: ${data.card_tier_display} (скидка ${data.discount_percent}%), владелец: ${data.client_name}
            </span>
          `;
          updatePriceCalculation();
        } else {
          appliedCardNumber = '';
          cardStatus.innerHTML = `<span class="text-danger small"><i class="fa-solid fa-xmark me-1"></i> ${data.message}</span>`;
          updatePriceCalculation();
        }
      } catch (e) {
        cardStatus.innerHTML = '<span class="text-danger small">Ошибка проверки карты</span>';
      }
    });
  }

  // 5. Управление предзаказом бара (+/- порции)
  window.changeBarQty = function (itemId, delta, name, price) {
    if (!selectedBarItems[itemId]) {
      selectedBarItems[itemId] = { itemId: itemId, name: name, price: parseFloat(price), qty: 0 };
    }

    selectedBarItems[itemId].qty += delta;
    if (selectedBarItems[itemId].qty <= 0) {
      delete selectedBarItems[itemId];
    }

    const countElem = document.getElementById(`barQty_${itemId}`);
    if (countElem) {
      countElem.innerText = selectedBarItems[itemId] ? selectedBarItems[itemId].qty : 0;
    }

    // Обновляем скрытый JSON
    const barList = Object.values(selectedBarItems).map(item => ({
      item_id: item.itemId,
      quantity: item.qty
    }));
    barItemsJson.value = JSON.stringify(barList);

    updatePriceCalculation();
  };

  // Слушатели событий формы
  resourceSelect.addEventListener('change', () => { checkCapacity(); updatePriceCalculation(); });
  dateInput.addEventListener('change', updatePriceCalculation);
  startTimeInput.addEventListener('change', updatePriceCalculation);
  endTimeInput.addEventListener('change', updatePriceCalculation);
  playersInput.addEventListener('input', () => { checkCapacity(); });

  // Первоначальный вызов
  checkCapacity();
  updatePriceCalculation();
});
