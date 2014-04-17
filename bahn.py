from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.uix.button import Button


class Boundry(Widget):
    pass

class BounceBall(Widget):
    velocity_x = NumericProperty(randint(-2,2))
    velocity_y = NumericProperty(randint(-2,2))
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class BahnGame(Widget):
#    ball = ObjectProperty(None)
    debug = ObjectProperty(None)
    boundry = ObjectProperty(None)
    def add_ball(self,instance):
	self.add_widget(BounceBall(pos=self.center,velocity_x=randint(-2,2), velocity_y=randint(-2,2)))
    def update(self, dt):
	self.debug.text = str(self.children)

	for bball in self.children:
            if "BounceBall object" in str(bball):

                if bball.top > self.boundry.top or bball.center_y-(bball.top-bball.center_y) < self.boundry.center_y-(self.boundry.top-self.boundry.center_y):
                        bball.velocity_y *= -1
                if bball.right > self.boundry.right or bball.center_x-(bball.right-bball.center_x) < self.boundry.center_x-(self.boundry.right-self.boundry.center_x):
                        bball.velocity_x *= -1
                bball.move()
#	self.ball.move()

class BahnApp(App):
    def build(self):
	game = BahnGame()
	but1 = Button(text='#')
	but1.bind(on_press=game.add_ball)
	game.add_widget(but1)
	Clock.schedule_interval(game.update, 1.0/30.0)
        return game


if __name__ == '__main__':
    BahnApp().run()
