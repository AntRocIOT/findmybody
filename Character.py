import os
import random
import cProfile
import cocos
import cv2
from cocos.euclid import Vector2
from cocos.sprite import Sprite
import pyglet
import cocos.collision_model as cm
from cocos.text import Label
import cocos.tiles as tiled
from cocos.camera import Camera
from collections import defaultdict
from cocos.layer import Layer, ScrollingManager
from cocos.actions import Hide, Show, MoveBy, CallFunc, Delay, Driver, Move, Repeat, BoundedMove
from pyglet.image import Animation
from pyglet.window import key

from pyglet.window.key import symbol_string
import Main
import Settings
class NavePrincipalDriver(BoundedMove):
    def step(self,dt):
        super().step(dt)
        velocidad = 400
        x = (Settings.keyboard_player[key.D] - Settings.keyboard_player[key.A]) * velocidad
        y = (Settings.keyboard_player[key.W] - Settings.keyboard_player[key.S]) * velocidad
        self.target.velocity = (x,y)
        self.target.update(dt)
class NaveEnemigaMove(Move):
    def step(self, dt):
        super().step(dt)
        velocidad = 50
        self.target.velocity = (0,-velocidad)
        self.target.update(dt)
class MovimientoDispara(Move):
    def step(self, dt):
        super().step(dt)
        velocidad = 300
        if not self.target.is_enemy:
            self.target.velocity = (0,300)
        elif self.target.is_enemy:
            self.target.velocity = (0,-200)
        self.target.update(dt)
NUMERO_ENEMIGOS = 12
class Character(cocos.layer.ScrollableLayer):
    is_event_handler = True

    def __init__(self):
        super().__init__()
        self.sprite_walk = []
        self.sprite_idle = []
        self.sprite_shoot = []
        self.numero_enemigos = 10
        self.disparo = None

        self.alive = 1
        self.zones = 0
        self.velocidad = 200
        self.keys = defaultdict(int)
        self.schedule(self.update)

        #self.schedule_interval(self.dispara_enemic,1.5)
        self.col_man = cm.CollisionManagerBruteForce()
        self.background = cocos.sprite.Sprite('images/background/background.png')
        directorio_personaje_reposo = 'images/character/idle'

        directorio_personaje_disparo = 'images/character/shoot2'
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

        animacioShoot = Animation.from_image_sequence(self.sprite_shoot, 0.02, True)
        animacioIdle = Animation.from_image_sequence(self.sprite_idle, 0.05, True)
        ani = pyglet.resource.animation('images/enemy/nave-dibujo-mas.gif')
        aniNavePrincipal =  pyglet.resource.animation('images/character/idle/nave-giff-nuevo-stilo.gif')
        animacioIdle = Animation.from_image_sequence(self.sprite_idle, 0.05, True)
        self.sprite_idle = NavePrincipal(aniNavePrincipal,animacioShoot,(200,200))
        self.sprite_idle.position = (200,200)
        self.sprite_idle.velocity = (0,0)
        self.sprite_idle.scale = 0.2

        self.sprite_idle.touched = False
        self.stage = Label("Stage +",font_name='Consolas',font_size=18,anchor_x='center',anchor_y='center')
        self.stage.position = (Main.director.get_window_size()[0]/2,Main.director.get_window_size()[1]/2)
        self.press_to_continue = Label("Press 'Space' to continue",font_name='Consolas',font_size=18,anchor_x='center',anchor_y='center')
        self.press_to_continue.position = (Main.director.get_window_size()[0] / 2, Main.director.get_window_size()[1] / 2-30)
        self.nave_enemigas = []
        self.nave_enemiga = EnemyIA(ani,(200,500),animacioShoot)
        self.nave_enemiga2 = EnemyIA(ani, (200, 650), animacioShoot)
        self.nave_enemiga3 = EnemyIA(ani, (200, 800), animacioShoot)
        self.nave_enemiga4 = EnemyIA(ani, (400, 500), animacioShoot)
        self.nave_enemiga5 = EnemyIA(ani, (400, 650), animacioShoot)
        self.nave_enemiga6 = EnemyIA(ani, (400, 800), animacioShoot)
        self.nave_enemiga7 = EnemyIA(ani, (300, 800), animacioShoot)
        self.nave_enemiga8 = EnemyIA(ani, (300, 950), animacioShoot)
        self.nave_enemiga9 = EnemyIA(ani, (300, 1100), animacioShoot)
        self.nave_enemiga10 = EnemyIA(ani, (200, 1250), animacioShoot)
        self.nave_enemiga11 = EnemyIA(ani, (300, 1400), animacioShoot)
        self.nave_enemiga12 = EnemyIA(ani, (400, 1550), animacioShoot)
        self.nave_enemigas.append(self.nave_enemiga)
        self.nave_enemigas.append(self.nave_enemiga2)
        self.nave_enemigas.append(self.nave_enemiga3)
        self.nave_enemigas.append(self.nave_enemiga4)
        self.nave_enemigas.append(self.nave_enemiga5)
        self.nave_enemigas.append(self.nave_enemiga6)
        self.nave_enemigas.append(self.nave_enemiga7)
        self.nave_enemigas.append(self.nave_enemiga8)
        self.nave_enemigas.append(self.nave_enemiga9)
        self.nave_enemigas.append(self.nave_enemiga10)
        self.nave_enemigas.append(self.nave_enemiga11)
        self.nave_enemigas.append(self.nave_enemiga12)
        self.numero_enemigos = 12
        # self.create_enemies()
        self.add(self.sprite_idle)
        self.add(self.stage)
        self.add(self.press_to_continue)
        self.stage_iniated = False
        self.sprite_idle.do(NavePrincipalDriver(Main.director.get_window_size()[0],Main.director.get_window_size()[1]))
        self.schedule_interval(self.sprite_idle.disparar, 0.2)
    def on_key_press(self, sym, dt):
         if Settings.keyboard_player[key.SPACE] and not self.stage_iniated:
            if self.stage is not None and self.press_to_continue is not None:
                self.stage.visible = False
                self.press_to_continue.visible = False
                self.stage_iniated = True
            for enemy in self.nave_enemigas:
                self.add(enemy)
                enemy.do(NaveEnemigaMove())
                self.schedule_interval(enemy.enemigo_disparo, 3)
    def update(self, dt):
        self.col_man.clear()
        self.sprite_idle.cshape.center = self.sprite_idle.position

        for ele in self.children:
            self.col_man.add(ele[1])

            if isinstance(ele[1],EnemyIA):
                ele[1].cshape.center = ele[1].position
                if self.col_man.they_collide(self.sprite_idle,ele[1]):
                        self.sprite_idle.touched = True
            if isinstance(ele[1],Disparo):
                ele[1].cshape.center = ele[1].position
                for ene in self.nave_enemigas:
                    if self.col_man.they_collide(ene,ele[1]) and not ele[1].is_enemy:
                            ene.touched = True
                            ele[1].touched = True
                            self.numero_enemigos -= 1
                if self.col_man.they_collide(self.sprite_idle,ele[1]) and ele[1].is_enemy:
                    self.sprite_idle.touched = True
                    self.unschedule(self.sprite_idle.disparar)
                    ele[1].touched = True

class NavePrincipal(Sprite):

    def __init__(self,image,anim,pos):
        super().__init__(image,pos)
        self.position_initial = pos
        self.scale = 0.4
        self.anim_shoot = anim
        self.velocity = (0,0)
        self.touched = False
        self.cshape = cm.AARectShape(Vector2(*pos),20,20)

    def update(self,dt):
        if not self.touched:
            self.cshape.center = Vector2(*self.position)
        else:
            self.cshape = cm.AARectShape((0,0),0,0)
            self.kill()

    def disparar(self,dt):

        if Settings.keyboard_player[key.SPACE]:
            disparo = Disparo(self.anim_shoot, (self.position[0],self.position[1]+20), False)
            self.parent.add(disparo)
            disparo.do(MovimientoDispara())

class Disparo(Sprite):

    def __init__(self,image,pos,is_enem):
        super().__init__(image,pos)
        self.touched = False
        self.position = pos
        self.is_enemy = is_enem
        self.scale = 0.2
        self.sprite_dis = image
        self.velocity = (0,0)
        self.cshape = cm.AARectShape(Vector2(*pos),2 , 2)

    def update(self, delta_t):
        if not self.is_enemy:
            if not self.touched:
                if self.position[1] >= Main.director.get_window_size()[1]:
                    print("Disparo mort.")
                    self.kill()
            else:
                self.kill()
        elif self.is_enemy:
            if self.position[1] <= 0:
                print("Disparo enemic mort.")
                self.kill()

class EnemyIA(Sprite):

    def __init__(self,image,pos,animShoot):
        super().__init__(image,pos)
        self.position = pos
        self.scale = 0.08
        self.rotation = 180
        self.velocity = (0,0)
        self.touched = False
        self.on_air = False
        posShoot = (self.position[0]/2, self.position[1]/2)
        self.fire = animShoot
        self.fire.velocity = (0, 0)
        self.fire.cshape = cm.AARectShape(Vector2(*posShoot),2,2)
        self.cshape = cm.AARectShape(Vector2(*pos), 20 , 20)

    def update(self,dt):
        if not self.touched:
            if self.position[1] <= 0:
                    print("Ha arribat al limit")
                    self.touched = True
                    self.parent.numero_enemigos -= 1
        else:
            self.cshape = cm.AARectShape((0,0),0,0)
            self.kill()
            
    def enemigo_disparo(self,dt):
        disparo = Disparo(self.fire, (self.position[0], self.position[1] - 30), True)
        if not self.touched:
            self.parent.add(disparo)
            disparo.do(MovimientoDispara())