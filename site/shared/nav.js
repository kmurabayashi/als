// 「過去イベント」プルダウン(<details class="dropdown">)を、外側クリック・Esc キーで閉じる
document.addEventListener('click', (e) => {
  document.querySelectorAll('details.dropdown[open]').forEach((d) => {
    if (!d.contains(e.target)) d.removeAttribute('open');
  });
});
document.addEventListener('keydown', (e) => {
  if (e.key !== 'Escape') return;
  document.querySelectorAll('details.dropdown[open]').forEach((d) => {
    d.removeAttribute('open');
    d.querySelector('summary')?.focus();
  });
});

// メールアドレスの組み立て(収集対策)。data-mail-u / data-mail-d に逆順で書いたものを戻す
document.querySelectorAll('[data-mail-u][data-mail-d]').forEach((el) => {
  const rev = (s) => s.split('').reverse().join('');
  const addr = rev(el.dataset.mailU) + '@' + rev(el.dataset.mailD);
  if (el.tagName === 'A') {
    const subject = el.dataset.mailSubject;
    el.href = 'mailto:' + addr + (subject ? '?subject=' + encodeURIComponent(subject) : '');
  } else {
    el.textContent = addr;
  }
});
