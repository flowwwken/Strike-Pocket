/**
 * Клиентская валидация форм и динамическая логика веб-сервиса «Strike & Pocket».
 * Занятие 9. Проверка обязательных полей, формата почты и телефона, длины текста до отправки.
 * Реализация специального бизнес-правила Варианта 4 (лимит 6 игроков на дорожку боулинга).
 * Студент: Верин Вадим Сергеевич, группа ИСдо-45.
 */

document.addEventListener('DOMContentLoaded', function () {
  const wizardForm = document.getElementById('bookingWizardForm');
  if (!wizardForm) return;

  const lastNameInput = document.getElementById('id_last_name');
  const firstNameInput = document.getElementById('id_first_name');
  const phoneInput = document.getElementById('id_phone');
  const emailInput = document.getElementById('id_email');
  const dateInput = document.getElementById('dateInput');
  const startTimeInput = document.getElementById('startTimeInput');
  const endTimeInput = document.getElementById('endTimeInput');
  const playersInput = document.getElementById('playersInput');
  const resourceSelect = document.getElementById('resourceSelect');
  const submitBtn = document.getElementById('submitBookingBtn');

  // Регулярные выражения
  const emailRegex = /^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}$/;
  const phoneDigitsRegex = /\d/g;

  // Хелпер: установка ошибки
  function setError(input, errorSpanId, message) {
    if (!input) return;
    input.classList.add('is-invalid');
    input.classList.remove('is-valid');
    const span = document.getElementById(errorSpanId);
    if (span) {
      span.textContent = message;
      span.classList.remove('d-none');
    }
  }

  // Хелпер: очистка ошибки
  function clearError(input, errorSpanId) {
    if (!input) return;
    input.classList.remove('is-invalid');
    input.classList.add('is-valid');
    const span = document.getElementById(errorSpanId);
    if (span) {
      span.textContent = '';
      span.classList.add('d-none');
    }
  }

  // Маска ввода телефона (+7 (XXX) XXX-XX-XX)
  if (phoneInput) {
    phoneInput.addEventListener('input', function (e) {
      let inputVal = e.target.value.replace(/\D/g, '');
      if (inputVal.startsWith('7') || inputVal.startsWith('8')) {
        inputVal = inputVal.substring(1);
      }
      let formatted = '+7 ';
      if (inputVal.length > 0) {
        formatted += '(' + inputVal.substring(0, 3);
      }
      if (inputVal.length >= 3) {
        formatted += ') ' + inputVal.substring(3, 6);
      }
      if (inputVal.length >= 6) {
        formatted += '-' + inputVal.substring(6, 8);
      }
      if (inputVal.length >= 8) {
        formatted += '-' + inputVal.substring(8, 10);
      }
      e.target.value = formatted;
      validatePhone();
    });
  }

  // Валидация фамилии (не менее 2 символов)
  function validateLastName() {
    if (!lastNameInput) return true;
    const val = lastNameInput.value.trim();
    if (!val) {
      setError(lastNameInput, 'error-last_name', 'Пожалуйста, введите фамилию гостя.');
      return false;
    }
    if (val.length < 2) {
      setError(lastNameInput, 'error-last_name', 'Фамилия должна содержать не менее 2 букв.');
      return false;
    }
    clearError(lastNameInput, 'error-last_name');
    return true;
  }

  // Валидация имени (не менее 2 символов)
  function validateFirstName() {
    if (!firstNameInput) return true;
    const val = firstNameInput.value.trim();
    if (!val) {
      setError(firstNameInput, 'error-first_name', 'Пожалуйста, введите имя гостя.');
      return false;
    }
    if (val.length < 2) {
      setError(firstNameInput, 'error-first_name', 'Имя должно содержать не менее 2 букв.');
      return false;
    }
    clearError(firstNameInput, 'error-first_name');
    return true;
  }

  // Валидация телефона (11 цифр)
  function validatePhone() {
    if (!phoneInput) return true;
    const digits = phoneInput.value.match(phoneDigitsRegex) || [];
    if (digits.length === 0) {
      setError(phoneInput, 'error-phone', 'Укажите контактный телефон.');
      return false;
    }
    if (digits.length < 11) {
      setError(phoneInput, 'error-phone', 'Номер телефона должен содержать 11 цифр (+7 (9XX) XXX-XX-XX).');
      return false;
    }
    clearError(phoneInput, 'error-phone');
    return true;
  }

  // Валидация e-mail
  function validateEmail() {
    if (!emailInput) return true;
    const val = emailInput.value.trim();
    if (!val) {
      setError(emailInput, 'error-email', 'Укажите e-mail для отправки электронного кассового чека (54-ФЗ).');
      return false;
    }
    if (!emailRegex.test(val)) {
      setError(emailInput, 'error-email', 'Введите корректный адрес электронной почты (например: user@mail.ru).');
      return false;
    }
    clearError(emailInput, 'error-email');
    return true;
  }

  // Валидация даты бронирования
  function validateDate() {
    if (!dateInput) return true;
    const val = dateInput.value;
    if (!val) {
      setError(dateInput, 'error-booking_date', 'Укажите дату сеанса.');
      return false;
    }
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const selected = new Date(val);
    if (selected < today) {
      setError(dateInput, 'error-booking_date', 'Нельзя оформить бронирование на прошедшую дату.');
      return false;
    }
    clearError(dateInput, 'error-booking_date');
    return true;
  }

  // Валидация времени начала и окончания
  function validateTime() {
    if (!startTimeInput || !endTimeInput) return true;
    const startVal = startTimeInput.value;
    const endVal = endTimeInput.value;
    const startHour = parseInt(startVal.split(':')[0], 10);
    let endHour = parseInt(endVal.split(':')[0], 10);
    if (endHour === 0) endHour = 24;

    if (endHour <= startHour) {
      setError(endTimeInput, 'error-time_end', 'Время окончания игры должно быть позже времени начала.');
      return false;
    }
    clearError(endTimeInput, 'error-time_end');
    return true;
  }

  // Специальное требование Варианта 4: лимит 6 игроков на дорожку боулинга
  function validateCapacitySpecialRequirement() {
    if (!resourceSelect || !playersInput) return true;
    const opt = resourceSelect.options[resourceSelect.selectedIndex];
    if (!opt) return true;

    const categoryCode = opt.dataset.category;
    const players = parseInt(playersInput.value, 10) || 1;

    if (categoryCode === 'BOWLING' && players > 6) {
      setError(
        playersInput,
        'error-players_count',
        `На одну дорожку боулинга допускается компания не более 6 человек (указано: ${players} чел.). При превышении числа гостей система требует добавить в бронь вторую дорожку.`
      );
      return false;
    }
    clearError(playersInput, 'error-players_count');
    return true;
  }

  // Слушатели событий blur / input для мгновенной обратной связи
  if (lastNameInput) lastNameInput.addEventListener('blur', validateLastName);
  if (firstNameInput) firstNameInput.addEventListener('blur', validateFirstName);
  if (phoneInput) phoneInput.addEventListener('blur', validatePhone);
  if (emailInput) emailInput.addEventListener('blur', validateEmail);
  if (dateInput) dateInput.addEventListener('change', validateDate);
  if (startTimeInput) startTimeInput.addEventListener('change', () => { validateTime(); });
  if (endTimeInput) endTimeInput.addEventListener('change', () => { validateTime(); });
  if (playersInput) playersInput.addEventListener('input', validateCapacitySpecialRequirement);
  if (resourceSelect) resourceSelect.addEventListener('change', validateCapacitySpecialRequirement);

  // Перехват отправки формы
  wizardForm.addEventListener('submit', function (e) {
    const isLastNameValid = validateLastName();
    const isFirstNameValid = validateFirstName();
    const isPhoneValid = validatePhone();
    const isEmailValid = validateEmail();
    const isDateValid = validateDate();
    const isTimeValid = validateTime();
    const isCapacityValid = validateCapacitySpecialRequirement();

    const isFormValid = isLastNameValid && isFirstNameValid && isPhoneValid &&
                        isEmailValid && isDateValid && isTimeValid && isCapacityValid;

    if (!isFormValid) {
      e.preventDefault();
      e.stopPropagation();

      // Плавный скролл к первому полю с ошибкой
      const firstInvalid = wizardForm.querySelector('.is-invalid');
      if (firstInvalid) {
        firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
        firstInvalid.focus();
      }
      return false;
    }

    // Если форма валидна — показываем индикатор загрузки и блокируем повторную отправку
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        Оформление бронирования и создание чека...
      `;
    }
  });
});
