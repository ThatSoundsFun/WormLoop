import pygame
from worm_class import *
from game_class import *
from random import seed
from collections import deque

#config 
save_file = 'wormloop_save.p'
log_file  = 'wormloop-log.txt'
max_fps = None

unit = 5
width = 800
height = 800

sunlight_chance = 10	#actual chance is 1 / value
mutation_chance = 1000	#actual chance is 1 / value

random_seed = 2
starting_pattern = [['north', 400, 400],['south', -10, -10]], deque(['r','r','l','l','l','.','.','.','x']), [0,0,0]

Game.init_screen(width, height)
seed(random_seed)
Worm.first_init(*starting_pattern)
Worm.list, Game.tick = Game.load_from_file(save_file, Worm.list, Game.tick)
while Game.running == True:
	Worm.clean_list(log_file)
	Worm.check_collision(width, height, unit)
	Worm.start_replication()
	Worm.can_replicate(sunlight_chance)
	Worm.move_worm(unit)
	for self in Worm.list:
		self.rotate_gene()
		self.change_direction()
		self.mutation(mutation_chance, unit)
		self.age += 1
	Game.tick_add(max_fps)
	Game.events()
	
pygame.quit()
Game.dump_save(save_file, Worm.list, Game.tick)