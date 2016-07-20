import pygame
import json

pygame.init()
clock = pygame.time.Clock()

class Game:
	running = True
	toggle_render = True
	tick = 0
	screen = None
	
	def init_screen(width, height):
		Game.screen = pygame.display.set_mode((width, height))
		Game.screen.fill((255,255,255))
		pygame.display.update()	
		
	def clear_screen():
		Game.screen.fill((255,255,255))
		pygame.display.update()	
	
	def load_from_file(file, *default):
		#if no data is found, then it will return default instead
		try:
			with open(file,'r') as f:
				return json.load(f)
		except(FileNotFoundError):
			with open(file, 'w') as f:
				return default
		except(ValueError):
			return default
	
	def events():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Game.running = False
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
				if Game.toggle_render == True:
					Game.toggle_render = False
					Game.clear_screen()
				else:
					Game.toggle_render = True
					Game.clear_screen()
			
	def dump_save(file, *data):
		print('Saving To file...')
		with open(file,'w') as file:
			json.dump(data, file, sort_keys=True, indent=1)
		print('Done')
		
	def tick_add(max_fps):
		Game.tick += 1
		if max_fps != None:
			clock.tick(max_fps)