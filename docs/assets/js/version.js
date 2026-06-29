async function loadVersionInfo() {
  try {
    const res = await fetch('data/version.json?cache=' + Date.now());
    const info = await res.json();

    const badge = document.createElement('div');
    badge.className = 'version-badge';
    badge.innerHTML = `<strong>v${info.version}</strong> · ${info.release}`;
    document.body.appendChild(badge);

    const footer = document.querySelector('.footer');
    if (footer) {
      const p = document.createElement('p');
      p.className = 'version-footer';
      p.textContent = `Version ${info.version} · ${info.release} · Built ${info.buildUtc}`;
      footer.appendChild(p);
    }
  } catch (err) {
    console.warn('Version metadata could not be loaded', err);
  }
}
loadVersionInfo();
