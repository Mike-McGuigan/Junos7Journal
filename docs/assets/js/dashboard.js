async function loadJson(path) {
  const res = await fetch(path + '?cache=' + Date.now());
  if (!res.ok) throw new Error(`Could not load ${path}`);
  return await res.json();
}
function formatValue(value, fallback = 'Not configured') {
  return value === null || value === undefined || value === '' ? fallback : value;
}
async function initDashboard() {
  const dashboard = await loadJson('data/dashboard.json');
  const route = await loadJson('data/route.json');
  const metrics = document.querySelector('#dashboardMetrics');
  if (metrics) {
    metrics.innerHTML = `
      <article class="metric-card"><div class="label">Version</div><div class="value">${dashboard.version}</div><div class="sub">${dashboard.release}</div></article>
      <article class="metric-card"><div class="label">Tracker</div><div class="value">${dashboard.tracker.workflow}</div><div class="sub">${dashboard.tracker.provider}</div></article>
      <article class="metric-card"><div class="label">Latest Status</div><div class="value">${dashboard.tracker.liveAis ? 'Live AIS' : 'Manual'}</div><div class="sub">${dashboard.tracker.latestStatus}</div></article>
      <article class="metric-card"><div class="label">Speed</div><div class="value">${formatValue(dashboard.tracker.latestSpeedKnots)} kn</div><div class="sub">latest manual lookup</div></article>
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
    const marker = L.circleMarker([stop.lat, stop.lng], {radius: stop.phase === 'milestone' ? 9 : 7, color: stop.phase === 'milestone' ? '#c9a45c' : '#9ed4ff', fillColor: stop.phase === 'milestone' ? '#c9a45c' : '#0f6f91', fillOpacity:0.95, weight:2}).addTo(map);
    marker.bindPopup(`<strong>${index + 1}. ${stop.name}</strong><br>${stop.date}<br><span class="status-pill">${stop.phase}</span>`);
  });
  map.fitBounds(completedLine.getBounds(), {padding: [35,35]});
  const timeline = document.querySelector('#mapTimeline');
  if (timeline) {
    timeline.innerHTML = route.map((stop, index) => `<button class="map-stop ${stop.phase === 'milestone' ? 'milestone' : ''}" data-index="${index}"><div class="map-stop-date">${stop.date}</div><strong>${index + 1}. ${stop.name}</strong></button>`).join('');
    timeline.querySelectorAll('.map-stop').forEach(btn => {
      btn.addEventListener('click', () => {
        const stop = route[Number(btn.dataset.index)];
        map.flyTo([stop.lat, stop.lng], 10, {duration: 0.8});
      });
    });
  }
}
initDashboard().catch(err => console.error(err));