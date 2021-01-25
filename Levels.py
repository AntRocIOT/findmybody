from cocos.actions import Bezier
from cocos.layer import ScrollableLayer, ScrollingManager
from cocos.scene import Scene
from cocos.tiles import load, RectMapLayer
import Main
import Layers
from Character import *
from Control import *
class Level(Scene):
    def __init__(self):
        super().__init__()
        fondo_level1 = Layers.Level1()

        #bg = load("mapas/juego_naves.tmx")
        #self.layer = bg["fondo"]
        #print (self.layer)
        #self.layer2 = bg["estrellas"]
        #self.layer3 = bg["estrellas_2"]
        self.scroller = ScrollableLayer()
        #self.scroller.add(layer)
        #self.scroll_layer = ScrollableLayer()
        personaje = Character()
        background = Layers.Level1()
        #self.scroller.add(self.layer)
        #self.scroller.add(self.layer2)
        #self.scroller.add(self.layer3)
        self.scroller.add(background)
        self.scroller.add(personaje)
        initialPos = (0,0)
        # for eleMap in self.scroller.children:
        #     if isinstance(eleMap[1],RectMapLayer):
        #         if eleMap[1].position[1] < Main.director.get_window_size()[1]:
        #             eleMap[1].position = ()
        #         elif eleMap[1].position[1] >= Main.director.get_window_size()[1]:
        #             eleMap[1].position = initialPos
        self.add(self.scroller)
        Settings.scroller = self.scroller
        #self.add

