
document.addEventListener('DOMContentLoaded', function () {

  // ===== Cart quantity steppers (+/-) =====
  document.querySelectorAll('.qty-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const input = btn.closest('.input-group').querySelector('.qty-input');
      const step = parseInt(btn.dataset.step, 10);
      const min = parseInt(input.min || 1, 10);
      const max = parseInt(input.max || 999, 10);
      let value = parseInt(input.value, 10) + step;
      if (value < min) value = min;
      if (value > max) value = max;
      input.value = value;
    });
  });

});

// ===== Checkout: highlight selected address card =====
document.querySelectorAll('.address-radio').forEach(function (radio) {
  radio.addEventListener('change', function () {
    document.querySelectorAll('.address-card').forEach(function (card) {
      card.classList.remove('selected');
    });
    radio.closest('.address-card').classList.add('selected');
  });
});

// Also allow clicking anywhere on the card to select the radio
document.querySelectorAll('.address-card').forEach(function (card) {
  card.addEventListener('click', function (e) {
    if (e.target.tagName !== 'INPUT') {
      const radio = card.querySelector('.address-radio');
      radio.checked = true;
      radio.dispatchEvent(new Event('change'));
    }
  });
});