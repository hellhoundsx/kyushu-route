# -*- coding: utf-8 -*-
import re
p="page.tpl.html"; t=open(p,encoding="utf-8").read()
HEAD=t[:t.index('<div class="wrap">')]
BODY=t[t.index('<div class="wrap">'):]

# ---- split the body into its sections, keyed by heading ----
bounds=[]
for m in re.finditer(r'<section class="(?:sec|mapsec)">', BODY):
    bounds.append(m.start())
bounds.append(BODY.index('<footer class="foot">'))
secs={}
order=[]
for i in range(len(bounds)-1):
    blk=BODY[bounds[i]:bounds[i+1]]
    h=re.search(r'<h2[^>]*>(.*?)</h2>', blk, re.S)
    key=re.sub(r'<[^>]+>','',h.group(1)).strip() if h else f"sec{i}"
    secs[key]=blk; order.append(key)
print("sections captured:", len(secs))
assert len(secs)==10, order

MAST=BODY[BODY.index('<div class="wrap">'):bounds[0]]
FOOT=BODY[BODY.index('<footer class="foot">'):]

# ---- the three city TBD articles move out of the Kyushu timeline ----
dbd=secs["The route, day by day"]
first_osk=dbd.index('<article class="day dOsk"')
last_end=dbd.rindex('</article>')+10
city_articles=dbd[first_osk:last_end]
secs["The route, day by day"]=dbd[:first_osk]+dbd[last_end:]
osk=re.findall(r'<article class="day dOsk">.*?</article>', city_articles, re.S)
assert len(osk)==3, len(osk)
print("city articles lifted:", len(osk))

def panel(pid, label, inner, selected=False):
    return (f'\n  <div class="panel" id="p-{pid}" role="tabpanel" aria-labelledby="t-{pid}"'
            f'{"" if selected else " hidden"}>\n{inner}\n  </div>\n')

TRIP = secs["The whole trip"] + secs["Where you sleep"] + secs["Still open"]
KYU  = (secs["Leg 1 &middot; Kyushu, by car"] + secs["Book these before you fly"]
        + secs["Night 2: Takachiho, en-suite only"] + secs["Night 3: Miyazaki, the easy one"]
        + secs["The route, day by day"] + secs["If you add more days"] + secs["Every leg, measured"])

def tbd(name, dates, nights, art, note):
    return (f'  <section class="sec">\n    <h2>{name}</h2>\n'
            f'    <p>{dates} &middot; {nights}. Not planned yet.</p>\n'
            f'    <div class="days">\n{art}\n    </div>\n'
            f'    <div class="tbdbox">\n      <p class="tbd-t">What this leg needs</p>\n'
            f'      <p class="tbd-n">{note}</p>\n    </div>\n  </section>\n')

OSA = tbd("Leg 2 &middot; Osaka", "20&ndash;24 November", "four nights", osk[0],
  "Beds for four in two en-suite rooms, a district to base in, and a plan for the days. No car from here on, "
  "so this becomes a trains-and-walking leg. Availability is not the constraint in a city this size.")
KYO = tbd("Leg 3 &middot; Kyoto, via Nara", "24&ndash;28 November", "four nights", osk[1],
  "A regional map of the Osaka&ndash;Nara&ndash;Kyoto triangle, the Nara day on the 24th, and beds. This is the tight "
  "leg: late November is peak maple season, the busiest week of the Kyoto year, so beds and the popular temples "
  "want booking well ahead.")
TOK = tbd("Leg 4 &middot; Tokyo", "28 November &ndash; 4 December", "six nights", osk[2],
  "A district map rather than a coastline &mdash; at city scale the useful drawing is neighbourhoods and stations. "
  "Six nights means where you sleep matters more than which hotel, and the 4th is the flight home.")

TABS = '''  <div class="tabs" role="tablist" aria-label="Trip legs">
    <button class="tab" id="t-trip"   role="tab" aria-controls="p-trip"   aria-selected="true"  data-p="trip">The whole trip</button>
    <button class="tab" id="t-kyushu" role="tab" aria-controls="p-kyushu" aria-selected="false" data-p="kyushu"><span class="tab-n">1</span> Kyushu</button>
    <button class="tab" id="t-osaka"  role="tab" aria-controls="p-osaka"  aria-selected="false" data-p="osaka"><span class="tab-n">2</span> Osaka</button>
    <button class="tab" id="t-kyoto"  role="tab" aria-controls="p-kyoto"  aria-selected="false" data-p="kyoto"><span class="tab-n">3</span> Kyoto</button>
    <button class="tab" id="t-tokyo"  role="tab" aria-controls="p-tokyo"  aria-selected="false" data-p="tokyo"><span class="tab-n">4</span> Tokyo</button>
  </div>
'''
NEW = (MAST + TABS
       + panel("trip","The whole trip",TRIP,selected=True)
       + panel("kyushu","Kyushu",KYU)
       + panel("osaka","Osaka",OSA)
       + panel("kyoto","Kyoto",KYO)
       + panel("tokyo","Tokyo",TOK)
       + FOOT)
open(p,"w",encoding="utf-8").write(HEAD+NEW)
print("tabified. panels: trip, kyushu, osaka, kyoto, tokyo")
