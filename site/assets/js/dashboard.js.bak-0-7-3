async function loadJson(path) {
  const res = await fetch(path + '?cache=' + Date.now());
  if (!res.ok) throw new Error(`Could not load ${path}`);
  return await res.json();
}
function formatValue(value, fallback = 'Not configured') {
  return value === null || value === undefined || value === '' ? fallback : value;
}
function formatCoords(pos) {
  if (!pos || pos.lat === undefined || pos.lng === undefined) return 'No precise live coordinate';
  return `${Number(pos.lat).toFixed(5)}, ${Number(pos.lng).toFixed(5)}`;
}
async function initDashboard() {
  const dashboard = await loadJson('data/dashboard.json');
  const route = await loadJson('data/route.json');
  const metrics = document.querySelector('#dashboardMetrics');
  const latestPos = dashboard.tracker.latestPrecisePosition;
  if (metrics) {
    metrics.innerHTML = `
      <article class="metric-card"><div class="label">Version</div><div class="value">${dashboard.version}</div><div class="sub">${dashboard.release}</div></article>
      <article class="metric-card"><div class="label">Tracker</div><div class="value">${dashboard.tracker.workflow}</div><div class="sub">${dashboard.tracker.provider}</div></article>
      <article class="metric-card"><div class="label">Latest AIS Summary</div><div class="value">${dashboard.tracker.liveAis ? 'Live AIS' : 'Manual'}</div><div class="sub">${dashboard.tracker.latestStatus}</div></article>
      <article class="metric-card"><div class="label">Latest Position</div><div class="value" style="font-size:1.15rem">${formatCoords(latestPos)}</div><div class="sub">${latestPos ? latestPos.reportedUtc : 'Not available'}</div></article>
      <article class="metric-card"><div class="label">Route Stops</div><div class="value">${dashboard.stats.routeStops}</div><div class="sub">voyage so far</div></article>
      <article class="metric-card"><div class="label">Media</div><div class="value">${dashboard.stats.mediaItems}</div><div class="sub">${dashboard.stats.photos} photos · ${dashboard.stats.videos} videos</div></article>`;
  }
  initVoyageMap(route);
}
function initVoyageMap(route) {
  const mapEl = document.querySelector('#voyageMap');
  if (!mapEl || typeof L === 'undefined') return;
  const map = L.map('voyageMap', {scrollWheelZoom: false});
  const street = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom:19, attribution:'&copy; OpenStreetMap contributors'});
  const satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {maxZoom:19, attribution:'Tiles &copy; Esri'});
  satellite.addTo(map);
  L.control.layers({'Satellite': satellite, 'Map': street}).addTo(map);
  const latlngs = route.map(stop => [stop.lat, stop.lng]);
  const completedLine = L.polyline(latlngs, {color:'#9ed4ff', weight:4, opacity:0.95}).addTo(map);
  route.forEach((stop, index) => {
    const isCurrent = stop.phase === 'current';
    const isMilestone = stop.phase === 'milestone';
    const marker = L.circleMarker([stop.lat, stop.lng], {
      radius: isCurrent ? 11 : isMilestone ? 9 : 7,
      color: isCurrent ? '#ff8a2a' : isMilestone ? '#c9a45c' : '#9ed4ff',
      fillColor: isCurrent ? '#ff8a2a' : isMilestone ? '#c9a45c' : '#0f6f91',
      fillOpacity:0.95,
      weight:2
    }).addTo(map);
    marker.bindPopup(`<strong>${index + 1}. ${stop.name}</strong><br>${stop.date}<br><span class="status-pill">${stop.phase}</span>${stop.note ? `<p>${stop.note}</p>` : ''}`);
  });
  map.fitBounds(completedLine.getBounds(), {padding: [35,35]});
  const timeline = document.querySelector('#mapTimeline');
  if (timeline) {
    timeline.innerHTML = route.map((stop, index) => `<button class="map-stop ${stop.phase === 'milestone' ? 'milestone' : ''} ${stop.phase === 'current' ? 'current' : ''}" data-index="${index}"><div class="map-stop-date">${stop.date}</div><strong>${index + 1}. ${stop.name}</strong></button>`).join('');
    timeline.querySelectorAll('.map-stop').forEach(btn => {
      btn.addEventListener('click', () => {
        const stop = route[Number(btn.dataset.index)];
        map.flyTo([stop.lat, stop.lng], 10, {duration: 0.8});
      });
    });
  }
}
initDashboard().catch(err => console.error(err));