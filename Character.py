import os
import random
import cProfile
import cocos
from cocos.euclid import Vector2
from cocos.sprite import Sprite
import pyglet
import cocos.collision_model as cm
import cocos.tiles as tiled
from cocos.camera import Camera
from collections import defaultdict
from cocos.layer import Layer, ScrollingManager
from cocos.actions import Hide, Show, MoveBy, CallFunc, Delay
from pyglet.image import Animation
from pyglet.window import key

from pyglet.window.key import symbol_string
import Main
import Settings


class Character(cocos.layer.ScrollableLayer):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        self.sprite_walk = []
        self.sprite_idle = []
        self.sprite_shoot = []
        self.numero_enemigos = 10
        self.disparo = None
        self.izquierda = False
        self.semaforo = 0
        self.alive = 1
        self.zones = 0
        self.velocidad = 200
        self.keys = defaultdict(int)
        self.schedule(self.update)
        self.schedule_interval(self.on_key_pressed,0.2)
        self.schedule_interval(self.dispara_enemic,1.5)
        self.col_man = cm.CollisionManagerBruteForce()
        self.background = cocos.sprite.Sprite('images/background/background.png')
        directorio_personaje_reposo = 'images/character/idle'
        directorio_personaje_andando = 'images/character/walk'
        directorio_personaje_disparo = 'images/character/shoot2'
        orderelistWalk = sorted(os.listdir('./' + directorio_personaje_andando))
        orderelistIdle = sorted(os.listdir('./' + directorio_personaje_reposo))
        orderelistShoot = sorted(os.listdir('./' + directorio_personaje_disparo))

        # for image in orderelistShoot:
        #     if image.endswith('.png'):
        #         new_image = pyglet.image.load(directorio_personaje_disparo + '/' + image)
        #         #new_image.blit(126, 126)
        #         self.image_shoot = new_image
        for image in orderelistIdle:
            if image.endswith('.png'):
                new_image = pyglet.image.load(directorio_personaje_reposo + '/' + image)
                #new_image.blit(126, 126)
                self.sprite_idle.append(new_image)
        for image in orderelistShoot:
            if image.endswith('.png'):
                new_image = pyglet.image.load(directorio_personaje_disparo + '/' + image)
                #new_image.blit(126, 126)
                self.sprite_shoot.append(new_image)
        self.animacioShoot = Animation.from_image_sequence(self.sprite_shoot, 0.02, True)
        animacioIdle = Animation.from_image_sequence(self.sprite_idle, 0.05, True)
        self.sprite_idle = NavePrincipal(animacioIdle, (200, 200))
        self.nave_enemigas = []
        for i in range (self.numero_enemigos):
            self.nave_enemigas.append(EnemyIA('images/enemy/Nave1.png',(random.randint(0,1200),random.randint(0,700)),self.animacioShoot))
        for ele in self.nave_enemigas:
            self.add(ele)
        self.add(self.sprite_idle)

            #self.sprite_walk.do(action=Hide())
        #self.add(self.sprite_walk)
    def on_close(self):
        self.alive = 0

    def on_key_press(self, sym, dt):
        self.keys[sym] = 1
    def on_key_pressed(self,dt):
        if self.keys[key.SPACE] and not self.sprite_idle.touched:
            posShoot = (self.sprite_idle.position[0], self.sprite_idle.position[1] + 70)
            #  self.disparo = Disparo(self.animacioShoot, posShoot, False)
            self.add(self.disparo)
    def on_key_release(self, sym, sprites):
        self.keys[sym] = 0
    def dispara_enemic(self,dt):
        for nave in self.nave_enemigas:
            posShoot = (nave.position[0], nave.position[1] - 70)
            self.disparo = Disparo(self.animacioShoot, posShoot, True)
            self.add(self.disparo)
    def update(self, dt):
        self.col_man.clear()
        print(Settings.zones)
        for ele in self.children:
            if isinstance(ele[1],Disparo):
                ele[1].update(dt)
                if self.col_man.they_collide(self.sprite_idle,ele[1]) and ele[1].is_enemy:
                        self.sprite_idle.touched = True
                for navee in self.nave_enemigas:
                    if self.col_man.they_collide(navee, ele[1]) and not ele[1].is_enemy:
                        ele[1].touched = True
                        navee.touched = True
                        self.nave_enemigas.remove(navee)
            if isinstance(ele[1],EnemyIA):
                ele[1].update(dt,self.sprite_shoot)
                if self.col_man.they_collide(self.sprite_idle, ele[1]):
                    ele[1].touched = True
                    self.sprite_idle.touched = True

            if isinstance(ele[1],NavePrincipal):
                ele[1].update(dt)
        if not self.sprite_idle.touched :
            x = self.keys[key.D] - self.keys[key.A]
            y = self.keys[key.W] - self.keys[key.S]
            if x != 0 or y != 0:
                posIdle = self.sprite_idle.position
                new_x = posIdle[0] + self.velocidad * x * dt * 2
                new_y = posIdle[1] + self.velocidad * y * dt * 2
                print(new_y,new_x)
                if new_y > 0+150 and new_y <= Main.get_screen_resolution()[1]-50 and new_x > 0 +50and new_x <= Main.get_screen_resolution()[0]-50:
                    self.sprite_idle.position = (new_x, new_y)

class NavePrincipal(Sprite):
    def __init__(self,image,pos):
        super().__init__(image,pos)
        self.position = pos
        self.scale = 0.4
        self.touched = False
        self.cshape = cm.CircleShape(Vector2(*pos),40)
    def update(self,dt):
        if not self.touched:
            self.cshape.center = Vector2(*self.position)
        else:
            self.cshape = cm.CircleShape((0,0),0)
            self.kill()
class Disparo(Sprite):
    def __init__(self,image,pos,is_enem):
        super().__init__(image,pos)
        self.touched = False
        self.is_enemy = is_enem
        self.scale = 0.2
        self.cshape = cm.CircleShape(Vector2(*pos),1)

    def update(self, delta_t):
        if not self.touched:
            if not self.is_enemy:
                move = MoveBy((0,800),1)
                self.do(move)
                self.cshape.center = Vector2(*self.position)
                if self.y > Main.get_screen_resolution()[1] :
                    self.kill()
            elif self.is_enemy:
                move = MoveBy((0, -200), 1)
                self.do(move)
                self.cshape.center = Vector2(*self.position)
                if self.y < 0:
                    self.kill()
        else:

            self.kill()
class EnemyIA(Sprite):
    def __init__(self,image,pos,animShoot):
        super().__init__(image,pos)
        self.position = pos
        self.scale = 0.2
        self.rotation = 180
        self.touched = False
        self.on_air = False
        posShoot = (self.position[0]/2-250, self.position[1]/2)
        self.fire = cocos.sprite.Sprite(animShoot,posShoot,scale=0.2)
        self.fire.cshape = cm.CircleShape(Vector2(*posShoot),4)
        self.cshape = cm.CircleShape(Vector2(*pos), 25)
    def update(self,dt,sprite_disparo):
        if not self.touched:
            self.position = Vector2(self.position[0],self.position[1]-50*dt)
            self.cshape.center = Vector2(*self.position)
            self.fire.position = Vector2(self.fire.position[0], self.fire.position[1] - 800 * dt)
            self.fire.cshape.center = Vector2(*self.fire.position)
            if self.y < 0:
                self.kill()

        else:
            self.cshape = cm.CircleShape((0,0),0)
            self.kill()