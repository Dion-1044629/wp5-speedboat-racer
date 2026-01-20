# OOAD + UML v1 — Speedboat Racer

## Doel

Een top-down racegame (speedboat) waarin de speler binnen de tijd de finish moet halen en als #1 eindigt. De camera volgt de speler (slechts deel van de track zichtbaar). UI toont timer (links) en positie (rechts).

## Use cases (kort)

1. **Start Race**
   - Speler start + 4 bots startposities.
   - Timer start.
2. **Besturen boot**
   - Speler geeft gas/rem/stuur (ramping input).
   - Boot beweegt met eenvoudige physics.
3. **Racen over track**
   - Checkpoints moeten in volgorde gehaald worden.
   - Progress bepaalt positie/ranking.
4. **Win / Lose**
   - Win: speler finished + positie 1 + tijd over.
   - Lose: timer 00:00 → game over.
   - Reset: R herstart race.

## Domeinmodel (klassen en verantwoordelijkheden)

- **Boat**
  - Houdt positie/hoek/snelheid bij en update beweging op basis van throttle/brake/steer.
- **BoatInputState**
  - Houdt actuele input (throttle/brake/steer) bij.
- **update_input(...)**
  - Ramping/smoothing van input zodat besturing niet “aan/uit” is.
- **CountdownTimer**
  - Aftellen, status (is_done), formattering.
- **Track**
  - Bevat geordende lijst van checkpoints.
- **Checkpoint**
  - Cirkelgebied (x,y,radius) dat in volgorde geraakt moet worden.
- **RacerProgress**
  - Volgt welke checkpoint “next” is + finished status.
- **update_progress(...)**
  - Verhoogt next checkpoint index wanneer racer checkpoint raakt.
- **RacerSnapshot**
  - Snapshot voor ranking (positie + progress + finish_time).
- **rank_racers / position_of**
  - Bepaalt sortering en positie van speler in het veld.
- **bot_decide(...)**
  - Eenvoudige AI die naar de volgende checkpoint stuurt.

## UML (tekstueel klassendiagram)

Boat

- x: float
- y: float
- angle: float
- speed: float
- max_speed, accel, drag, turn_rate, brake_decel

* update(throttle, brake, steer, dt): None

BoatInputState

- throttle: float
- brake: float
- steer: float

CountdownTimer

- total_seconds: float
- remaining: float

* update(dt): None
* is_done: bool
* as_text(): str

Checkpoint

- x: float
- y: float
- radius: float

Track

- checkpoints: list[Checkpoint]

RacerProgress

- next_cp_index: int
- finished: bool

RacerSnapshot

- racer_id: str
- x: float
- y: float
- prog: RacerProgress
- finish_time: float | None

Relaties:

- Track 1..\* -> Checkpoint
- RacerSnapshot 1 -> RacerProgress
- Game loop (main) gebruikt: Boat, BoatInputState, CountdownTimer, Track, RacerProgress, ranking, bot_decide

## Belangrijke ontwerpkeuzes (v1)

- **Scheiding logica vs rendering**: track/progress/ranking/timer zijn pure logica en testbaar met pytest.
- **TDD waar mogelijk**: input, timer, track/progress, ranking zijn met unit tests afgedekt.
- **Eenvoudige AI (waypoint following)** om bots te laten racen zonder zware pathfinding.

## Tests (overzicht)

- tests/test_boat_input.py (input ramping)
- tests/test_timer.py (countdown timer)
- tests/test_track.py (checkpoint progress)
- tests/test_ranking.py (ranking + tie-breaker)
