from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

class BounceBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class BahnGame(Widget):
    ball = ObjectProperty(None)
    debug = ObjectProperty(None)

    def update(self, dt):
	self.ball.move()
	self.debug.text = str(self.collide_widget(self.ball))

class BahnApp(App):
    def build(self):
	game = BahnGame()
	Clock.schedule_interval(game.update, 1.0/60.0)
        return game


if __name__ == '__main__':
    BahnApp().run()
