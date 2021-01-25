from cocos.actions import Action


class Control(Action):
    def step(self,dt):
        self.target.update(dt)
