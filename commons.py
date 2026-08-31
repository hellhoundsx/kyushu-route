import json,urllib.parse,urllib.request,sys
API="https://commons.wikimedia.org/w/api.php"
UA="KyushuRoutePlanner/1.0 (personal travel page; contact via github.com/hellhoundsx)"
def q(params):
    params.update(format="json",formatversion="2")
    r=urllib.request.Request(API+"?"+urllib.parse.urlencode(params),headers={"User-Agent":UA})
    return json.load(urllib.request.urlopen(r,timeout=30))
def search(term,n=6):
    d=q(dict(action="query",generator="search",gsrsearch="filetype:bitmap "+term,
             gsrnamespace="6",gsrlimit=str(n),prop="imageinfo",
             iiprop="url|size|extmetadata",iiurlwidth="760"))
    out=[]
    for p in d.get("query",{}).get("pages",[]):
        ii=(p.get("imageinfo") or [{}])[0]
        em=ii.get("extmetadata",{})
        get=lambda k: (em.get(k,{}) or {}).get("value","")
        out.append(dict(title=p["title"], w=ii.get("width"), h=ii.get("height"),
            thumb=ii.get("thumburl"), lic=get("LicenseShortName"),
            author=__import__("re").sub(r"<[^>]+>","",get("Artist"))[:60],
            usage=get("UsageTerms")))
    return out
TERMS=sys.argv[1:]
for t in TERMS:
    print("="*70); print(t)
    for r in search(t):
        print(f"  [{r['lic'] or '?':18s}] {r['w']}x{r['h']}  {r['title'][5:60]}")
        print(f"       by {r['author'] or '(none)'}")
