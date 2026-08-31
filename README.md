# Kyushu Ground Route — 17–20 Nov 2026

A single-page driving plan for Fukuoka → Kurokawa Onsen → Aso → Takachiho → Miyazaki → Kagoshima.

**Live page:** https://hellhoundsx.github.io/kyushu-route/

## What's in it

- An interactive SVG map of Kyushu built from open prefecture geometry, projected to scale — no tile server, no external JS.
- Per-day route filters, hover/tap detail cards, and the three overnight stops marked distinctly.
- Measured driving times for every leg (Google Maps, typical traffic) rather than estimates.
- Booking deadlines that fall before departure, and the candidate stops for extra days.

## Build

The page is generated, not hand-written:

```
python3 mkmap.py      # Japan prefecture GeoJSON -> simplified, projected SVG paths
python3 build.py      # places, routes, markers, labels -> map fragment
python3 assemble.py   # fragment + template -> single self-contained HTML file
```

`index.html` is fully self-contained apart from Google Fonts.
