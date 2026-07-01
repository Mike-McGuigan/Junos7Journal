#!/usr/bin/env python3
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
import json, os, subprocess, sys, webbrowser
ROOT=Path(__file__).resolve().parents[1]; PORT=8765; VERSION="2.1.1"; RELEASE="Geographic Intelligence polish"
def run(cmd,check=True):
    p=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=False)
    if check and p.returncode!=0: raise RuntimeError(f"Command failed: {' '.join(cmd)}\n\n{p.stdout}")
    return p.stdout.strip()
def git_health():
    info={"ok":True,"version":VERSION,"release":RELEASE,"repo":ROOT.name,"root":str(ROOT),"checks":[]}
    def check(name,cmd,required=True,warning_ok=False):
        try:
            out=run(cmd,True)
            info["checks"].append({"name":name,"ok":True,"required":required,"warning":False,"output":out})
            return out
        except Exception as e:
            output=str(e)
            if warning_ok:
                info["checks"].append({"name":name,"ok":True,"required":False,"warning":True,"output":output})
            else:
                info["checks"].append({"name":name,"ok":False,"required":required,"warning":not required,"output":output})
                if required: info["ok"]=False
            return ""
    check("Git installed",["git","--version"])
    info["branch"]=check("Current branch",["git","branch","--show-current"],False) or "unknown"
    info["remote"]=check("Remote",["git","remote","-v"],False)
    status=check("Working tree",["git","status","--short"],False)
    info["workingTreeClean"]=not bool(status.strip())
    helper=check("Credential helper",["git","config","--global","credential.helper"],False,warning_ok=True)
    info["credentialHelper"]=helper or "not configured globally"
    return info
def safe_name(v): return "".join(c.lower() if c.isalnum() else "-" for c in v).strip("-") or "junos7"
def write_update(update):
    name=safe_name(update.get("routePoint",{}).get("name","junos7")); d=ROOT/"admin-input"; d.mkdir(parents=True,exist_ok=True); out=d/"latest-location.json"; arch=d/f"manual-location-{name}.json"; txt=json.dumps(update,indent=2); out.write_text(txt,encoding="utf-8"); arch.write_text(txt,encoding="utf-8"); return out
def publish(update):
    log=[]; loc=update.get("routePoint",{}).get("name","Manual location")
    if not git_health()["ok"]: raise RuntimeError("Git health check failed. Check the dashboard/server output.")
    p=write_update(update); log.append(f"Wrote {p.relative_to(ROOT)}"); log.append(run([sys.executable,"tools/apply_manual_location.py",str(p.relative_to(ROOT))])); log.append(run([sys.executable,"tools/build_site.py"]))
    status=run(["git","status","--porcelain"],False)
    if not status.strip(): log.append("No git changes detected. Nothing to commit or push."); return "\n".join(log)
    run(["git","add","."]); log.append(run(["git","commit","-m",f"Update Juno's 7 location - {loc}"])); log.append(run(["git","push"])); log.append("Published to GitHub. Check GitHub Actions for the Pages deployment."); return "\n".join(log)
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw): super().__init__(*a,directory=str(ROOT/"site"),**kw)
    def _json(self,status,payload):
        data=json.dumps(payload).encode("utf-8"); self.send_response(status); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(data))); self.send_header("Access-Control-Allow-Origin","*"); self.end_headers(); self.wfile.write(data)
    def do_OPTIONS(self): self.send_response(204); self.send_header("Access-Control-Allow-Origin","*"); self.send_header("Access-Control-Allow-Headers","Content-Type"); self.send_header("Access-Control-Allow-Methods","POST, GET, OPTIONS"); self.end_headers()
    def do_GET(self):
        if urlparse(self.path).path in {"/api/status","/api/health"}: self._json(200,git_health()); return
        super().do_GET()
    def do_POST(self):
        if urlparse(self.path).path!="/api/publish": self._json(404,{"ok":False,"error":"Not found"}); return
        try:
            n=int(self.headers.get("Content-Length","0")); update=json.loads(self.rfile.read(n).decode("utf-8"))
            if "routePoint" not in update or "tracker" not in update: raise ValueError("Invalid update payload")
            self._json(200,{"ok":True,"log":publish(update)})
        except Exception as e: self._json(500,{"ok":False,"error":str(e)})
def main():
    os.chdir(ROOT); url=f"http://localhost:{PORT}/admin.html"; print("="*72); print("Captain's Dashboard"); print("="*72); print(f"Repository: {ROOT}"); print(f"URL:        {url}\n"); print("Health check:")
    h=git_health()
    for item in h["checks"]:
        sym="OK " if item["ok"] and not item.get("warning") else ("WARN" if item.get("warning") else "ERR"); first=(item["output"] or "").splitlines()[0] if item["output"] else ""; print(f"  [{sym}] {item['name']}: {first}")
    print("\nLeave this window open while using Publish. Press Ctrl+C to stop."); print("="*72); webbrowser.open(url)
    try: ThreadingHTTPServer(("localhost",PORT),Handler).serve_forever()
    except KeyboardInterrupt: print("\\nCaptain's Dashboard stopped.")
if __name__=="__main__": main()
