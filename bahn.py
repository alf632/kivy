from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.uix.button import Button

class Boundry(Widget):
    pass

class Barier(Widget):
    height = NumericProperty(50)
    width = NumericProperty(50)
    tmp=[0,0]
    mode=0
    def on_touch_down(self, touch):
	if abs((Vector(self.center)-touch.pos).x) <= self.width/2 and abs((Vector(self.center)-touch.pos).y) <= self.height/2:
	    self.mode=1
	    self.tmp=touch.pos
	    direction=Vector(self.center)-(touch.pos)
	    print direction
    def on_touch_move(self, touch):
	if self.mode == 1:
	    self.center = touch.pos
    def on_touch_up(self, touch):
	self.mode=0

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
	self.find_neighbours()
	self.debug.text=str(self.children)
	for bball in self.children:
            if "BounceBall object" in str(bball):

		if bball.top > self.boundry.top or bball.center_y-(bball.top-bball.center_y) < self.boundry.center_y-(self.boundry.top-self.boundry.center_y):
		        bball.velocity_y *= -1
		if bball.right > self.boundry.right or bball.center_x-(bball.right-bball.center_x) < self.boundry.center_x-(self.boundry.right-self.boundry.center_x):
		        bball.velocity_x *= -1

		if bball.velocity_x > 3:
			bball.velocity_x = 3
                if bball.velocity_x < -3:
                        bball.velocity_x = -3
                if bball.velocity_y > 3:
                        bball.velocity_y = 3
                if bball.velocity_y < -3:
                        bball.velocity_y = -3

		bball.move()

    def find_neighbours(self):
	for bball in self.children:
	    if "BounceBall object" in str(bball):
		for obball in self.children:
		    if "BounceBall object" in str(obball):
			if str(bball) != str(obball):
			    dist=Vector(bball.center).distance(obball.center)
#			    if dist <= 50:
#                                obballbball = (Vector(bball.pos)-Vector(obball.pos)).normalize()
#				obballbball = Vector(bball.velocity)+obballbball
#				self.debug.text=str(obballbball)
#                                bball.velocity_x=obballbball.x
#                                bball.velocity_y=obballbball.y

			    if dist < 100:
				obballbball = 10* (Vector(bball.pos)-Vector(obball.pos)) #.normalize()
		 		obballbball = Vector(bball.velocity)+(obballbball/(dist*dist))
				self.debug.text=str(obballbball)
				bball.velocity_x=obballbball.x
				bball.velocity_y=obballbball.y

				

class BahnApp(App):
    def build(self):
	game = BahnGame()
	but1 = Button(text='#')
	but1.bind(on_press=game.add_ball)
	game.add_widget(but1)
	Clock.schedule_interval(game.update, 1.0/15.0)
        return game


if __name__ == '__main__':
    BahnApp().run()
