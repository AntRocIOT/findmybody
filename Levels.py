from cocos.actions import Bezier
from cocos.layer import ScrollableLayer, ScrollingManager
from cocos.scene import Scene
from cocos.tiles import load, RectMapLayer
import Main
import Layers
from Character import *
class Level(Scene):
    def __init__(self):
        super().__init__()
        fondo_level1 = Layers.Level1()

        self.scroller = ScrollableLayer()
        personaje = Character()
        background = Layers.Level1()
        self.scroller.add(background)
        self.scroller.add(personaje)
        self.add(self.scroller)
        Settings.scroller = self.scroller
