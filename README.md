# Japan, 17 Nov – 4 Dec 2026 — 17 nights

Kyushu by car (17–20 Nov) planned in full, then Osaka, Kyoto via Nara, and Tokyo recorded as dates awaiting plans.

| Leg | Dates | Nights | Status |
|---|---|---|---|
| Kyushu, by car | 17–20 Nov | 3 | planned |
| Osaka | 20–24 Nov | 4 | TBD |
| Kyoto, via Nara | 24–28 Nov | 4 | TBD |
| Tokyo | 28 Nov – 4 Dec | 6 | TBD |

**Live page:** https://hellhoundsx.github.io/kyushu-route/

Tabbed by leg, deep-linkable: [#trip](https://hellhoundsx.github.io/kyushu-route/#trip) ·
[#kyushu](https://hellhoundsx.github.io/kyushu-route/#kyushu) ·
[#osaka](https://hellhoundsx.github.io/kyushu-route/#osaka) ·
[#kyoto](https://hellhoundsx.github.io/kyushu-route/#kyoto) ·
[#tokyo](https://hellhoundsx.github.io/kyushu-route/#tokyo)

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
