// Auto-dismiss flash messages
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity .5s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 500);
    }, 4000);
  });

  // Wishlist toggle (UI only)
  document.querySelectorAll('.pcard-wish').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.textContent = btn.textContent === '♡' ? '♥' : '♡';
      btn.style.color = btn.textContent === '♥' ? '#EF4444' : '';
    });
  });
});
