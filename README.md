# Japan, 17 Nov – 4 Dec 2026 — 17 nights

Kyushu by car (17–20 Nov) and Osaka planned and booked. Kyoto via Nara planned, beds still to book, with an onsen night at Hakone on the way to Tokyo.

| Leg | Dates | Nights | Status |
|---|---|---|---|
| Kyushu, by car | 17–20 Nov | 3 | planned |
| Osaka | 20–24 Nov | 4 | booked |
| Kyoto, via Nara | 24–27 Nov | 3 | planned, beds to book |
| Hakone, onsen | 27–28 Nov | 1 | planned, bed to book |
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

The page is generated, not hand-written. `page.tpl.html` is the source; `index.html` is output.

```
python3 assemble.py   # src/ fragments + page.tpl.html -> build/kyushu-route.html
python3 mksite.py     # wrap that into index.html, which is what Pages serves
```

Those two are all you need for a content change. Edit `page.tpl.html`, run them, done —
never edit `index.html` by hand.

The map generators only need running if the geometry itself changes:

```
python3 mkmap.py          # japan.geojson -> src/kyushu.json
python3 build.py          # src/kyushu.json -> src/map.frag.html, src/places.final.json
python3 mknational.py     # japan.geojson -> src/japan_national.json
python3 build_national.py # src/japan_national.json -> src/national.frag.html
python3 mkkyoto.py        # src/kyoto_wards.geojson -> src/kyoto.frag.html
```

`mkkyoto.py` needs no download: `src/kyoto_wards.geojson` is committed, being only
645 KB &mdash; the eleven wards of Kyoto city from the MLIT N03 administrative boundaries.

`mkmap.py` and `mknational.py` need `src/japan.geojson`, a prefecture-level GeoJSON of
Japan. It is ~10 MB so it is not committed; fetch a Japan admin-level-1 GeoJSON with a
numeric `id` property per prefecture (1-47) and drop it in `src/`.

`index.html` is fully self-contained apart from Google Fonts.
