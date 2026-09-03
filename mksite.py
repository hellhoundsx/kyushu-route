# -*- coding: utf-8 -*-
"""Wraps the artifact fragment into a standalone page for GitHub Pages.
The artifact host supplies doctype/head/body; Pages does not."""
import re, shutil, pathlib
frag = open("kyushu-route.html", encoding="utf-8").read()
title = re.search(r"<title>(.*?)</title>", frag)
title = title.group(1) if title else "Kyushu Ground Route"
frag = re.sub(r"<title>.*?</title>\s*", "", frag, count=1)
HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="color-scheme" content="light dark">
<title>%s</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&amp;family=Archivo:wght@400;500;600&amp;family=JetBrains+Mono:wght@400;600&amp;display=swap">
</head>
<body>
""" % title
out = pathlib.Path("site/index.html")
out.write_text(HEAD + frag + "\n</body>\n</html>\n", encoding="utf-8")
for f in ("build.py","build_national.py","assemble.py","page.tpl.html","pics.json","mksite.py"):
    shutil.copy(f, "site/"+f)
print("site/index.html", round(out.stat().st_size/1048576,2), "MB |", title)
