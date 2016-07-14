import pickle
import pygame

pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
background_color = (255,255,255)

class Game:
	running = True
	toggle_render = True
	tick = 0
	
	def load_from_file(file, *default):
		#if no data is found, then it will return default instead
		try:
			with open(file,'rb') as f:
				return pickle.load(f)
		except:
			pass
		return default
	
	def events():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Game.running = False
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				if Game.toggle_render == True:
					Game.toggle_render = False
				else:
					Game.toggle_render = True
			
	def update_screen(max_fps):
		pygame.display.update()	
		screen.fill(background_color)
		if Game.toggle_render == True:
			clock.tick(max_fps)
			
	def dump_save(input, file):
		print('Saving To file...')
		with open(file,'wb') as file:
			pickle.dump(input, file)
		print('Done')