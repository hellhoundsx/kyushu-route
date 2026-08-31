import json, math

SCRATCH = "/private/tmp/claude-502/-Users-ricardo-gomes-Documents-apps-Nexus/0c7e087e-eb8c-40da-bc86-9cfbdc429ed8/scratchpad/"
KYUSHU = {40:"Fukuoka",41:"Saga",42:"Nagasaki",43:"Kumamoto",44:"Oita",45:"Miyazaki",46:"Kagoshima"}

# clip box: mainland Kyushu only (drops Tsushima, Iki, Goto, Amami, Tokara)
LAT0, LAT1 = 30.90, 34.05
LON0, LON1 = 129.55, 132.25

d = json.load(open(SCRATCH+"japan.geojson"))

def rings(geom):
    t, c = geom["type"], geom["coordinates"]
    if t == "Polygon":   return [c[0]]
    if t == "MultiPolygon": return [p[0] for p in c]
    return []

def perp(pt, a, b):
    (x,y),(x1,y1),(x2,y2) = pt,a,b
    dx,dy = x2-x1, y2-y1
    if dx==0 and dy==0: return math.hypot(x-x1,y-y1)
    t = max(0,min(1,((x-x1)*dx+(y-y1)*dy)/(dx*dx+dy*dy)))
    return math.hypot(x-(x1+t*dx), y-(y1+t*dy))

def dp(pts, tol):
    if len(pts) < 3: return pts
    dmax, idx = 0, 0
    for i in range(1,len(pts)-1):
        dd = perp(pts[i], pts[0], pts[-1])
        if dd > dmax: dmax, idx = dd, i
    if dmax > tol:
        return dp(pts[:idx+1],tol)[:-1] + dp(pts[idx:],tol)
    return [pts[0], pts[-1]]

def ring_area(r):
    s = 0
    for i in range(len(r)):
        x1,y1 = r[i]; x2,y2 = r[(i+1)%len(r)]
        s += x1*y2 - x2*y1
    return abs(s)/2

# ---- projection: equirectangular, x compressed by cos(mean lat) ----
MEANLAT = 32.5
KX = math.cos(math.radians(MEANLAT))
W = 1000.0
sx = W / ((LON1-LON0)*KX)
H = (LAT1-LAT0)*sx

def proj(lon, lat):
    return ((lon-LON0)*KX*sx, (LAT1-lat)*sx)

out = {}
for f in d["features"]:
    pid = f["properties"]["id"]
    if pid not in KYUSHU: continue
    paths = []
    for r in rings(f["geometry"]):
        lons = [p[0] for p in r]; lats = [p[1] for p in r]
        clon, clat = sum(lons)/len(lons), sum(lats)/len(lats)
        if not (LON0<=clon<=LON1 and LAT0<=clat<=LAT1): continue
        if ring_area(r) < 0.0004: continue           # drop specks
        pts = [proj(*p) for p in r]
        simp = dp(pts, 0.55)                          # px tolerance
        if len(simp) < 4: continue
        paths.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x,y in simp) + "Z")
    if paths:
        out[KYUSHU[pid]] = " ".join(paths)

meta = {"viewBox": f"0 0 {W:.0f} {H:.0f}", "lon0":LON0,"lon1":LON1,"lat0":LAT0,"lat1":LAT1,
        "kx":KX,"sx":sx,"w":W,"h":H}
json.dump({"meta":meta,"prefs":out}, open(SCRATCH+"kyushu.json","w"))

print("viewBox", meta["viewBox"])
for k,v in out.items(): print(f"  {k:10s} {len(v):6d} chars  {v.count('M')} rings")
print("total path chars", sum(len(v) for v in out.values()))
