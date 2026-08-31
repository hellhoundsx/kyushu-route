import json, math
S="/private/tmp/claude-502/-Users-ricardo-gomes-Documents-apps-Nexus/0c7e087e-eb8c-40da-bc86-9cfbdc429ed8/scratchpad/"
# Kyushu -> Kanto: every prefecture the trip's corridor passes through or near
KEEP=set(list(range(8,15))+list(range(18,31))+list(range(31,40))+list(range(40,47)))
LAT0,LAT1,LON0,LON1 = 30.60, 36.60, 129.20, 140.80
d=json.load(open(S+"japan.geojson"))
def rings(g):
    t,c=g["type"],g["coordinates"]
    return [c[0]] if t=="Polygon" else ([p[0] for p in c] if t=="MultiPolygon" else [])
def perp(p,a,b):
    (x,y),(x1,y1),(x2,y2)=p,a,b; dx,dy=x2-x1,y2-y1
    if dx==0 and dy==0: return math.hypot(x-x1,y-y1)
    t=max(0,min(1,((x-x1)*dx+(y-y1)*dy)/(dx*dx+dy*dy)))
    return math.hypot(x-(x1+t*dx), y-(y1+t*dy))
def dp(pts,tol):
    if len(pts)<3: return pts
    dmax,idx=0,0
    for i in range(1,len(pts)-1):
        dd=perp(pts[i],pts[0],pts[-1])
        if dd>dmax: dmax,idx=dd,i
    return dp(pts[:idx+1],tol)[:-1]+dp(pts[idx:],tol) if dmax>tol else [pts[0],pts[-1]]
def area(r):
    s=0
    for i in range(len(r)):
        x1,y1=r[i]; x2,y2=r[(i+1)%len(r)]; s+=x1*y2-x2*y1
    return abs(s)/2
MEAN=33.6; KX=math.cos(math.radians(MEAN)); W=1000.0
sx=W/((LON1-LON0)*KX); H=(LAT1-LAT0)*sx
def proj(lo,la): return ((lo-LON0)*KX*sx,(LAT1-la)*sx)
paths=[]
for f in d["features"]:
    if f["properties"]["id"] not in KEEP: continue
    for r in rings(f["geometry"]):
        lons=[p[0] for p in r]; lats=[p[1] for p in r]
        clon,clat=sum(lons)/len(lons),sum(lats)/len(lats)
        if not (LON0<=clon<=LON1 and LAT0<=clat<=LAT1): continue
        if area(r) < 0.006: continue                  # drop small islands at this zoom
        pts=[proj(*p) for p in r]
        simp=dp(pts,0.9)
        if len(simp)<4: continue
        paths.append("M"+"L".join(f"{x:.1f},{y:.1f}" for x,y in simp)+"Z")
meta=dict(viewBox=f"0 0 {W:.0f} {H:.0f}",lon0=LON0,lon1=LON1,lat0=LAT0,lat1=LAT1,kx=KX,sx=sx,w=W,h=H)
json.dump({"meta":meta,"path":" ".join(paths)},open(S+"japan_national.json","w"))
print("viewBox",meta["viewBox"])
print("rings",len(paths),"| path chars",sum(len(p) for p in paths))
print(f"scale {sx:.1f} px/deg = {111000/sx:.0f} m per px")
