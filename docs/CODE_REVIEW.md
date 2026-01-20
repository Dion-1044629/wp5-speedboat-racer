# Code review (self-review)

## Context

Dit project is individueel uitgevoerd; er was geen vaste peer/group beschikbaar voor een externe code review. Daarom is een self-review uitgevoerd op basis van de beoordelingscriteria en best practices (OOAD, testbaarheid, scheiding van verantwoordelijkheden).

Reviewer: Dion Stolk (self)  
Datum: \_**\_-\_\_**-2026  
Scope: src/_, tests/_, docs/\*

## Bevindingen (minimaal 6 punten)

1. **Sterk punt — testbare logica:** input/timer/track/ranking zijn los van rendering gehouden en via pytest getest.
2. **Sterk punt — duidelijke modules:** boat, input, track, ranking, bot_ai zijn gescheiden i.p.v. één groot bestand.
3. **Verbeterpunt — consistente imports:** package-style imports (`src.`) moeten overal consistent blijven om `python -m src.main` en tests stabiel te houden.
   - Actie: imports gecontroleerd en consistent gemaakt.
4. **Verbeterpunt — debug output:** debug overlays moesten uit kunnen voor demo/oplevering.
   - Actie: `DEBUG` flag toegevoegd en debug rendering achter deze flag gezet.
5. **Verbeterpunt — ranking fairness:** bij gelijke “finished” status kon de speler ten onrechte #1 worden (stable sort tie).
   - Actie: tie-breaker toegevoegd op basis van `finish_time` + unit test.
6. **Verbeterpunt — gameplay tuning:** besturing voelde “snappy”.
   - Actie: steering tuning via parameters (`steer_rate`/`return_rate`) en balans botsnelheid.

## Opvolging (bewijs via commits)

- Debug flag + opschonen overlays: commit(s) in git history.
- Tie-breaker finish_time + test: commit(s) in git history.
- Steering tuning: commit(s) in git history.
- Docs (OOAD/UML, sprints): commit(s) in git history.

## Reflectie (kort)

De grootste impact zat in het scheiden van domeinlogica en rendering, waardoor testen mogelijk bleef. Daarnaast bleek “ranking” subtiel: zonder expliciete tie-breaker krijg je onbedoeld gedrag. Volgende keer zou ik eerder een `Race`-klasse introduceren om `main` kleiner te houden.
