# -*- coding: utf-8 -*-
"""Fragment + template -> one self-contained page.

Inputs live in src/ (the map fragments and the places list) and in the repo root
(page.tpl.html, pics.json). Output goes to build/, which mksite.py then wraps.
Paths resolve from this file, not the working directory, so it runs from anywhere.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
SRC, BUILD = ROOT/"src", ROOT/"build"
BUILD.mkdir(exist_ok=True)

# compact separators: this is what the published page uses, and at ~1 MB of
# base64 image data the spaces are not free
J = dict(ensure_ascii=False, separators=(",", ":"))

svg, labels = (SRC/"map.frag.html").read_text(encoding="utf-8").split("\n<!--LABELS-->\n")
kyoto, ktri = (SRC/"kyoto.frag.html").read_text(encoding="utf-8").split("\n<!--KTRIANGLE-->\n")
nsvg, nlab = (SRC/"national.frag.html").read_text(encoding="utf-8").split("\n<!--NLABELS-->\n")
places = json.loads((SRC/"places.final.json").read_text(encoding="utf-8"))

KEEP = ("kind", "label", "note", "when", "leg", "status", "sclass", "day", "l", "t", "gmap")
slim = [{k: p[k] for k in KEEP} for p in places]

pics = json.loads((ROOT/"pics.json").read_text(encoding="utf-8"))
PIC = {r["label"]: {"b": r["b64"],
                    "c": "%s / %s, Wikimedia Commons" % (r["author"] or "unknown", r["lic"])}
       for r in pics}
credits = []
for r in pics:
    t = "%s (%s)" % (r["author"] or "unknown", r["lic"])
    if t not in credits: credits.append(t)

out = (ROOT/"page.tpl.html").read_text(encoding="utf-8")
for token, value in (("@@MAP@@", svg),
                     ("@@LABELS@@", labels),
                     ("@@NATIONAL@@", nsvg + "\n" + nlab),
                     ("@@KYOTO@@", kyoto),
                     ("@@KTRIANGLE@@", ktri),
                     ("@@PLACES@@", json.dumps(slim, **J)),
                     ("@@PICS@@", json.dumps(PIC, **J)),
                     ("@@CREDITS@@", "; ".join(credits))):
    assert token in out, "template is missing " + token
    out = out.replace(token, value)

# the page is written as pure ASCII; everything above latin-1 becomes an entity
out = "".join(c if ord(c) < 128 else "&#%d;" % ord(c) for c in out)
assert "@@" not in out, "a placeholder survived"

(BUILD/"kyushu-route.html").write_text(out, encoding="ascii")
print("build/kyushu-route.html", len(out), "chars |", len(slim), "places |", len(PIC), "pictures")
