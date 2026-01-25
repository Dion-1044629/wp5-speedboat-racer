# Review follow-up — WP5 Speedboat Racer

Dit document laat zien wat ik heb gedaan met de feedback uit de externe code review.

Bron: docs/EXTERNAL_CODE_REVIEW.md (Alec Rahan, 24-01-2026)

---

## Punt 1 — Scheiding van verantwoordelijkheden (sterk punt)

**Feedback:** De code is logisch opgesplitst (input, AI, track, ranking, timer).  
**Actie:** Geen wijziging nodig. Ik behoud deze structuur.  
**Bewijs:** Bestaande modules blijven ongewijzigd (src/boat_input.py, src/bot_ai.py, src/track.py, src/ranking.py, src/timer.py).

---

## Punt 2 — Gameplay-flow is duidelijk (sterk punt)

**Feedback:** Countdown/GO, timer, positie-indicator, win/game-over flow zijn consistent.  
**Actie:** Geen wijziging nodig. Wel zorg ik dat dit duidelijk zichtbaar is in de demo-video en README-checklist.  
**Bewijs:** README bevat checklist + demo-link (README.md).

---

## Punt 3 — Tests aanwezig (sterk punt)

**Feedback:** Tests voor kernlogica zijn aanwezig en zinvol gekozen.  
**Actie:** Geen wijziging nodig. Tests blijven onderdeel van de oplevering.  
**Bewijs:** `py -m pytest` geeft groen resultaat.

---

## Punt 4 — Magic numbers / constants verspreid (verbeterpunt)

**Feedback:** Veel constants staan verspreid, vooral in main.py.  
**Actie:** DEFERRED (niet doorgevoerd). Reden: project is stabiel en ik wil vlak voor inleveren geen refactor-risico introduceren.  
**Bewijs:** In OOAD/UML v2 staat het voornemen om main te verkleinen / verantwoordelijkheden te verplaatsen (docs/OOAD_UML_V2.md).

---

## Punt 5 — main.py is lang en doet veel (verbeterpunt)

**Feedback:** main.py is monolithisch; splitsen in functies zou beter zijn.  
**Actie:** DEFERRED (niet doorgevoerd). Reden: dit is een grotere refactor en kan bugs geven; de huidige versie werkt en tests zijn groen.  
**Bewijs:** Ontwerp v2 beschrijft hoe dit idealiter wordt opgelost met een Race-klasse (docs/OOAD_UML_V2.md).

---

## Punt 6 — Innovatie documenteren (verbeterpunt)

**Feedback:** Boost is duidelijk, maar documenteer kort het “waarom” en gedrag.  
**Actie:** DOORGEVOERD. Ik heb de innovatie (boost pickups) concreet beschreven in README en in docs.  
**Bewijs:** README.md (Innovatie: factor 1.35, duur ~2s, HUD “BOOST!”). + ontwerpnotities in docs.

---

## Conclusie

De externe review is verwerkt door (1) aantoonbaar te houden wat al goed was (structuur/tests), (2) documentatie van de innovatie te versterken, en (3) grotere refactors bewust uit te stellen om stabiliteit richting inleveren te waarborgen.
