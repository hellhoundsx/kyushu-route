import json
S="/private/tmp/claude-502/-Users-ricardo-gomes-Documents-apps-Nexus/0c7e087e-eb8c-40da-bc86-9cfbdc429ed8/scratchpad/"
svg,labels=open(S+"map.frag.html").read().split("\n<!--LABELS-->\n")
pl=json.load(open(S+"places.final.json"))
slim=[{k:p[k] for k in ("kind","label","note","when","leg","status","sclass","day","l","t","gmap")} for p in pl]
out=(open(S+"page.tpl.html").read()
     .replace("@@MAP@@",svg)
     .replace("@@LABELS@@",labels)
     .replace("@@PLACES@@",json.dumps(slim,ensure_ascii=False)))
pics=json.load(open(S+"pics.json"))
PIC={r["label"]:{"b":r["b64"],"c":"%s / %s, Wikimedia Commons"%(r["author"] or "unknown", r["lic"])} for r in pics}
out=out.replace("@@PICS@@", json.dumps(PIC, ensure_ascii=False))
seen=[]
for r in pics:
    t="%s (%s)"%(r["author"] or "unknown", r["lic"])
    if t not in seen: seen.append(t)
out=out.replace("@@CREDITS@@", "; ".join(seen))
nsvg,nlab=open(S+"national.frag.html").read().split("\n<!--NLABELS-->\n")
out=out.replace("@@NATIONAL@@", nsvg+"\n"+nlab)
def ascii_esc(t):
    return "".join(c if ord(c)<128 else "&#%d;"%ord(c) for c in t)
out=ascii_esc(out)
open(S+"kyushu-route.html","w",encoding="ascii").write(out)
print("written",len(out),"chars")
for tok in ("@@MAP@@","@@LABELS@@","@@PLACES@@"):
    assert tok not in out, tok
print("no placeholders left")
