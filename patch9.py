# -*- coding: utf-8 -*-
import re
p="page.tpl.html"; t=open(p,encoding="utf-8").read()
def rep(a,b,l):
    """Whitespace-insensitive replace: any run of whitespace in the anchor
    matches any run in the file, so line-wrap differences cannot break it."""
    global t
    pat=re.compile(r"\s+".join(re.escape(w) for w in a.split()))
    m=pat.search(t)
    assert m,"MISSING: "+l
    t=t[:m.start()]+b+t[m.end():]; print("  ok:",l)
def drop(a,l):
    rep(a,"",l)

# ---- 1. bathroom talk out of display copy (narrow anchors) ----
rep("Only three have a steering wheel in them. From Kyushu onward every bed is en-suite or a whole house — no shared bathrooms. Pick a leg above.",
    "Only three of them have a steering wheel in them. Pick a leg above.", "standfirst")
drop(" Shared bathrooms here, unlike the rest of the trip — that is the nature of a capsule hotel.", "night 0")
rep("<h2>Night 2: Takachiho, en-suite only</h2>", "<h2>Night 2: Takachiho</h2>", "takachiho heading")
rep("What is left needs a phone call, and only a\n    handful of it is en-suite.", "What is left needs a phone call.", "takachiho intro")
rep("The call list, re-ordered by bathroom", "The call list, in the order worth trying", "call list heading")
rep("Bathroom arrangements are as stated on each property’s own page. The grid tracks", "The grid tracks", "call list preamble")
rep('<th scope="col">Bathroom</th>', '', "bathroom column header")
before=len(re.findall(r'<td[^>]*>(?:&#20840;|&#12518;|unstated)',t))
t=re.sub(r'<td(?: style="color:var\(--jade\)")?>(?:&#20840;&#23460;&#12496;&#12473;[^<]*|&#12518;&#12491;&#12483;&#12488;&#12496;&#12473;[^<]*|unstated[^<]*)</td>','',t)
print(f"  ok: bathroom cells removed ({before})")
rep("Its own page says &#20840;&#23460;&#12496;&#12473; — a bath in\n    every room — and it is the one property the association grid marks open for the 18th. Available and en-suite beats\n    big and unknown.",
    "It is the one property the association grid marks open for the 18th, and it clears the room requirement. Solest\n    is the biggest in town at 68 rooms and publishes nothing to the grid, so its status is unknown rather than full —\n    that is the next call.", "imakuni flag")
i=t.index("<b>Yado Kariboshi is out</b>"); j=t.index("</p>",i)+5
t=t[:t.rindex('<p class="flag">',0,i)]+t[j:]; print("  ok: kariboshi flag dropped")
if "<b>Start with Solest.</b>" in t:
    i=t.index("<b>Start with Solest.</b>"); j=t.index("</p>",i)+5
    t=t[:t.rindex('<p class="flag">',0,i)]+t[j:]; print("  ok: solest flag dropped (folded into imakuni)")
else:
    print("  -- solest flag already absent")
rep("Bookable now, all en-suite or whole-house", "Bookable now, without a phone call", "bookable heading")
rep("Run through Booking’s private-bathroom filter, dates and party size already in the links.\n    A whole house counts because the bathroom is yours.",
    "Dates and party size are already in the links.", "bookable preamble")
rep("Quad room, 4 futons. Survives the private-bathroom filter. One room, so the couple shares.",
    "Quad room, 4 futons. One room, so the couple shares.", "iwato setup")
i=t.index("<b>Excluded for shared bathrooms:</b>"); j=t.index("</p>",i)+5
t=t[:t.rindex('<p class="flag">',0,i)]+t[j:]; print("  ok: excluded flag dropped")
rep("through to its own page, where the bathroom arrangement is stated.",
    "through to its own page and phone number.", "grid card")
rep("With private bathroom and a 8+ score required, for two rooms on the 19th,", "With an 8+ score required, for two rooms on the 19th,", "miyazaki intro")
rep(">49 en-suite options for two rooms.", ">49 options for two rooms.", "miyazaki night row")
rep("nothing en-suite is bookable online in the town itself except\n        Guest House Iwato", "the only thing bookable online in the town itself is Guest House\n        Iwato", "unbooked card")

# ---- 2. three separate bedrooms from Osaka onward ----
rep("Four nights, out on the 24th. From here on there is no car — trains, walkable districts, and cities where\n        availability is not the problem.",
    "Four nights, out on the 24th. No car from here on — trains and walkable districts. Three separate bedrooms from\n        here too: one double and two singles, so everyone has their own door.", "osaka night row")
rep("Late November is peak maple season in Kyoto — the one leg where beds get tight.",
    "Late November is peak maple season — the one leg where beds get tight, and three separate bedrooms will be the\n        hard part.", "kyoto night row")
rep("Six nights, the longest stay, flying out on the 4th. Enough time that the choice of district matters more than\n        the hotel.",
    "Six nights, the longest stay, flying out on the 4th. Long enough that the district matters more than the building,\n        and long enough that three separate bedrooms is worth paying for.", "tokyo night row")
rep("Beds for four in two en-suite rooms, a district to base in, and a plan for the days.",
    "Three separate bedrooms &mdash; one double, two singles &mdash; a district to base in, and a plan for the days.", "osaka brief")
rep("Availability is not the constraint in a city this size.",
    "Availability is not the constraint in a city this size; the room split is.", "osaka brief tail")
rep("A regional map of the Osaka&ndash;Nara&ndash;Kyoto triangle, the Nara day on the 24th, and beds.",
    "A regional map of the Osaka&ndash;Nara&ndash;Kyoto triangle, the Nara day on the 24th, and three separate bedrooms.", "kyoto brief")
rep("Six nights means where you sleep matters more than which hotel,",
    "Six nights means the district matters more than the building, three separate bedrooms again,", "tokyo brief")
open(p,"w",encoding="utf-8").write(t); print("\ntemplate written")
