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
        self.schedule(self.update)
        self.level1 = Level1Background('mapas/space.png',(600,0))
        self.level1_scroll = Level1Background('mapas/space.png',(600,Main.get_screen_resolution()[1]))
        self.add(self.level1).add(self.level1_scroll)
    def update(self,dt):
        for ele in self.children:
            if isinstance(ele[1],Level1Background):
                ele[1].update(dt)
class Level1Background(Sprite):
    def __init__(self,image,pos):
        super().__init__(image,pos)
        self.position = pos
        self.image2 = image


    def update(self,dt):
        self.position = (self.position[0],self.position[1]-400*dt)
        if self.position[1] <= -Main.get_screen_resolution()[1]/2:
            self.position = (600,Main.get_screen_resolution()[1]+280)
            Settings.zones +=1