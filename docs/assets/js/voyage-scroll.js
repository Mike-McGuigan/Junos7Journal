function centerVoyageStopTile(button){
  if(!button) return;
  button.scrollIntoView({block:'nearest', inline:'center', behavior:'smooth'});
}

function centerVoyageStopTileFromClick(ev){
  const button = ev.target.closest('#mapTimeline .map-stop');
  if(!button) return;
  // Let the existing dashboard click handler finish, then center the tile.
  setTimeout(() => centerVoyageStopTile(button), 0);
}

document.addEventListener('click', centerVoyageStopTileFromClick, true);

function centerSelectedVoyageStopTile(){
  const current = document.querySelector('#mapTimeline .map-stop[aria-current="true"]');
  if(!current) return false;
  centerVoyageStopTile(current);
  return true;
}

function centerVoyageStopTileFromMapClick(ev){
  const target = ev.target;
  const mapPoint = target?.closest?.('#voyageMap .leaflet-interactive, #voyageMap .leaflet-marker-icon');
  if(!mapPoint) return;
  setTimeout(() => centerSelectedVoyageStopTile(), 0);
}

document.addEventListener('click', centerVoyageStopTileFromMapClick, true);

function requestedVoyageStop(){
  const requestedStop = new URLSearchParams(location.search).get('stop');
  return requestedStop ? requestedStop.trim().toLowerCase() : '';
}

function findRequestedVoyageStopButton(timeline){
  const requested = requestedVoyageStop();
  if(!requested || !timeline) return null;
  return [...timeline.querySelectorAll('.map-stop')].find(el => {
    const label = el.querySelector('strong')?.textContent || '';
    const date = el.querySelector('.map-stop-date')?.textContent || '';
    return [label, date, el.textContent || '']
      .some(text => text.trim().toLowerCase().includes(requested));
  }) || null;
}

function centerRequestedVoyageStopTile(){
  const timeline = document.querySelector('#mapTimeline');
  const match = findRequestedVoyageStopButton(timeline);
  if(match){
    centerVoyageStopTile(match);
    return true;
  }
  return false;
}

function waitForRequestedVoyageStopTile(){
  if(!requestedVoyageStop()) return;
  if(centerRequestedVoyageStopTile()) return;

  const timeline = document.querySelector('#mapTimeline');
  if(!timeline){
    requestAnimationFrame(waitForRequestedVoyageStopTile);
    return;
  }

  const observer = new MutationObserver(() => {
    if(centerRequestedVoyageStopTile()) observer.disconnect();
  });
  observer.observe(timeline, {childList: true, subtree: true});

  let attempts = 0;
  const poll = () => {
    if(centerRequestedVoyageStopTile() || attempts++ > 30){
      observer.disconnect();
      return;
    }
    requestAnimationFrame(poll);
  };
  requestAnimationFrame(poll);
}

if(document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', waitForRequestedVoyageStopTile, {once: true});
} else {
  waitForRequestedVoyageStopTile();
}
