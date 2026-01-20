# OOAD + UML v2 — Speedboat Racer (na evaluatie/refinement)

## Waarom v2?

Na v1 bleek dat `main.py` te veel verantwoordelijkheden had (game state, race rules, ranking, bot update, rendering). In v2 beschrijven we een duidelijkere verdeling volgens SOLID:

- **Single Responsibility**: race-regels en statebeheer uit `main` halen.
- **Testbaarheid**: race rules blijven pure logica.

## Nieuwe/gewijzigde componenten (ontwerp)

### Nieuwe klasse: Race

Verantwoordelijk voor:

- beheren van racers (speler + bots)
- timer, win/lose state
- track progress updates
- ranking/positie berekenen

`main.py` doet dan alleen:

- input lezen
- Race.update(...) aanroepen
- RaceState renderen

### Nieuwe dataklasse: RaceState (optioneel)

Bevat alleen data die rendering nodig heeft:

- posities, angles, speed
- HUD strings (timer/position)
- flags: game_over / won

## UML (v2 tekstueel)

Race

- track: Track
- timer: CountdownTimer
- player: Boat
- bots: list[Boat]
- player_prog: RacerProgress
- bot_progs: list[RacerProgress]
- finish_times: dict[str, float|None]
- won: bool
- game_over: bool

* update(dt, input_state): None
* reset(): None
* position(): int

RaceState (optional)

- timer_text: str
- position_text: str
- won: bool
- game_over: bool

Bestaande klassen blijven:

- Boat, BoatInputState, CountdownTimer
- Track, Checkpoint
- RacerProgress, RacerSnapshot
- ranking functies, bot_decide

Relaties:

- Race 1 -> Track
- Race 1 -> CountdownTimer
- Race 1 -> Boat (player)
- Race 1 -> list[Boat] (bots)
- Race gebruikt Track/update_progress en ranking voor positie.

## Design decisions (v2)

- **Race centraliseert regels**: win/lose en progress/ranking zijn één bron van waarheid.
- **Rendering blijft in main**: voorkomt vermenging van UI en domain logic.
- **Bot AI blijft aparte module**: uitwisselbaar (later complexer zonder Race te wijzigen).

## Wat zou code-refactor v2 zijn? (scope-bewust)

- Introduceer `src/race.py` met bovenstaande velden en methodes.
- `main.py` initialiseert `Race` en handelt alleen input + render af.
- Tests: voeg unit tests toe voor Race win/lose transitions (RUNNING→WON/GAME_OVER).
