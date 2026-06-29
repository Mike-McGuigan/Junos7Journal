let journalData;
async function loadJournal(){
  const res = await fetch('data/journal.json');
  journalData = await res.json();
  renderRouteCards(journalData.route);
  renderMap(journalData.route);
  renderTimeline(journalData.entries, journalData.media);
  renderGallery(journalData.media);
}
function renderRouteCards(route){
  document.querySelector('#routeGrid').innerHTML = route.map(stop => `<article class="stop ${stop.phase === 'milestone' ? 'milestone' : ''}"><div class="stop-date">${stop.date}</div><div class="stop-name">${stop.name}</div></article>`).join('');
}
function project(lat, lng, bounds, w, h){
  const x = ((lng - bounds.minLng) / (bounds.maxLng - bounds.minLng)) * (w-120) + 60;
  const y = (1 - ((lat - bounds.minLat) / (bounds.maxLat - bounds.minLat))) * (h-100) + 50;
  return [x,y];
}
function renderMap(route){
  const el = document.querySelector('#routeMap');
  const w=1100, h=520;
  const bounds = {minLat: Math.min(...route.map(r=>r.lat))-0.35,maxLat: Math.max(...route.map(r=>r.lat))+0.35,minLng: Math.min(...route.map(r=>r.lng))-0.35,maxLng: Math.max(...route.map(r=>r.lng))+0.35};
  const pts = route.map(r => ({...r, p: project(r.lat,r.lng,bounds,w,h)}));
  const path = pts.map((r,i)=>`${i?'L':'M'} ${r.p[0].toFixed(1)} ${r.p[1].toFixed(1)}`).join(' ');
  el.innerHTML = `<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="Route map"><defs><radialGradient id="seaGlow" cx="50%" cy="35%"><stop offset="0%" stop-color="#155d79"/><stop offset="100%" stop-color="#061928"/></radialGradient></defs><rect width="${w}" height="${h}" fill="url(#seaGlow)"></rect><path class="route-line" d="${path}"></path>${pts.map(r=>`<circle class="route-point ${r.phase==='milestone'?'milestone':''}" cx="${r.p[0]}" cy="${r.p[1]}" r="${r.phase==='milestone'?8:5}"></circle><text class="map-label" x="${r.p[0]+10}" y="${r.p[1]-4}">${r.name}</text><text class="map-date" x="${r.p[0]+10}" y="${r.p[1]+11}">${r.date}</text>`).join('')}</svg>`;
}
function renderTimeline(entries, media){
  const mediaById = Object.fromEntries(media.map(m=>[m.id,m]));
  document.querySelector('#timeline').innerHTML = entries.map(entry => `<article class="card ${entry.type}"><div class="date">${entry.date}</div><h3>${entry.title}</h3><p class="location">${entry.location}</p>${entry.quote ? `<blockquote class="quote">“${entry.quote}”<br><span class="person">— ${entry.person}</span></blockquote>` : ''}<p>${entry.body}</p><div class="media-grid">${(entry.media || []).map(id => renderMedia(mediaById[id])).join('')}</div></article>`).join('');
}
function renderMedia(m){
  if(!m) return '';
  if(m.type === 'video') return `<figure><video controls preload="metadata" src="${m.url}"></video><figcaption class="media-caption">${m.caption}</figcaption></figure>`;
  return `<figure><img src="${m.url}" alt="${m.title}"><figcaption class="media-caption">${m.caption}</figcaption></figure>`;
}
function renderGallery(media){
  document.querySelector('#gallery').innerHTML = media.map(m => renderMedia(m)).join('');
}
loadJournal();