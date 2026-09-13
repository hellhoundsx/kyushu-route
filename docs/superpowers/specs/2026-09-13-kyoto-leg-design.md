# Kyoto leg — design

**Date:** 13 September 2026
**Leg:** 3 of 4 — Kyoto, via Nara. 24–28 November 2026, four nights, four travellers.
**Goal:** take the Kyoto tab from a one-card stub to the same finish as the Osaka tab.

---

## 1. Where things stand

Eighteen nights, 16 November to 4 December 2026. Eight are booked: the Narita pods
(Flavio), Kurokawa and Gokase (Maye), Aoshima (Ricardo), and four nights of Osaka
(Ricardo). Ten are not, and all ten are Kyoto and Tokyo.

The Kyoto tab today holds one placeholder day card and a box listing three things the
leg needs: a regional map, the Nara day, and beds. This spec covers all three.

Fixed before we started:

- You leave Osaka on the morning of the 24th and arrive in Tokyo on the 28th.
- No car from Osaka onward. Trains and walking.
- Nara sits between Osaka and Kyoto, so the 24th is a day out, not a transfer.
- Late November is peak maple season — the busiest week of the Kyoto year.
- The four travellers are Ricardo, Daniel, Flavio and Maye. Flavio and Maye are a couple.
- 23 November is Labour Thanksgiving Day. The long weekend therefore **ends** the day
  before you arrive, so three of your four nights are ordinary weekdays.

## 2. What we decided

| Question | Answer |
|---|---|
| How much to build | The full leg, to the same standard as Osaka |
| Where to sleep | Downtown Kyoto. Price **1 double + 1 twin** against **3 rooms** and choose from the numbers |
| The three full days | Four anchors a day, evening illuminations included |
| The 24th | Half a day in Nara, bags sent ahead to the Kyoto hotel. Lockers at Nara station as the fallback |
| The map | A Kyoto city map, plus a small Osaka–Nara–Kyoto triangle map |
| How to build it | Repair the broken build first, then add Kyoto through it |

On rooms: the Osaka leg ruled out "two doubles", because that put Ricardo and Daniel in
one bed. A **twin** is two separate beds, so the two-room option is back on the table and
is expected to be much cheaper. That is why both configurations get priced rather than
one being assumed.

---

## 3. Part A — repair the build

### The problem

`assemble.py`, `mkmap.py`, `mknational.py` and `build_national.py` all read from

```
/private/tmp/claude-502/-Users-ricardo-gomes-Documents-apps-Nexus/0c7e087e-.../scratchpad/
```

a scratchpad belonging to a different project's session. It is gone, and the raw
`japan.geojson` went with it. So the README's three-command build does not run, and
`page.tpl.html` and `index.html` are being kept in step by hand — that is what
`patch9.py` is.

Kyoto is a large content drop and Tokyo is right behind it. Fix this first.

### The fix

1. **Create `src/`** and recover into it the three files `assemble.py` cannot find:
   `map.frag.html` (which contains both the Kyushu map and, after a `<!--LABELS-->`
   marker, its labels), `places.final.json`, and `national.frag.html` (likewise split by
   `<!--NLABELS-->`). `pics.json` and `japan_national.json` are already in the repo and
   stay where they are.

2. **Recover them from `index.html`**, which is the assembled output and therefore holds
   every fill. Each region sits between identifiable markers — the Kyushu map inside the
   Kyushu panel's `.mapwrap`, the national map inside `.nwrap`, the places array in its
   `<script>`. Write a throwaway extraction script, run it once, check the output
   round-trips, then delete the script. It is not part of the build.

3. **Repoint every `S=`** to `src/`, resolved relative to the script's own location, not
   the working directory.

4. **Fix the output paths, which are broken in two more places.** `assemble.py` writes
   `kyushu-route.html` into the scratchpad, but `mksite.py` reads it from the working
   directory — so the two halves of the build do not currently meet. And `mksite.py`
   writes `site/index.html`, while the live page is `index.html` at the repo root and
   there is no `site/` directory. Settle on the root, since that is what GitHub Pages is
   serving and what `.nojekyll` is there for.

5. **Note the missing input.** `mkmap.py` and `mknational.py` need `japan.geojson`, which
   is too large to commit. Add a README line saying where to download it and that those
   two scripts only need running if the geometry changes.

6. **Verify**: `python3 assemble.py && python3 mksite.py` must reproduce the current
   `index.html` before any Kyoto content is added. Byte-for-byte is the target. If it
   differs, every single difference must be understood and deliberately accepted — an
   unexplained difference means the extraction is wrong. This is the gate: do not add
   Kyoto content until the build reproduces the page you already have.

### Acceptance

- `python3 assemble.py && python3 mksite.py` runs from a clean checkout with no manual steps.
- The regenerated `index.html` matches the committed one, before Kyoto is added, with
  any difference explained and accepted rather than ignored.
- `page.tpl.html` is the only file edited by hand from here on.

---

## 4. Part B — the maps

### The Kyoto basin map

**Not a ward map.** Osaka's ward map works because Osaka's districts are its wards — Kita,
Naniwa, Abeno are ward names people use. Kyoto's eleven wards mean nothing to a visitor.
What you navigate by is the river, the hills, and the grid between them.

New `mkkyoto.py` writes `src/kyoto.frag.html`; the template gets a `@@KYOTO@@` placeholder;
`assemble.py` fills it. Same pattern as the existing map scripts, same projection maths
(`dp()` simplification, cosine-latitude projection), same 1000-unit width convention.

On the map:

- The Kamo river running south through the middle, and the Katsura on the west.
- The hills closing the basin east, north and west — the reason the city is the shape it is.
- Rail: Karasuma subway (north–south), Tozai subway (east–west), Keihan up the east bank,
  Hankyu along Shijo, JR Nara line south, JR Sagano line west.
- The hotel as a green marker, in the Osaka map's `olb-bed` idiom.
- Anchors colour-coded by day: east (25th), west and north (26th), south (27th).
- Kyoto Station marked, since the 28th leaves from it.

Reuse the Osaka map's CSS classes and label-anchor system (`olb-l` / `olb-r` and the
percentage positioning) rather than inventing new ones. If the Osaka classes turn out to
be too Osaka-specific, generalise them rather than duplicating.

### The triangle map

Small — roughly a fifth the height of the city map. Osaka, Nara and Kyoto with the rail
lines between them, and the 24th's path drawn across it: Osaka to Nara in the morning,
Nara to Kyoto in the afternoon. It explains one day, so it gets one day's worth of space.

---

## 5. Part C — the four days

Split by geography so you never cross the city twice in a day. In peak week that split is
what saves you.

### 24 November, Tuesday — Osaka to Nara to Kyoto

Bags to the Osaka front desk first thing for forwarding to the Kyoto hotel; roughly
¥2,000 a case, so about ¥8,000 for the four. Confirm the Osaka hotel offers it and what
the cut-off time is. If not, coin lockers at Nara station — but note on the page that the
large lockers fill by mid-morning in high season.

Nara from about 10:00 to 14:00: Nandaimon gate, Todai-ji and the Great Buddha, the deer
park, and Kasuga Taisha's lantern approach if the clock allows. Into Kyoto mid-afternoon,
check in, then an evening illumination.

### 25 November, Wednesday — east, Higashiyama

**Kiyomizu-dera opens at 06:00.** This is the single most valuable fact on the page: in
peak maple week it means the temple in near-silence and Sannenzaka walked before the first
coach parks. Build the day on it.

Then Nanzen-ji and the aqueduct, the Philosopher's Path north to Ginkaku-ji, and Eikan-do
after dark — the best of the light-ups and directly on that line.

### 26 November, Thursday — west, then north

Arashiyama at dawn for the bamboo grove, Tenryu-ji's garden, Togetsukyo bridge. Then north
to Kinkaku-ji and Ryoan-ji. Evening back in town, Pontocho or Gion.

**This is the weakest day** — Arashiyama to Kinkaku-ji is a real cross-city haul. Price
the transfer honestly on the page, and if it reads badly, the alternative is to drop the
northern pair and give Arashiyama the whole day including the Hozugawa river boat or the
Sagano Romantic Train.

### 27 November, Friday — south

Fushimi Inari before sunrise; it is open 24 hours and that is the only sane way to walk
the gates. Then Tofuku-ji, which is the maple temple and will be at its absolute peak that
week. Afternoon deliberately loose: Nijo Castle, Nishiki market, or Uji for tea and
Byodo-in.

**Uji is filler, not an anchor** — present it as one of three afternoon options, not as
the plan.

### 28 November, Saturday — out

Shinkansen to Tokyo, a little over two hours from Kyoto Station. One line on the page, not
a card; the Tokyo leg picks it up.

### The gap to watch

Downtown gets no firm slot in the above — no Nijo Castle, no Imperial Palace, no Nishiki
morning. For a four-anchor pace that may be too thin. The 27th afternoon is where it goes
if it goes anywhere; say so plainly rather than leaving it implied.

---

## 6. Part D — beds

Downtown: the Shijo–Kawaramachi–Karasuma block.

Price both configurations for 24–28 November, four nights, and put them side by side:

- **Two rooms** — one double for Flavio and Maye, one twin for Ricardo and Daniel.
- **Three rooms** — the Osaka split, everyone with their own door except the couple.

For each candidate record: total in euros, per-person split, free-cancellation date,
review score and count, walking distance to Shijo-Kawaramachi, and the link with dates and
occupancy already in the query string — the Osaka booking link is the model.

Recommend from the numbers, not ahead of them. Osaka's €877 for four nights in three rooms
is the reference point; say whether Kyoto comes in above or below it and by how much.

Carry over the two habits the Osaka leg established: state the cancellation date as a chip
on the card, and check whether the price has moved since booking, because that is what
tells you whether the cancellation window is protecting real money.

---

## 7. Part E — the rest of the page

- **Trip table:** the Kyoto row moves off TBD.
- **Where you sleep:** the nights 8–11 card gets the real property, price, who booked it
  and the cancellation date.
- **Masthead and counts:** "Eight are settled … ten still to find" is recalculated.
- **Still open:** the "Kyoto and Tokyo are all that is left" card becomes Tokyo only.
- **National map legend:** "by rail — TBD" no longer describes both rail legs once one is
  planned. Split it or re-word it.

---

## 8. Facts to verify before publishing

Everything in Part C is a candidate until checked against the source. Nothing on this list
goes on the page unverified.

1. Kiyomizu-dera 2026 opening hour and any autumn evening opening.
2. Eikan-do autumn light-up dates and hours for 2026.
3. Kodai-ji and Kiyomizu evening opening dates for 2026 — these decide the 24th's evening.
4. **Tofuku-ji**: whether 2026 peak season uses timed or reserved entry. If it does, that
   is a second booking clock alongside the beds and belongs in the TBD box.
5. **Arashiyama**: whether the Hozugawa river boat and the Sagano Romantic Train need
   booking ahead in peak week.
6. Todai-ji and Kasuga Taisha opening hours in November.
7. Osaka-to-Nara and Nara-to-Kyoto train times, fares and lines — Kintetsu and JR both run
   it and they arrive at different stations in Nara.
8. Whether the Osaka hotel does luggage forwarding, the cut-off time, and the real price.
9. Kyoto to Tokyo shinkansen journey time and fare on the 28th.
10. Sunset time in Kyoto in late November — it drives every "go at dawn" claim.
11. Whether the 2026 Kumamoto earthquake note needs anything for Kansai. Almost certainly
    not, but check rather than assume.

---

## 9. Out of scope

- The Tokyo leg. It gets its own spec.
- Buying anything. This produces a shortlist and a recommendation; the booking is Ricardo's.
- Re-drawing the Kyushu or Osaka maps.
- Any refactor of the page's CSS beyond what the Kyoto map genuinely needs.

## 10. Done when

- The build runs from a clean checkout and regenerates `index.html` from `page.tpl.html`.
- The Kyoto tab carries a basin map, a triangle map, four day cards, a bed comparison with
  real prices and cancellation dates, and a TBD box naming what is still open.
- Every fact in section 8 is checked, and anything that could not be confirmed is marked as
  unconfirmed on the page rather than stated as fact.
- The trip tab's table, night cards, counts and "Still open" section all agree with the
  Kyoto tab.
