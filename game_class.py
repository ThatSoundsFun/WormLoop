import pygame
import pickle
import json
from worm_class import *

pygame.init()
clock = pygame.time.Clock()

class Game:
	running = True
	toggle_render = True
	screen = None
	
	def screen_init(width, height):
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
		except(ValueError):
			return Game.load_old(file, default)
		except(FileNotFoundError):
			with open(file, 'w') as f:
				return default
			
	def load_old(file, default):
		try:
			with open(file, 'rb') as f:
				obj_list, tick = pickle.load(f)
				Game.convert_warning()
				config = default[2]
				return '1.1', tick, config, obj_list
		except:
			Game.corrupt_file_warning()
			return default
			
	def corrupt_file_warning():
		print('WARNING: Save File Is Corrupted.')
		print('If You Continue, This File Will Get Overwritten When You Quit.')
		print('Press Enter To Continue:')
		input()
		
	def convert_warning():
		print('WARNING: The Length Of All Worms Will Get Adjusted To Equal Their Gene Length.')
		print('Make Sure That The Configs Are The Same And That You Backed Up Your Files')
		print('Are You Sure You Want To Continue?')
		print('Press Enter To Continue:')
		input()
		
	def events(unit):
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
			elif event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				print(Worm.at_click_location(pos, unit))
			
	def dump_save(file, *data):
		print('Saving To file...')
		with open(file,'w') as file:
			json.dump(data, file, sort_keys=True, indent=1)
		print('Done')
		
	def fps(max_fps):
		if max_fps != None:
			clock.tick(max_fps)