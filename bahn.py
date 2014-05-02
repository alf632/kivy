from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.uix.button import Button
from kivy.graphics import Ellipse, Color, Line
from kivy.uix.scatter import Scatter

select_lock = False

class Boundry(Widget):
    pass

class Barier(Widget):
    height = NumericProperty(100)
    width = NumericProperty(100)
    offset = NumericProperty(20)
    tmp=[0,0]
    mode=0 # mode 0: scale ; else: reposition
    selected = False

    def on_touch_down(self, touch):
	global select_lock
	if select_lock == False:
	    if abs((Vector(self.center)-touch.pos).x) <= self.width/2 and abs((Vector(self.center)-touch.pos).y) <= self.height/2:
		self.selected=True
		select_lock=True
		self.tmp=touch.pos
		direction=Vector(self.center)-(touch.pos)
		if abs(direction.y) < self.height/4 and abs(direction.x) < self.width/4: #wenn touch im widget-randbereich
		    self.mode=1

    def on_touch_move(self, touch):
        if self.selected==True:
	    if self.mode == 0:
	        direction=Vector(self.center)-(touch.pos)
	        if direction.y <= -self.height/4+20: # oben
	            self.height=self.height + (Vector(touch.pos)-(self.tmp)).y
	        if direction.y >= self.height/4-20: # unten
	    	    self.height=self.height - (Vector(touch.pos)-(self.tmp)).y
	    	    self.y = self.y + (Vector(touch.pos)-(self.tmp)).y
	        if direction.x <= -self.width/4+20: # rechts
	            self.width=self.width + (Vector(touch.pos)-(self.tmp)).x
	        if direction.x >= self.width/4-20: # links
	            self.width=self.width - (Vector(touch.pos)-(self.tmp)).x
	    	    self.x = self.x + (Vector(touch.pos)-(self.tmp)).x
	    	self.tmp=touch.pos
	    else:
		    self.center=touch.pos

    def on_touch_up(self, touch):
	self.mode = 0
	self.selected=False
	global select_lock
	select_lock=False

class BounceBall(Widget):
    radius = NumericProperty(20)
    velocity_x = NumericProperty(randint(-2,2))
    velocity_y = NumericProperty(randint(-2,2))
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class BahnGame(Widget):
#    ball = ObjectProperty(None)
    debug = ObjectProperty(None)
    boundry = ObjectProperty(None)
    Dimention =  NumericProperty(20)
    def add_ball(self,instance):
	self.add_widget(BounceBall(pos=self.center,velocity_x=randint(-2,2), velocity_y=randint(-2,2), radius=self.Dimention))
    def add_barier(self,instance):
	self.add_widget(Barier(pos = (100, 100), offset=self.Dimention))
    def update(self, dt):
	self.keep_distance()
	self.mind_barier()
	for bball in self.children:
            if "BounceBall object" in str(bball):

		if bball.top > self.boundry.top or bball.center_y-(bball.top-bball.center_y) < self.boundry.center_y-(self.boundry.top-self.boundry.center_y):
		        bball.velocity_y *= -1
		if bball.right > self.boundry.right or bball.center_x-(bball.right-bball.center_x) < self.boundry.center_x-(self.boundry.right-self.boundry.center_x):
		        bball.velocity_x *= -1
		# MAX Speed
		if bball.velocity_x > 3:
			bball.velocity_x = 3
                elif bball.velocity_x < -3:
                        bball.velocity_x = -3
                if bball.velocity_y > 3:
                        bball.velocity_y = 3
                elif bball.velocity_y < -3:
                        bball.velocity_y = -3
		# Faulheit
                if bball.velocity_x > 0:
                        bball.velocity_x -= 0.01
                elif bball.velocity_x < 0:
                        bball.velocity_x += 0.01
                if bball.velocity_y > 0:
                        bball.velocity_y -= 0.01
                elif bball.velocity_y < 0:
                        bball.velocity_y += 0.01

		bball.move()

    def keep_distance(self):
	for bball in self.children:
	    if "BounceBall object" in str(bball):
		for obball in self.children:
		    if "BounceBall object" in str(obball):
			if str(bball) != str(obball):
			    dist=Vector(bball.center).distance(obball.center)

			    if dist < bball.radius*1.5 and dist > 0:
				obballbball = 10* (Vector(bball.pos)-Vector(obball.pos)) #.normalize()
		 		obballbball = Vector(bball.velocity)+(obballbball/(dist*dist))
				bball.velocity_x=obballbball.x
				bball.velocity_y=obballbball.y

    def mind_barier(self):
	for bball in self.children:
	    if "BounceBall object" in str(bball):
		for barier in self.children:
		    if "Barier object" in str(barier):
			if bball.collide_widget(barier):
			    nearest=Vector(barier.center)
			    nearestdist=nearest.distance(bball.center)
			    if barier.height > barier.width:
				for y in range(int(barier.y+barier.offset), int(barier.y+barier.height-barier.offset)):
				    dist = Vector(barier.center_x,y).distance(bball.center)
				    if dist < nearestdist:
					nearest = Vector(barier.center_x,y)
					nearestdist=dist
			    else:
				for x in range(int(barier.x+barier.offset), int(barier.x+barier.width-barier.offset)):
				    dist = Vector(x,barier.center_y).distance(bball.center)
				    if dist < nearestdist:
					nearest = Vector(x,barier.center_y)
					nearestdist=dist
#			    with self.canvas:
#				Color(1, 0, 0)
#				Ellipse(pos=nearest, size=(5,5))
			    barierbball = 20* (Vector(bball.center)-Vector(nearest))
			    if nearestdist==0:
				nearestdist=0.1
			    barierbball = Vector(bball.velocity)+(barierbball/(nearestdist*nearestdist))
#                            with self.canvas:
#                                Line(points=[nearest.x+barierbball.x, nearest.y+barierbball.y , nearest.x, nearest.y], width=1)
			    bball.velocity_x=barierbball.x
			    bball.velocity_y=barierbball.y
    def clean_up(self,instance):
	for widget in self.children:
	    if "BounceBall object" in str(widget) or "Barier object" in str(widget):
		self.remove_widget(widget)

class BahnApp(App):
    def build(self):
	game = BahnGame()
	but1 = Button(text='add Ball', size=(100,100), pos=(0,0))
	but2 = Button(text='add Barier', size=(100,100), pos=(100,0))
	but3 = Button(text='delete', size=(100,100), pos=(0,100))
	but1.bind(on_press=game.add_ball)
	but2.bind(on_press=game.add_barier)
	but3.bind(on_press=game.clean_up)
	game.add_widget(but1)
	game.add_widget(but2)
	game.add_widget(but3)
	Clock.schedule_interval(game.update, 1.0/15.0)
        return game


if __name__ == '__main__':
    BahnApp().run()
