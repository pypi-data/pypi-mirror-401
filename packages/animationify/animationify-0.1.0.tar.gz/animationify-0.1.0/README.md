
# Animationify 🎬

Animationify is a Python library for creating 2D cartoon-style animations
using simple and clean Python code.

## Install
```bash
pip install animationify
```

## Example
```python
from animationify import Scene, Character

scene = Scene()
hero = Character("hero.png", 100, 200)

scene.add(hero)
hero.move_to(400, 200, duration=2)

scene.export("movie.mp4")
```
