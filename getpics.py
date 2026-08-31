# -*- coding: utf-8 -*-
import json,urllib.parse,urllib.request,subprocess,base64,re,time,os
API="https://commons.wikimedia.org/w/api.php"; UA="KyushuRoutePlanner/1.0 (github.com/hellhoundsx)"
OUT="pics/"; os.makedirs(OUT,exist_ok=True)
PICKS=[
 # route
 ("Mameda-machi, Hita",       "File:Mameda-machi, Hita 02.jpg"),
 ("Nabegataki Falls",         "File:裏から見る鍋ヶ滝.jpg"),
 ("Kurokawa · DeepSpot",      "File:Kurokawa-Onsen Light-up.jpg"),
 ("Daikanbo",                 "File:A view of the five mountains of Aso from Daikanbo viewpoint.jpg"),
 ("Nakadake · Kusasenri",     "File:Sulphuric lake in Naka-dake crater (5274089965).jpg"),
 ("Amano-Iwato",              "File:Amanoiwato-west-shrine (28795304727).jpg"),
 ("Takachiho · the gorge",    "File:Manai Falls at Takachiho Gorge.jpg"),
 ("Miyazaki",                 "File:Miyazaki Miyazaki-jingu Haiden 1.JPG"),
 ("Aoshima Shrine",           "File:Ogre's Washboards and Torii, Aoshima, Miyazaki - Nov 5, 2017.jpg"),
 ("Udo Jingu",                "File:Udo-jingu Main hall 001.jpg"),
 ("Obi, Nichinan",            "File:Obi, Nichinan, Ōtemon Gate of Obi Castle 01.jpg"),
 # could add
 ("Beppu",                    "File:Umi Jigoku (Sea Hell) in Beppu.jpg"),
 ("Yufuin",                   "File:Lake Kinrin in Yufuin, Oita - Aug 24, 2018 (1).jpg"),
 ("Kumamoto Castle",          "File:Kumamoto Castle 04n4272.jpg"),
 ("Takamori · Minamiaso",     "File:Mt Aso from Minamiaso Hisaishi.JPG"),
 ("Gokase",                   "File:Gokase Geo-Park.JPG"),
 ("Nobeoka",                  "File:MtAtago Nobeoka from Shiroyama 2010.JPG"),
 ("Sekinoo Falls",            "File:Sekinoo Falls 01.jpg"),
 ("Kirishima Jingu",          "File:Kirishima-Jingu Front.jpg"),
 ("Ebino Highlands",          "File:Ebino Plateau05n4592.jpg"),
 ("Cape Toi",                 "File:Wild horse of cape toi , 都井岬の野生馬 - panoramio - z tanuki (4).jpg"),
 ("Sakurajima",               "File:2025-03-01 Sakurajima and Sakura.jpg"),
]
def meta(titles):
    for a in range(5):
        try:
            r=urllib.request.Request(API+"?"+urllib.parse.urlencode(dict(action="query",
              titles="|".join(titles),prop="imageinfo",iiprop="url|extmetadata",
              iiurlwidth="900",format="json",formatversion="2")),headers={"User-Agent":UA})
            return json.load(urllib.request.urlopen(r,timeout=45))
        except Exception as e:
            if a==4: raise
            time.sleep(6*(a+1))
titles=[t for _,t in PICKS]; M={}
for i in range(0,len(titles),4):
    d=meta(titles[i:i+4])
    for p in d["query"]["pages"]:
        if "imageinfo" not in p: print("  !! MISS",p.get("title")); continue
        ii=p["imageinfo"][0]; em=ii.get("extmetadata",{})
        g=lambda k:(em.get(k,{}) or {}).get("value","")
        M[p["title"]]=dict(thumb=ii["thumburl"],page=ii["descriptionurl"],
            lic=g("LicenseShortName"),author=re.sub(r"<[^>]+>","",g("Artist")).strip()[:70])
    time.sleep(2)
res=[]
for label,title in PICKS:
    if title not in M: print("  SKIP (no meta):",label); continue
    info=M[title]; base=re.sub(r'[^a-z0-9]+','_',label.lower())
    raw,fin=OUT+base+".src.jpg", OUT+base+".jpg"
    for a in range(4):
        try:
            rq=urllib.request.Request(info["thumb"],headers={"User-Agent":UA})
            open(raw,"wb").write(urllib.request.urlopen(rq,timeout=60).read()); break
        except Exception as e:
            if a==3: print("  DL FAIL",label,e); raw=None
            else: time.sleep(5*(a+1))
    if not raw: continue
    subprocess.run(["sips","-Z","520",raw,"--out",fin],capture_output=True)
    subprocess.run(["sips","-c","293","520",fin,"--out",fin],capture_output=True)
    subprocess.run(["sips","-s","format","jpeg","-s","formatOptions","62",fin,"--out",fin],capture_output=True)
    b=open(fin,"rb").read()
    res.append(dict(label=label,b64=base64.b64encode(b).decode(),kb=round(len(b)/1024,1),
                    lic=info["lic"],author=info["author"],page=info["page"]))
    print(f"  {label[:24]:26s} {res[-1]['kb']:6.1f}KB  {info['lic']:14s} {info['author'][:30]}")
json.dump(res,open("pics.json","w"))
print(f"\n{len(res)} images, {round(sum(r['kb'] for r in res)/1024,2)} MB")
