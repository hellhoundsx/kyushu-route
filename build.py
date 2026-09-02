import json, math
S="/private/tmp/claude-502/-Users-ricardo-gomes-Documents-apps-Nexus/0c7e087e-eb8c-40da-bc86-9cfbdc429ed8/scratchpad/"
K=json.load(open(S+"kyushu.json")); M=K["meta"]; KX,SX,LON0,LAT1=M["kx"],M["sx"],M["lon0"],M["lat1"]
def P(lat,lon): return ((lon-LON0)*KX*SX,(LAT1-lat)*SX)
VB=(148,110,815,1164)
def pc(x,y): return ((x-VB[0])/VB[2]*100,(y-VB[1])/VB[3]*100)

SHORT={"Kurokawa &middot; DeepSpot":"Kurokawa",
       "Aoshima Shrine":"Aoshima",
       "Takachiho &middot; the gorge":"Takachiho",
       "Nakadake &middot; Kusasenri":"Nakadake",
       "Takamori &middot; Minamiaso":"Takamori"}

def p(lat,lon,day,kind,anc,label,note,when,leg="",status="",sclass=""):
    return dict(lat=lat,lon=lon,day=day,kind=kind,anc=anc,label=label,note=note,
                when=when,leg=leg,status=status,sclass=sclass)

# leg strings only quote MEASURED times; intermediate stops get a positional phrase instead
PL=[
 p(33.5859,130.4510,17,"air","t","Fukuoka Airport",
   "Land at nine, collect the car at ten. Kurokawa is only 1 h 45 m away direct, so the afternoon is yours.",
   "17 Nov &middot; 09:00","arrive from Tokyo"),
 p(33.3213,130.9410,17,"stop","r","Mameda-machi, Hita",
   "A preserved Edo merchant street of white-walled townhouses. An hour is enough.",
   "17 Nov &middot; lunch","sits on the Fukuoka&ndash;Kurokawa line"),
 p(33.1170,131.0330,17,"stop","l","Nabegataki Falls",
   "A wide, low curtain of water you walk behind. Ten minutes from the house.",
   "17 Nov &middot; 14:00 or 15:00","","Timed entry, book online","warn"),
 p(33.0836,131.1206,17,"bed","r","Kurokawa &middot; DeepSpot",
   "Three bedrooms, private sauna, Aso panorama, 10 min drive from the village. &euro;222 for four. Buy the tegata pass for the baths.",
   "Night 1 &middot; 17 Nov","1 h 59 m from Fukuoka via Hita and the falls","Booked","ok"),
 p(32.9830,131.0330,18,"stop","r","Daikanbo",
   "The northern rim of the caldera, looking down the whole crater floor. The Milk Road runs along the ridge from here.",
   "18 Nov &middot; from 09:40","first stop out of Kurokawa"),
 p(32.8846,131.0787,18,"stop","l","Nakadake &middot; Kusasenri",
   "The live crater and the grass plain below it. November gate hours are 8:30&ndash;17:00.",
   "18 Nov &middot; around 11:30","","Cancelled if gas is high &mdash; check at breakfast","warn"),
 p(32.7400,131.3750,18,"stop","r","Amano-Iwato",
   "The cave the sun goddess hid in, plus the river cave at Amanoyasugawara filled with thousands of stacked stone cairns.",
   "18 Nov &middot; 15:00, in daylight","sunset is about 17:20"),
 p(32.7117,131.3078,18,"bed","l","Takachiho &middot; the gorge",
   "Kagura danced at the shrine at 20:00, about an hour. The self-row boat to Manai Falls goes at opening next morning.",
   "Night 2 &middot; 18 Nov","2 h 27 m from Kurokawa via Daikanbo and the crater","One bed left in town","warn"),
 p(31.9170,131.4230,19,"bed","r","Miyazaki",
   "Nishitachi for the night out. Chicken nanban was invented in this prefecture &mdash; eat it here, with the local beef.",
   "Night 3 &middot; 19 Nov","1 h 57 m from Takachiho, tolls","Not booked yet","open"),
 p(31.7970,131.4620,19,"stop","r","Aoshima Shrine",
   "An island shrine ringed by the Devil's Washboard, a shelf of wave-cut rock ribs exposed at low tide.",
   "19 Nov &middot; afternoon","1 h 13 m round the coast from Miyazaki"),
 p(31.6330,131.4570,19,"stop","r","Udo Jingu",
   "A vermilion shrine built inside a sea cave in the cliff face. The most striking single thing on this coast.",
   "19 Nov &middot; afternoon","on the same coast run"),
 p(31.6220,131.3530,19,"stop","b","Obi, Nichinan",
   "An intact samurai castle town, the turning point of the coast day.",
   "19 Nov &middot; late afternoon","southern end of the run"),
 p(31.8034,130.7194,20,"air","b","Kagoshima Airport",
   "Car back at the airport, flight at 17:00, then four nights in Osaka to the 24th. Kirishima Jingu is 19 minutes off the direct run and sits beside the airport.",
   "20 Nov &middot; 17:00 to Osaka","1 h 34 m from Miyazaki, 1 h 53 m via Kirishima Jingu","Osaka 20&ndash;24 Nov","ok"),

 p(33.2790,131.5000,0,"opt","r","Beppu",
   "Steam vents across a whole hillside and eight distinct hot-spring fields. The biggest onsen town in Kyushu.",
   "if you add a night at the front","about 1 h from Kurokawa"),
 p(33.2640,131.3600,0,"opt","l","Yufuin",
   "A smart, walkable onsen town with a lake and a long craft street.",
   "if you add a night at the front","almost exactly on the way in"),
 p(33.5215,130.5349,17,"alt","r","Dazaifu Tenmangu",
   "A major shrine 30 min out of Fukuoka, and about thirty shops along its approach grilling umegae mochi to order &mdash; red bean inside, plum-blossom stamped on a hot iron plate.",
   "17 Nov &middot; the long way","+21 min on the day"),
 p(33.3167,130.5083,17,"alt","l","Kurume",
   "Where tonkotsu ramen was invented, at a stall called Nankin Senryo in 1937. The milky white broth came a decade later, by accident, when a cook at Sankyu left the pot on too long.",
   "17 Nov &middot; the long way","lunch, straight off the expressway"),
 p(32.8030,130.7080,17,"alt","l","Kumamoto Castle",
   "Reopened August 2026 after the earthquake, with new stone-wall damage and reconstruction running to 2052. Sakuranobaba Josaien at its foot is the easiest lunch of the day; Suizenji Jojuen garden is a short hop.",
   "17 Nov &middot; alternative route","+1 h 18 m on the day"),
 p(33.0029,130.9451,17,"alt","l","Kikuchi Gorge",
   "Four kilometres of clear water and moss under broadleaf forest, and one of Kumamoto's best autumn walks. Closed after the quake, entry ban since lifted.",
   "17 Nov &middot; only with a trade","11 min of driving, an hour of walking"),
 p(32.8220,131.1280,0,"opt","r","Takamori &middot; Minamiaso",
   "The caldera's southern floor, and the moss-covered cave shrine at Kamishikimi Kumano Imasu.",
   "if you add a night in the middle","just south of the crater"),
 p(32.6580,131.1830,0,"opt","l","Gokase",
   "Not a sight, but the closest place to Takachiho with rooms free &mdash; including a 2-bed, 2-bath cottage at &euro;137.",
   "fallback if Takachiho stays full","14 km from Takachiho"),
 p(32.5820,131.6650,0,"opt","r","Nobeoka",
   "The coastal gateway, if you would rather reach the sea on the 18th than the 19th.",
   "alternative shape for day 18","east of Takachiho"),
 p(31.7460,131.0130,20,"stop","r","Sekinoo Falls",
   "Potholes among the largest in the world, a National Natural Monument since 1928, plus suspension bridges over the gorge. Free entry and parking. 30 min for the falls, 50 with the potholes, 60 for the full loop.",
   "20 Nov &middot; mid-morning","4 min on top of the Kirishima detour"),
 p(31.8580,130.8360,20,"stop","r","Kirishima Jingu",
   "A shrine in deep cedar forest on the volcano's flank, twenty minutes from the airport.",
   "20 Nov &middot; late morning","19 min off the direct run"),
 p(31.8375,130.6736,20,"stop","l","Kareigawa Station",
   "Opened 1903 and the oldest wooden station building in Kyushu, a National Registered Cultural Property since 2006. Original waiting room and ticket counter. Ten minutes from the airport, so it is the natural last stop.",
   "20 Nov &middot; early afternoon","4 min on top of the other two"),
 p(31.9430,130.8590,0,"opt","l","Ebino Highlands",
   "Crater lakes on the rim above Kirishima, with genuine autumn colour in November. A winding climb, so it wants a couple of hours rather than a look.",
   "only with a late car return","+58 min on the run to the airport"),
 p(31.3680,131.3350,0,"opt","r","Cape Toi",
   "Wild horses grazing on an open headland at the southern end of the Nichinan coast.",
   "stretches the coast day","below Obi"),
 p(31.5850,130.6570,0,"opt","r","Sakurajima",
   "A live volcano across the bay, reached by a 15-minute ferry. Needs you to be in the city, which an airport car return means you are not.",
   "only if you add a Kagoshima night","ferry from the city"),
]

places=[]
for q in PL:
    x,y=P(q["lat"],q["lon"]); L,T=pc(x,y)
    gmap="https://www.google.com/maps/search/?api=1&amp;query=%.5f%%2C%.5f"%(q["lat"],q["lon"])
    places.append(dict(x=round(x,1),y=round(y,1),l=round(L,3),t=round(T,3),
                       day=q["day"],kind=q["kind"],anc=q["anc"],label=q["label"],note=q["note"],
                       when=q["when"],leg=q["leg"],status=q["status"],sclass=q["sclass"],
                       gmap=gmap, lat=q["lat"], lon=q["lon"]))
byl={p_["label"]:p_ for p_ in places}
def line(*ls): return " ".join(f'{byl[l]["x"]},{byl[l]["y"]}' for l in ls)
ALT17=line("Fukuoka Airport","Dazaifu Tenmangu","Kurume","Kumamoto Castle","Kikuchi Gorge","Nabegataki Falls","Kurokawa &middot; DeepSpot")
ROUTES=[("17",line("Fukuoka Airport","Mameda-machi, Hita","Nabegataki Falls","Kurokawa &middot; DeepSpot")),
        ("18",line("Kurokawa &middot; DeepSpot","Daikanbo","Nakadake &middot; Kusasenri","Amano-Iwato","Takachiho &middot; the gorge")),
        ("19",line("Takachiho &middot; the gorge","Miyazaki","Aoshima Shrine","Udo Jingu","Obi, Nichinan")),
        ("20",line("Miyazaki","Sekinoo Falls","Kirishima Jingu","Kareigawa Station","Kagoshima Airport"))]

o=[]
o.append(f'<svg class="map" viewBox="{VB[0]} {VB[1]} {VB[2]} {VB[3]}" role="img" aria-label="Route map of Kyushu from Fukuoka to Kagoshima">')
o.append('<rect x="0" y="0" width="1000" height="1383" class="sea"/>')
o.append('<g class="land">')
for nm,dpath in K["prefs"].items(): o.append(f'<path d="{dpath}"/>')
o.append('</g>')
o.append(f'<polyline class="rt rt17 rtalt" data-day="17" points="{ALT17}"/>')
for day,pts in ROUTES:
    o.append(f'<polyline class="rt rt{day}" data-day="{day}" points="{pts}"/>')
fk=byl["Fukuoka Airport"]; kg=byl["Kagoshima Airport"]

def head(tip, ctrl, L=17.0, W=6.0):
    """Arrowhead built from the curve's end tangent, so it always points along the line."""
    tx,ty = tip; cx,cy = ctrl
    dx,dy = tx-cx, ty-cy                       # tangent at the tip = tip - control point
    n = math.hypot(dx,dy) or 1.0
    dx,dy = dx/n, dy/n
    bx,by = tx-dx*L, ty-dy*L                   # base centre, L behind the tip
    px,py = -dy, dx                            # unit normal
    return (f'M{tx:.1f},{ty:.1f} L{bx+px*W:.1f},{by+py*W:.1f} '
            f'L{bx-px*W:.1f},{by-py*W:.1f} Z')

# inbound from Tokyo: ENE, 15 deg above horizontal, arriving westward into Fukuoka
IN_START=(fk["x"]+228, fk["y"]-61); IN_CTRL=(fk["x"]+118, fk["y"]-52); IN_TIP=(fk["x"]+15, fk["y"]-6)
o.append(f'<path class="fly" d="M{IN_START[0]},{IN_START[1]} Q{IN_CTRL[0]},{IN_CTRL[1]} {IN_TIP[0]},{IN_TIP[1]}"/>')
o.append(f'<path class="flyhead" d="{head(IN_TIP, IN_CTRL)}"/>')

# outbound to Osaka: NE, 36.6 deg above horizontal
OUT_START=(kg["x"]+14, kg["y"]-10); OUT_CTRL=(kg["x"]+64, kg["y"]-44); OUT_TIP=(kg["x"]+124, kg["y"]-92)
o.append(f'<path class="fly" d="M{OUT_START[0]},{OUT_START[1]} Q{OUT_CTRL[0]},{OUT_CTRL[1]} {OUT_TIP[0]},{OUT_TIP[1]}"/>')
o.append(f'<path class="flyhead" d="{head(OUT_TIP, OUT_CTRL)}"/>')
for i,q in enumerate(places):
    X,Y=q["x"],q["y"]
    o.append(f'<g class="mk mk-{q["kind"]}" data-day="{q["day"]}" data-i="{i}" tabindex="0" role="button" aria-label="{q["label"]}">')
    if q["kind"] in ("opt","alt"):
        o.append(f'<circle class="hit" cx="{X}" cy="{Y}" r="20"/><circle class="dot" cx="{X}" cy="{Y}" r="7.5"/>')
    elif q["kind"]=="bed":
        o.append(f'<circle class="hit" cx="{X}" cy="{Y}" r="27"/>'
                 f'<circle class="halo" cx="{X}" cy="{Y}" r="21"/>'
                 f'<circle class="ring" cx="{X}" cy="{Y}" r="14.5"/>'
                 f'<circle class="core" cx="{X}" cy="{Y}" r="6"/>')
    else:
        o.append(f'<circle class="hit" cx="{X}" cy="{Y}" r="22"/>'
                 f'<circle class="halo" cx="{X}" cy="{Y}" r="15"/>'
                 f'<circle class="dot" cx="{X}" cy="{Y}" r="9"/>')
    o.append('</g>')
km50=50_000/(111_320/SX)
o.append(f'<g class="scale"><line x1="188" y1="1240" x2="{188+km50:.0f}" y2="1240"/>'
         f'<line x1="188" y1="1232" x2="188" y2="1248"/>'
         f'<line x1="{188+km50:.0f}" y1="1232" x2="{188+km50:.0f}" y2="1248"/></g>')
o.append('</svg>')
svg="\n".join(o)

lab=[]
for i,q in enumerate(places):
    extra=("lb-opt" if q["kind"]=="opt" else "lb-rt lb-alt" if q["kind"]=="alt"
           else "lb-rt lb-bed" if q["kind"]=="bed" else "lb-rt")
    lab.append(f'<span class="lb lb-{q["anc"]} {extra}" data-day="{q["day"]}" data-i="{i}" '
               f'style="left:{q["l"]}%;top:{q["t"]}%">{SHORT.get(q["label"], q["label"])}</span>')
L1,T1=pc(fk["x"]+228,fk["y"]-61); L2,T2=pc(kg["x"]+124,kg["y"]-92)
lab.append(f'<span class="lb lb-fly lb-r" style="left:{L1:.3f}%;top:{T1:.3f}%">from Tokyo</span>')
lab.append(f'<span class="lb lb-fly lb-l" style="left:{L2:.3f}%;top:{T2:.3f}%">to Osaka</span>')

open(S+"map.frag.html","w").write(svg+"\n<!--LABELS-->\n"+"\n".join(lab))
json.dump(places,open(S+"places.final.json","w"))
print("svg",len(svg),"| places",len(places),
      "| with status",sum(1 for q in places if q["status"]),
      "| with leg",sum(1 for q in places if q["leg"]))
