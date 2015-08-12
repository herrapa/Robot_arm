import sys
import serial
import threading
import time
import struct
import pygame

#main class for interfacing with the arm
class ControllerMain(object):
	def __init__(self):
		self.updateInterval = 50
		self.arduino = None
		self.basePos = 1375
		self.shoulderPos = 1500
		self.elbowPos = 1200
		pygame.init()
		pygame.joystick.init()


	def setup(self):
		port = "COM6"
		baud = 115200
		joystickNr = 0
		if len(sys.argv) == 3:
			port = sys.argv[1]
			baud = sys.argv[2]
		else:
			print ("USAGE: 'python controller.py PORT BAUDRATE #Joystick'")
			print ("Using default values: " + port + ", " + str(baud) + ", " + str(joystickNr))
		self.arduino = serial.Serial(port, baud, timeout=0)

		size = (700, 700)
		self.screen = pygame.display.set_mode(size)
		self.done = False
		self.clock = pygame.time.Clock()
		pygame.display.set_caption("Robota")

		self.joystick = pygame.joystick.Joystick(joystickNr)
		self.joystick.init()

		time.sleep(1.5)
		self.mainLoop()

	def mainLoop(self): 
		while not self.done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.done = True
			
			self.update()
			pygame.display.flip()
			self.clock.tick(self.updateInterval)
		
		pygame.quit()

	#update should be overridden in subclass
	def update(self):
		for i in range(4):
			axis = self.joystick.get_axis(i)
			print("Axis {} value: {:>6.3f}".format(i, axis))

		speed = 20

		self.basePos = min(2000, max(800, self.basePos + self.joystick.get_axis(2) * speed))
		self.shoulderPos = min(2150, max(820, self.shoulderPos + self.joystick.get_axis(1) * speed))
		self.elbowPos = min(2200, max(830, self.elbowPos + self.joystick.get_axis(0) * speed))

		self.arduino.write(struct.pack("<HHH", int(self.basePos), int(self.shoulderPos), int(self.elbowPos)))


if __name__ == '__main__':
	controller = ControllerMain()
	controller.setup()