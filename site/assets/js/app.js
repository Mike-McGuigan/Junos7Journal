async function loadJournal(){
  const res = await fetch('data/journal.json');
  const data = await res.json();
  document.querySelector('#routeGrid').innerHTML = data.route.map(stop => `<article class="stop ${stop.phase==='milestone'?'milestone':''}"><div class="stop-date">${stop.date}</div><div class="stop-name">${stop.name}</div></article>`).join('');
  document.querySelector('#timeline').innerHTML = data.entries.map(entry => `<article class="card ${entry.type==='highlight'||entry.type==='milestone'?'highlight':''}"><div class="date">${entry.date}</div><h3>${entry.title}</h3><p class="location">${entry.location}</p>${entry.quote?`<blockquote class="quote">“${entry.quote}”<br><span class="person">— ${entry.person}</span></blockquote>`:''}<p>${entry.body}</p></article>`).join('');
}
loadJournal();