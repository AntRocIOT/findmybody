# This is a sample Python script.
from collections import defaultdict

import subprocess
import cocos
import os,re

import Settings
from Layers import *
from Levels import *
from Character import *
from cocos.scene import Scene
from cocos.menu import *
from cocos.director import director
from pyglet.window import key

def init_director():
    xsize, ysize = get_screen_resolution()
    director.init( caption='', fullscreen=False)
    director.show_FPS = True


def get_screen_resolution():
    cmd = ['xrandr']
    cmd2 = ['grep', '*']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
    p.stdout.close()
    resolution_string, junk = p2.communicate()
    resolution = str(resolution_string.split()[0])
    reso = re.findall(r'\d+',resolution)
    return int(reso[0]),int(reso[1])

class MiMenu(Menu):
    def __init__(self):
        super().__init__("Menu principal")
        resoluciones = ['640x480', '800x600', '1024x768', '1280x720', '1600x900']
        colores = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 200, 200)]
        item1 = ToggleMenuItem('Sonido', self.choose_sound, True)
        item2 = MultipleMenuItem('Resolucion', self.choose_resolution, resoluciones)
        item3 = ColorMenuItem('Color', self.choose_color, colores)
        item4 = EntryMenuItem('Dificultad (1-10):', self.choose_dificulty, '', max_length=2)
        item5 = ImageMenuItem('images/character/idle/Nave2.png', self.on_image_callback)
        item6 = MenuItem('Salir', self.salir)
        self.create_menu([item1, item2, item3, item4, item5, item6])

    def choose_sound(self, b):
        if b:
            sel = 'activado'
        else:
            sel = 'desactivado'
        print('Tu eleccion de audio es: ', sel)

    def choose_resolution(self, valor):
        print('Has elegido la resolución número{}'.format(valor + 1))

    def choose_color(self, valor):
        print('Has elegido el color número'.format(valor + 1))

    def choose_dificulty(self, valor):
        print('Has elegido el nivel de dificultad', valor)

    def on_image_callback(self):
        director.run(escena_2)
        print('Has elegido comenzar el juego')

    def salir(self):
        director.window.close()
        print('Has elegido salir')
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   # size = director.get_window_size()
   init_director()
   escena_1 = Scene(MiMenu())
   escena_2 = Level()
   Settings.init()
   director.show_FPS = True
   keyboard = key.KeyStateHandler()
   Settings.keyboard_player = keyboard
   director.window.push_handlers(keyboard)
   cProfile.run('director.run(escena_1)')
   #director.run(escena_1)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
