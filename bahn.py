from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

class Boundry(Widget):
    pass

class BounceBall(Widget):
    velocity_x = NumericProperty(1)
    velocity_y = NumericProperty(2)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class BahnGame(Widget):
    ball = ObjectProperty(None)
    debug = ObjectProperty(None)
    boundry = ObjectProperty(None)

    def update(self, dt):
	self.debug.text = str(self.ball.velocity)

	if self.ball.top > self.boundry.top or self.ball.center_y-(self.ball.top-self.ball.center_y) < self.boundry.center_y-(self.boundry.top-self.boundry.center_y):
		self.ball.velocity_y *= -1
	if self.ball.right > self.boundry.right or self.ball.center_x-(self.ball.right-self.ball.center_x) < self.boundry.center_x-(self.boundry.right-self.boundry.center_x):
		self.ball.velocity_x *= -1
	self.ball.move()

class BahnApp(App):
    def build(self):
	game = BahnGame()
	Clock.schedule_interval(game.update, 1.0/30.0)
        return game


if __name__ == '__main__':
    BahnApp().run()
