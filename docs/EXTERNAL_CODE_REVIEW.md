# Externe code review — WP5 Speedboat Racer

**Reviewer:** Alec Rahan (student, programmeert in Python/C++/Java)  
**Datum:** 24-01-2026  
**Repo:** https://github.com/Dion-1044629/wp5-speedboat-racer

## Feedbackpunten

1. **Goede scheiding van verantwoordelijkheden in de codebase.**  
   Input, AI, track/progress, ranking en timer zijn logisch opgesplitst, waardoor de code beter te volgen is.
   (Bijv. `src/boat_input.py`, `src/bot_ai.py`, `src/track.py`, `src/ranking.py`, `src/timer.py`)

2. **Gameplay-flow is duidelijk en af te vinken volgens de opdracht.**  
   Countdown/GO, timer, positie-indicator en win/game-over flow zijn zichtbaar en consistent geïmplementeerd.
   (Bijv. HUD + state-afhandeling in `src/main.py`)

3. **Tests zijn aanwezig voor kernlogica en lijken zinvol gekozen.**  
   Er zijn tests voor input, timer, track/progress en ranking, wat helpt voor betrouwbaarheid en onderhoud.
   (Bijv. `tests/test_timer.py`, `tests/test_ranking.py`, `tests/test_track.py`, `tests/test_boat_input.py`)

4. **Veel ‘magic numbers’/constants staan verspreid, vooral in `main.py`.**  
   Dit maakt tunen en aanpassen lastiger (screen size, radii, pickup locaties, rates).  
   Suggestie: maak een duidelijk “CONFIG” blok bovenin `main.py` of een apart `config.py`.

5. **`main.py` is vrij lang en doet veel tegelijk (update, draw, audio, powerups).**  
   Dit maakt uitbreiden/refactoren lastiger en vergroot kans op fouten.  
   Suggestie: splits in kleine functies zoals `update_player()`, `update_bots()`, `draw_world()`, `draw_hud()`, `handle_restart()`.

6. **Innovatie (boost pickups) is duidelijk, maar documenteer kort het ‘waarom’ en gedrag.**  
   In README staat het al, maar in docs kan het nog sterker: doel, duur/factor, en waar in code.  
   Suggestie: voeg 3–5 regels toe in je docs/ontwerpnotities over de boost (2s, factor 1.35, HUD “BOOST!”).
