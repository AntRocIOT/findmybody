from cocos.actions import Move, Repeat, MoveBy

import Main
from cocos.layer import ScrollableLayer
from cocos.sprite import Sprite

import Settings
from Levels import Level
from Character import Character


class Level1(ScrollableLayer):
    is_event_handler = True

    def __init__(self):
        super().__init__()

        SCROLLING_SPEED = 100
        self.level1 = Level1Background('images/background/fondo_naves.png',(300,0))
        self.level1_scroll = Level1Background('images/background/capa_velocidad.png',(Main.director.get_window_size()[0]/2,600))
        self.level1_scroll.scale = 0.1
        #self.add(self.level1)
        self.add(self.level1_scroll)
        #self.level1.do(Repeat(MoveBy((0,-400),500/150)+MoveBy((0,400),0)))
        self.level1_scroll.do(Repeat(MoveBy((0,-800),1)+MoveBy((0,800),0)))
        #self.level1_scroll.do(LevelBackGroundInfinite())
class Level1Background(Sprite):
    def __init__(self,image,pos):
        super().__init__(image,pos)
        self.position = pos
        self.image2 = image
        self.scale = 0.3
        self.velocity = (0,0)

