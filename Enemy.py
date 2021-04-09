import os

from cocos.euclid import Vector2
from cocos.layer import Layer
from cocos.sprite import Sprite
import cocos.collision_model as cm

class EnemyLayer(Layer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        self.enemysprite = EnemyIA('images/enemy/Nave1.png')
    def update(self,dt):

class EnemyIA(Sprite):
    def __init__(self,image,pos):
        super().__init__(image,pos)
        self.position = pos
        self.scale = 0.4
        self.rotation = 180
        self.cshape = cm.AARectShape(Vector2(self.position), self.width / 2, self.height / 2
    def update(self,dt):
        self.position = Vector2(self.position + 10,0)