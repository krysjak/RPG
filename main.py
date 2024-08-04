import pydoc
from ursina import *
"""
A Test Python 2D pixel art game.
Modules:
    buildozer - using to export to android and ios(Note: Only works on Mac/Linux) git: https://github.com/kivy/buildozer
    ursina - as the main game engine
command:
    pydoc -w main
    pydoc -p 1234
    pip freeze > requirements.txt
"""

app = Ursina()

cube = Entity(model='cube', color=hsv(300,1,1), scale=2, collider='box')

def spin():
    cube.animate('rotation_y', cube.rotation_y+10, duration=1, curve=curve.in_out_expo)

cube.on_click = spin
EditorCamera()  # add camera controls for orbiting and moving the camera

app.run()
pydoc.writedoc('main')