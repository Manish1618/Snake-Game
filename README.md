# Snake Game with Python

**Ayush Kumar** · Roll No. 251151004038 · B.Tech CSE, 2nd Year

A classic Snake game written in Python with **pygame** (`snake.py`), plus a browser port
(`index.html`) so it can be played online. The web version is deployed on **Render** as a
static site using `render.yaml`.

## Play
- **Online:** https://snake-game-ayush.onrender.com
- **Desktop (Python):**
  ```bash
  pip install pygame
  python snake.py
  ```

## Controls
| Key | Action |
|---|---|
| Arrow keys / WASD | Move |
| P | Pause / resume |
| R | Restart after game over |
| Esc | Quit (desktop) |

On phones: swipe or use the on-screen pad; tap to pause/restart.

## Features
- 25 × 20 grid, wall and self collision
- Speed rises from 8 to 20 FPS as the score grows (+1 FPS every 3 apples)
- Buffered turns (up to 3) so quick key combos aren't lost
- High score (kept in the browser via `localStorage`)

## Files
| File | Purpose |
|---|---|
| `snake.py` | Original pygame game |
| `index.html` | Browser version (HTML5 canvas + JS) |
| `render.yaml` | Render static-site blueprint |
| `Snake_Game_Report_Ayush_Kumar.pdf` | Project report |
