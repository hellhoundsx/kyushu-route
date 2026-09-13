# -*- coding: utf-8 -*-
"""Kyoto ward map + the Osaka-Nara-Kyoto triangle -> src/kyoto.frag.html

Real boundaries for the eleven wards of Kyoto city, from
src/kyoto_wards.geojson (MLIT N03 administrative boundaries), simplified and
projected to scale -- the same treatment the Osaka map gets. Longitude is
scaled by the cosine of the mean latitude so the result is not stretched.

Temples, shrines and stations sit at their real coordinates on top.
"""
import json, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT/"src"; SRC.mkdir(exist_ok=True)

# ------------------------------------------------------------------ geometry
def perp(p, a, b):
    (x, y), (x1, y1), (x2, y2) = p, a, b
    dx, dy = x2-x1, y2-y1
    if dx == 0 and dy == 0: return math.hypot(x-x1, y-y1)
    t = max(0, min(1, ((x-x1)*dx + (y-y1)*dy)/(dx*dx + dy*dy)))
    return math.hypot(x-(x1+t*dx), y-(y1+t*dy))

def dp(pts, tol):
    """Douglas-Peucker, iterative -- some of these rings run to 6,500 points
    and the recursive form blows the stack."""
    if len(pts) < 3: return pts
    keep = [False]*len(pts); keep[0] = keep[-1] = True
    stack = [(0, len(pts)-1)]
    while stack:
        i, j = stack.pop()
        if j <= i+1: continue
        dmax, idx = 0.0, i
        for k in range(i+1, j):
            d = perp(pts[k], pts[i], pts[j])
            if d > dmax: dmax, idx = d, k
        if dmax > tol:
            keep[idx] = True
            stack.append((i, idx)); stack.append((idx, j))
    return [p for p, k in zip(pts, keep) if k]

def rings(geom):
    t, c = geom["type"], geom["coordinates"]
    if t == "Polygon": return [c[0]]
    if t == "MultiPolygon": return [p[0] for p in c]
    return []

def projector(lon0, lon1, lat0, lat1, width=1000.0):
    kx = math.cos(math.radians((lat0+lat1)/2))
    sx = width/((lon1-lon0)*kx)
    def P(lat, lon): return ((lon-lon0)*kx*sx, (lat1-lat)*sx)
    return P, width, (lat1-lat0)*sx

def path(P, pts, close=False):
    return " ".join(("M" if i == 0 else "L")+"%.1f %.1f" % P(*p)
                    for i, p in enumerate(pts)) + (" Z" if close else "")

# ============================================================ 1. the city map
# The crop is the basin floor. Sakyo and Ukyo run far into the mountains; their
# geometry is drawn and then clipped by the viewBox rather than being cut here,
# so the ward edges stay true right up to the frame.
LON0, LON1, LAT0, LAT1 = 135.645, 135.832, 34.955, 35.055
P, W, H = projector(LON0, LON1, LAT0, LAT1)
MARGIN = 260.0                      # keep rings a little outside the frame

wards = json.loads((SRC/"kyoto_wards.geojson").read_text(encoding="utf-8"))
paths, kept, dropped = [], 0, 0
for ft in wards["features"]:
    for ring in rings(ft["geometry"]):
        pts = [P(la, lo) for lo, la in ring]
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        if max(xs) < -MARGIN or min(xs) > W+MARGIN or max(ys) < -MARGIN or min(ys) > H+MARGIN:
            dropped += 1; continue
        simp = dp(pts, 0.7)
        if len(simp) < 4: continue
        kept += 1
        paths.append('<path class="kward" d="%s Z"/>' % " ".join(
            ("M" if i == 0 else "L")+"%.1f %.1f" % p for i, p in enumerate(simp)))

# rail, through the real stations it calls at
KARASUMA = [(34.9858,135.7588),(35.0035,135.7596),(35.0109,135.7596),
            (35.0182,135.7596),(35.0294,135.7596),(35.0442,135.7588)]
TOZAI    = [(35.0125,135.7505),(35.0109,135.7596),(35.0102,135.7690),
            (35.0093,135.7757),(35.0100,135.7817),(35.0087,135.7889)]
KEIHAN   = [(34.9671,135.7727),(34.9766,135.7715),(34.9931,135.7705),(34.9974,135.7712),
            (35.0036,135.7720),(35.0093,135.7730),(35.0181,135.7727),(35.0300,135.7700)]
HANKYU   = [(35.0035,135.7455),(35.0035,135.7596),(35.0035,135.7686)]
JR_SAGANO= [(34.9858,135.7588),(35.0106,135.7395),(35.0150,135.7050),(35.0186,135.6828)]
JR_NARA  = [(34.9858,135.7588),(34.9766,135.7666),(34.9673,135.7726),(34.9600,135.7760)]

SPOTS = [
 (34.9949,135.7850,"Kiyomizu-dera &middot; 06:00","e","r"),
 (35.0000,135.7807,"Kodai-ji","e","r"),
 (35.0113,135.7944,"Nanzen-ji","e","r"),
 (35.0155,135.7944,"Eikan-do","e","r"),
 (35.0270,135.7982,"Ginkaku-ji","e","r"),
 (35.0131,135.6776,"Arashiyama","w","l"),
 (35.0394,135.7292,"Kinkaku-ji","w","l"),
 (35.0345,135.7183,"Ryoan-ji","w","l"),
 (34.9671,135.7727,"Fushimi Inari","s","r"),
 (34.9760,135.7740,"Tofuku-ji &middot; 08:30","s","r"),
 (35.0142,135.7481,"Nijo Castle","o","l"),
 (35.0050,135.7649,"Nishiki","o","l"),
]
# a few anchors sit close enough that their labels collide; nudge those labels
# off the marker by a percentage of the frame. The marker itself never moves.
NUDGE = {"Eikan-do": (0, -2.4), "Nijo Castle": (0, -3.2)}

# no hotel is chosen yet, so the green marker is the interchange the plan leans
# on rather than a specific bed
HOTEL   = (35.0109,135.7596,"Karasuma Oike &middot; both subways")
STATION = (34.9858,135.7588,"Kyoto Station")

o = ['<div class="mapwrap">',
     '<svg class="map kmap" viewBox="0 0 %.0f %.0f" role="img" aria-label="Map of Kyoto city by ward, '
     'with the anchors of each day and the rail lines">' % (W, H),
     '<rect x="0" y="0" width="%.0f" height="%.0f" class="kbg"/>' % (W, H)]
o += paths
for line, cls in ((KARASUMA,"krail ksub"), (TOZAI,"krail ksub"), (KEIHAN,"krail"),
                  (HANKYU,"krail"), (JR_SAGANO,"krail kjr"), (JR_NARA,"krail kjr")):
    o.append('<path class="%s" d="%s"/>' % (cls, path(P, line)))
for lat, lon, lab, day, side in SPOTS:
    x, y = P(lat, lon)
    o.append('<g class="kmk kmk-%s" role="img" aria-label="%s">'
             '<circle class="ohalo" cx="%.1f" cy="%.1f" r="10"/>'
             '<circle class="odot" cx="%.1f" cy="%.1f" r="5"/></g>' % (day, lab, x, y, x, y))
for lat, lon, lab, cls in ((HOTEL[0],HOTEL[1],HOTEL[2],"kmk-bed"),
                           (STATION[0],STATION[1],STATION[2],"kmk-gate")):
    x, y = P(lat, lon)
    o.append('<g class="kmk %s" role="img" aria-label="%s">'
             '<circle class="ohalo" cx="%.1f" cy="%.1f" r="11"/>'
             '<circle class="odot" cx="%.1f" cy="%.1f" r="5.5"/></g>' % (cls, lab, x, y, x, y))
o.append('</svg>')
def lbl(P, W, H, lat, lon, text, side, extra=""):
    x, y = P(lat, lon)
    dx, dy = NUDGE.get(text.split(" &middot;")[0], (0, 0))
    return '<span class="olb olb-%s %s" style="left:%.3f%%;top:%.3f%%">%s</span>' % (
        side, extra, x/W*100 + dx, y/H*100 + dy, text)
for lat, lon, lab, day, side in SPOTS:
    o.append(lbl(P, W, H, lat, lon, lab, side, "klb-"+day))
o.append(lbl(P, W, H, HOTEL[0], HOTEL[1], HOTEL[2], "l", "olb-bed"))
o.append(lbl(P, W, H, STATION[0], STATION[1], STATION[2], "r", "klb-gate"))
o.append('</div>')
CITY = "\n".join(o)

# ======================================================== 2. the triangle map
T_LON0, T_LON1, T_LAT0, T_LAT1 = 135.44, 135.90, 34.60, 35.03
TP, TW, TH = projector(T_LON0, T_LON1, T_LAT0, T_LAT1)
NAMBA, KNARA, KYOTO = (34.6659,135.5010), (34.6851,135.8300), (34.9858,135.7588)
t = ['<div class="mapwrap kmini">',
     '<svg class="map kmap" viewBox="0 0 %.0f %.0f" role="img" aria-label="The Osaka to Nara to Kyoto '
     'triangle, showing the route of the 24th">' % (TW, TH),
     '<rect x="0" y="0" width="%.0f" height="%.0f" class="kbg"/>' % (TW, TH),
     '<path class="ktri" d="%s"/>' % path(TP, [NAMBA, KNARA, KYOTO], close=True),
     '<path class="kleg" d="%s"/>' % path(TP, [NAMBA, KNARA]),
     '<path class="kleg" d="%s"/>' % path(TP, [KNARA, KYOTO])]
for (lat, lon), cls, lab in ((NAMBA,"kmk-gate","Osaka-Namba"), (KNARA,"kmk-s","Kintetsu Nara"),
                            (KYOTO,"kmk-bed","Kyoto")):
    x, y = TP(lat, lon)
    t.append('<g class="kmk %s" role="img" aria-label="%s">'
             '<circle class="ohalo" cx="%.1f" cy="%.1f" r="16"/>'
             '<circle class="odot" cx="%.1f" cy="%.1f" r="8"/></g>' % (cls, lab, x, y, x, y))
t.append('</svg>')
t.append(lbl(TP, TW, TH, NAMBA[0], NAMBA[1], "Osaka-Namba", "r", "klb-gate"))
t.append(lbl(TP, TW, TH, KNARA[0], KNARA[1], "Kintetsu Nara", "l", "klb-s"))
t.append(lbl(TP, TW, TH, KYOTO[0], KYOTO[1], "Kyoto", "l", "olb-bed"))
# the fare labels sit off their line, not on it -- on the midpoint the first one
# lands straight on top of the Kintetsu Nara label
t.append(lbl(TP, TW, TH, 34.6450, 135.6655, "39 m &middot; &yen;680", "r", "klb-leg"))
t.append(lbl(TP, TW, TH, 34.8355, 135.7200, "45 m &middot; &yen;760", "l", "klb-leg"))
t.append('</div>')
TRI = "\n".join(t)

(SRC/"kyoto.frag.html").write_text(CITY + "\n<!--KTRIANGLE-->\n" + TRI, encoding="utf-8")
print("src/kyoto.frag.html written")
print("  city map  %.0f x %.0f | %d rings drawn, %d clipped out | %d anchors"
      % (W, H, kept, dropped, len(SPOTS)))
print("  triangle  %.0f x %.0f" % (TW, TH))
