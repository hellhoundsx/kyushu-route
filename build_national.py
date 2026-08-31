# -*- coding: utf-8 -*-
import json, math
S="/private/tmp/claude-502/-Users-ricardo-gomes-Documents-apps-Nexus/0c7e087e-eb8c-40da-bc86-9cfbdc429ed8/scratchpad/"
N=json.load(open(S+"japan_national.json")); M=N["meta"]
KX,SX,LON0,LAT1=M["kx"],M["sx"],M["lon0"],M["lat1"]
def P(la,lo): return ((lo-LON0)*KX*SX,(LAT1-la)*SX)
VB=(70,40,905,545)                      # crop off empty ocean
def pc(x,y): return ((x-VB[0])/VB[2]*100,(y-VB[1])/VB[3]*100)

CITY=[  # lat, lon, label, anchor, kind  (anchors keep the edge cities and the Kansai cluster apart)
 (33.5859,130.4510,"Fukuoka","r","hop"),
 (31.5830,130.5420,"Kagoshima","r","hop"),
 (34.6900,135.5000,"Osaka","l","stay"),
 (34.6850,135.8300,"Nara","r","via"),
 (35.0110,135.7680,"Kyoto","t","stay"),
 (35.6800,139.6900,"Tokyo","l","stay"),
]
# the Kyushu drive, through its real waypoints
DRIVE=[(33.5859,130.4510),(33.0836,131.1206),(32.7117,131.3078),(31.9170,131.4230),(31.5830,130.5420)]

def poly(seq): return " ".join(f"{P(la,lo)[0]:.1f},{P(la,lo)[1]:.1f}" for la,lo in seq)

o=[f'<svg class="nmap" viewBox="{VB[0]} {VB[1]} {VB[2]} {VB[3]}" role="img" '
   f'aria-label="Overview of the whole trip from Kyushu through Osaka and Kyoto to Tokyo">']
o.append(f'<rect x="0" y="0" width="{M["w"]:.0f}" height="{M["h"]:.0f}" class="nsea"/>')
o.append(f'<g class="nland"><path d="{N["path"]}"/></g>')
# leg 1 - driven, planned
o.append(f'<polyline class="nleg ndone" points="{poly(DRIVE)}"/>')
# leg 0 - the inbound: Tokyo -> Fukuoka on the morning of the 17th.
# bowed south over the Pacific so it reads as a flight and does not sit on the rail line
TY=P(35.6800,139.6900); FK=P(33.5859,130.4510); CT=P(31.15,135.10)
o.append(f'<path class="nfly nfly-in" d="M{TY[0]:.1f},{TY[1]:.1f} Q{CT[0]:.1f},{CT[1]:.1f} {FK[0]:.1f},{FK[1]:.1f}"/>')
# leg 2 - flight Kagoshima -> Osaka
o.append(f'<polyline class="nfly" points="{poly([(31.5830,130.5420),(34.6900,135.5000)])}"/>')
# legs 3 & 4 - rail, still TBD
o.append(f'<polyline class="nleg ntbd" points="{poly([(34.6900,135.5000),(34.6850,135.8300),(35.0110,135.7680)])}"/>')
o.append(f'<polyline class="nleg ntbd" points="{poly([(35.0110,135.7680),(35.6800,139.6900)])}"/>')
for la,lo,lab,anc,kind in CITY:
    x,y=P(la,lo)
    o.append(f'<g class="nmk nmk-{kind}"><circle class="nhalo" cx="{x:.1f}" cy="{y:.1f}" r="13"/>'
             f'<circle class="ndot" cx="{x:.1f}" cy="{y:.1f}" r="7"/></g>')
# label anchors for the inbound arc, placed at its southern apex
AP=((TY[0]+2*CT[0]+FK[0])/4,(TY[1]+2*CT[1]+FK[1])/4)
o.append('</svg>')
svg="\n".join(o)

lab=[]
for la,lo,label,anc,kind in CITY:
    x,y=P(la,lo); L,T=pc(x,y)
    lab.append(f'<span class="nlb nlb-{anc} nlb-{kind}" style="left:{L:.3f}%;top:{T:.3f}%">{label}</span>')
L,T=pc(*AP)
lab.append(f'<span class="nlb nlb-fly nlb-b" style="left:{L:.3f}%;top:{T:.3f}%">17 Nov &middot; Tokyo &rarr; Fukuoka</span>')
open(S+"national.frag.html","w").write(svg+"\n<!--NLABELS-->\n"+"\n".join(lab))
print("overview svg",len(svg),"chars |",len(CITY),"cities")
for la,lo,l,a,k in CITY:
    x,y=P(la,lo); L,T=pc(x,y)
    inside = 0<=L<=100 and 0<=T<=100
    print(f"  {l:10s} {L:6.1f}% {T:6.1f}%  {'ok' if inside else 'OUTSIDE CROP'}")
