import json,urllib.parse,urllib.request,subprocess,base64,os,re
API="https://commons.wikimedia.org/w/api.php"
UA="KyushuRoutePlanner/1.0 (personal travel page; github.com/hellhoundsx)"
OUT="pics/"
# marker label -> Commons file (curated: landscape, permissive licence, right subject)
PICKS=[
 ("Mameda-machi, Hita",              "File:Mameda-machi, Hita 02.jpg"),
 ("Nabegataki Falls",                "File:裏から見る鍋ヶ滝.jpg"),
 ("Kurokawa · DeepSpot",             "File:Kurokawa-Onsen Light-up.jpg"),
 ("Daikanbo",                        "File:Mt.Daikanbo 02.jpg"),
 ("Nakadake · Kusasenri",            "File:MountAsoCrater from Kusasenri viewpoint.jpg"),
 ("Amano-Iwato",                     "File:Amanoiwato-west-shrine (28795304727).jpg"),
 ("Takachiho · the gorge",           "File:Takachiho Gorge (52132194587).jpg"),
 ("Aoshima Shrine",                  "File:Ogre's Washboards and Torii, Aoshima, Miyazaki - Nov 5, 2016.jpg"),
 ("Udo Jingu",                       "File:Udo-jingu Main hall 001.jpg"),
 ("Obi, Nichinan",                   "File:Obi, Nichinan, Ōtemon Gate of Obi Castle 01.jpg"),
 ("Sakurajima",                      "File:2025-03-01 Sakurajima and Sakura.jpg"),
]
def meta(titles):
    r=urllib.request.Request(API+"?"+urllib.parse.urlencode(dict(
        action="query",titles="|".join(titles),prop="imageinfo",
        iiprop="url|extmetadata",iiurlwidth="900",format="json",formatversion="2")),
        headers={"User-Agent":UA})
    d=json.load(urllib.request.urlopen(r,timeout=40))
    m={}
    for p in d["query"]["pages"]:
        if "imageinfo" not in p: print("  !! no imageinfo:",p.get("title")); continue
        ii=p["imageinfo"][0]; em=ii.get("extmetadata",{})
        g=lambda k:(em.get(k,{}) or {}).get("value","")
        m[p["title"]]=dict(thumb=ii["thumburl"], page=ii["descriptionurl"],
            lic=g("LicenseShortName"), author=re.sub(r"<[^>]+>","",g("Artist")).strip()[:70])
    return m
titles=[t for _,t in PICKS]
M={}
for i in range(0,len(titles),5): M.update(meta(titles[i:i+5]))
res=[]
for label,title in PICKS:
    if title not in M: print("  MISS",title); continue
    info=M[title]
    raw=OUT+re.sub(r'[^a-z0-9]+','_',label.lower())+".src.jpg"
    fin=OUT+re.sub(r'[^a-z0-9]+','_',label.lower())+".jpg"
    r=urllib.request.Request(info["thumb"],headers={"User-Agent":UA})
    open(raw,"wb").write(urllib.request.urlopen(r,timeout=60).read())
    subprocess.run(["sips","-Z","520",raw,"--out",fin],capture_output=True)
    subprocess.run(["sips","-c","293","520",fin,"--out",fin],capture_output=True)
    subprocess.run(["sips","-s","format","jpeg","-s","formatOptions","62",fin,"--out",fin],capture_output=True)
    b=open(fin,"rb").read()
    res.append(dict(label=label, b64=base64.b64encode(b).decode(),
                    kb=round(len(b)/1024,1), lic=info["lic"], author=info["author"], page=info["page"]))
    print(f"  {label[:26]:28s} {res[-1]['kb']:6.1f} KB  {info['lic']:14s} {info['author'][:32]}")
json.dump(res,open("pics.json","w"))
print("\ntotal embedded:",round(sum(r['kb'] for r in res)/1024,2),"MB across",len(res),"images")
