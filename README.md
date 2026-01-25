# WP5 Speedboat Racer

## Doel

Top-down racing game (“Speedboat Racer”) met:

- Timer linksboven (countdown)
- Positie rechtsboven als 1e/2e/3e/4e/5e
- 4 AI-tegenstanders

Bij time-out (zonder finish) verschijnt: "Game over, dude".

## Innovatie

Boost pickups: verzamel blauwe pickups op de map om ~2 seconden 35% sneller te varen. Tijdens de boost verschijnt “BOOST!” in de HUD.

## Controls

- Gas: W / ↑
- Rem: S / ↓
- Sturen: A / D of ← / →
- Restart game: R

## Installatie & Run (Python + Pygame)

### 1) Clone

- `git clone https://github.com/Dion-1044629/wp5-speedboat-racer.git`
- `cd wp5-speedboat-racer`

### 2) Virtual environment + dependencies (Windows)

- `py -m venv .venv`
- `.\.venv\Scripts\activate`
- `pip install -r requirements.txt`

### 3) Run

- `py -m src.main`

## Demo video

[Google Drive demo video](https://drive.google.com/file/d/1sffeVxD6aQyI2ZebcUqHxSKkH7J5bsp5/view?usp=sharing)

**Checklist in demo:**

- Startmoment: 3–2–1–GO! (geen beweging vóór GO)
- HUD: timer linksboven + positie rechtsboven (1e/2e/…)
- Innovatie: boost pickup → “BOOST!” + tijdelijk sneller
- Einde: “Game over, dude” bij time-out (en/of win bij finish als #1)
- Run: `py -m src.main` • Tests: `py -m pytest`
- Geluid: start-geluid bij GO en eind-geluid bij win/game over.”
