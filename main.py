from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import ListProperty, ObjectProperty, StringProperty, BooleanProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
import os

os.environ['RootFolder'] = os.path.dirname(__file__)
os.environ['KvFolder'] = os.path.join(os.environ['RootFolder'], f'kv{os.sep}')

for file in list(os.path.join(os.environ['KvFolder'], i) for i in os.listdir(os.environ['KvFolder']) if 'start_screen' not in i):
	Builder.load_file(file)

class ColorButton(MDBoxLayout):
	position = StringProperty()
	main = ObjectProperty()
	valid = BooleanProperty(True)
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.size_hint = None, None
		self.size = 90, 60

	def on_touch_down(self, touch):
		if self.valid:
			if self.collide_point(touch.x, touch.y):
				self.change_color(self.main.root.ids.resistorBox.children, self.position)
				

	def change_color(self, resistors, position):
		for resistor in resistors:
			if resistor.opacity == 1:
				resistor.ids[position].md_bg_color = self.md_bg_color
				self.main.checkColor(self.md_bg_color, resistor)

class ColorLabel(MDBoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.size_hint = None, None
		self.size = 10, 40
		self.pos_hint = {'center_y': .5}

class FourColorResistor(MDBoxLayout):
	pass

class FourButtonScreen(MDScreen):
	pass

class FiveColorResistor(MDBoxLayout):
	pass

class FiveButtonScreen(MDScreen):
	pass

class SixColorResistor(MDBoxLayout):
	pass

class SixButtonScreen(MDScreen):
	pass



class Main(MDApp):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.colors = {'black':  [[0/255, 0/255, 0/255, 1],        0],
					   'brown':  [[128/255, 43/255, 0/255, 1],     1],
					   'red':    [[255/255, 0/255, 0/255, 1],      2],
					   'orange': [[255/255, 128/255, 0/255, 1],    3],
					   'yellow': [[255/255, 255/255, 0/255, 1],    4],
					   'green':  [[0/255, 255/255, 0/255, 1],      5],
					   'blue':   [[0/255, 0/255, 255/255, 1],      6],
					   'violet': [[255/255, 0/255, 128/255, 1],    7],
					   'gray':   [[128/255, 128/255, 128/255, 1],  8],
					   'white':  [[255/255, 255/255, 255/255, 1],  9],
					   'gold':   [[200/255, 152/255, 30/255, 1],  -1],
					   'silver': [[140/255, 140/255, 140/255, 1], -2]
					  }
	# def on_start(self):
	# 	self.root.ids.resistorBox.add_widget(self.fourcolorresistor)

	def build(self):
		return Builder.load_file('kv/start_screen.kv')

	def getColorValue(self, colorList):
		for color in self.colors.values():
			if colorList == color[0]:
				return color[1]

	def checkColor(self, resistorColor, resistor):
		self.holder = ''
		for color, code in self.colors.items():
			if code[0] == resistorColor:
				toast(color)
		for resistors in resistor.ids.values():
			self.holder += str(self.getColorValue(resistors.md_bg_color))
		if self.root.ids.fourcolorresistor.opacity == 1:
			self.displayValue(self.holder, 4)
		elif self.root.ids.fivecolorresistor.opacity == 1:
			self.displayValue(self.holder, 5)

	def displayValue(self, value, band):
		if band == 4:
			one = value[0]
			two = value[1]
			if value[0:3].isdigit():
				three = value[2]
				if len(value) == 4:
					four = int(value[-1])
				else:
					four = int(value[-2:])
			else:
				three = value[value.index('-'):value.index('-')+2]
				if len(value) == 5:
					four = int(value[-1])
				else:
					four = int(value[-2:])
			result = int(one+two)*(10**int(three))
			
			self.root.ids.result.text = self.format4Result(result)+ 'Ω ± '+ self.formatTolerance(four)
		elif band == 5:
			one = value[0]
			two = value[1]
			three = value[2]
			if value[0:4].isdigit():
				four = value[3]
				if len(value) == 5:
					five = int(value[-1])
				else:
					five = int(value[-2:])
			else:
				four = value[value.index('-'):value.index('-')+2]
				if len(value) == 6:
					five = int(value[-1])
				else:
					five = int(value[-2:])
			result = int(one+two+three)*(10**int(four))
			self.root.ids.result.text = self.format5Result(result)+ 'Ω ± '+ self.formatTolerance(five)

	def format4Result(self, result):
		if 0<=result<=999:
			if str(result).startswith('0'):
				return '%.2f'%result
			else:
				if '.'in str(result):
					return '%.1f'%result
				else:
					return str(result)
		elif 1000<=result<=999999:
			if str(result).endswith('0000'):
				return str(result).strip('0')+'0 K'
			elif str(result).endswith('000'):
				return str(result).strip('0')+' K'
			elif str(result).endswith('00'):
				return str(result)[0]+'.'+str(result)[1]+' K'
		elif 1000000<=result<=999999999:
			if str(result).endswith('0000000'):
				return str(result).strip('0')+'0 M'
			elif str(result).endswith('000000'):
				return str(result).strip('0')+' M'
			elif str(result).endswith('00000'):
				return str(result)[0]+'.'+str(result)[1]+' M'
		elif 1000000000<=result<=999999999999:
			if str(result).endswith('000000000'):
				return str(result).strip('0')+' G'
			elif str(result).endswith('00000000'):
				return str(result)[0]+'.'+str(result)[1]+' G'

	def format5Result(self, result):
		if 0<=result<=999:
			if str(result).startswith('0'):
				if int(result) == 0:
					return str(result)
				else:
					return '%.2f'%result
			else:
				if '.'in str(result):
					return '%.1f'%result
				else:
					return str(result)
		elif 1000<=result<=999999:
			if str(result).endswith('00000'):
				return str(result).strip('0')+'00 K'
			elif str(result).endswith('0000'):
				return str(result).strip('0')+'0 K'
			elif str(result).endswith('000'):
				return str(result).strip('0')+'K'
			elif str(result).endswith('00'):
				if result <= 9999:
					return str(result)[0]+'.'+str(result)[1]+' K'
				else:
					return str(result)[0:2]+'.'+str(result)[2]+' K'
			elif str(result).endswith('0'):
				return str(result)[0]+'.'+str(result)[1]+str(result)[2]+' K'
		elif 1000000<=result<=999999999:
			if str(result).endswith('00000000'):
				return str(result).strip('0')+'00 M'
			elif str(result).endswith('0000000'):
				return str(result).strip('0')+'0 M'
			elif str(result).endswith('000000'):
				return str(result).strip('0')+' M'
			elif str(result).endswith('00000'):
				if result <= 9999999:
					return str(result)[0]+'.'+str(result)[1]+' M'
				else:
					return str(result)[0]+str(result)[1]+'.'+str(result)[2]+' M'
			elif str(result).endswith('0000'):
				return str(result)[0]+'.'+str(result)[1]+str(result)[2]+' M'
		elif 1000000000<=result<=999999999999:
			if str(result).endswith('00000000000'):
				return str(result).strip('0')+'00 G'
			elif str(result).endswith('0000000000'):
				return str(result).strip('0')+'0 G'
			elif str(result).endswith('000000000'):
				return str(result).strip('0')+' G'
			elif str(result).endswith('00000000'):
				if result <= 9999999999:
					return str(result)[0]+'.'+str(result)[1]+' G'
				else:
					return str(result)[0]+str(result)[1]+'.'+str(result)[2]+' G'
			elif str(result).endswith('0000000'):
				return str(result)[0]+'.'+str(result)[1]+str(result)[2]+' G'
			
	def formatTolerance(self, value):
		if value == 1:
			return '1%'
		elif value == 2:
			return '2%'
		#Note There is no value for 4, this is to avert errors fix it
		elif value == 4:
			return '1%'
		#-----------------------------------------------------------#
		elif value == 5:
			return '0.5%'
		elif value == 6:
			return '0.25%'
		elif value == 7:
			return '0.1%'
		elif value == 8:
			return '0.05%'
		elif value == -1:
			return '5%'
		elif value == -2:
			return '10%'
		
	def changeResistor(self, resistor1, *resistors):
		resistor1.opacity = 1
		for resistor in resistors:
			resistor.opacity = 0

if __name__ == '__main__':
	Main().run()