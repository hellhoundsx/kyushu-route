# -*- coding: utf-8 -*-
"""Wraps the assembled fragment into the page GitHub Pages serves.

assemble.py emits a body fragment with a bare <title>; Pages needs a whole
document. Output is index.html at the repo root, which is what .nojekyll and the
Pages settings point at.
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
frag = (ROOT/"build"/"kyushu-route.html").read_text(encoding="utf-8")

m = re.search(r"<title>(.*?)</title>", frag)
title = m.group(1) if m else "Kyushu Ground Route"
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

out = ROOT/"index.html"
out.write_text(HEAD + frag + "\n</body>\n</html>\n", encoding="ascii")
print("index.html", round(out.stat().st_size/1048576, 2), "MB |", title)
