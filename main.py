import pygame
import time
from worm_class import *
from game_class import *
from random import seed

#config 
save_file = 'wormloop-save-.json'
log_file  = 'wormloop-log-.txt'
max_fps = None

unit = 5
width = 800
height = 800

sunlight_chance = 10	#actual chance is 1 / value
mutation_chance = 1000	#actual chance is 1 / value

random_seed      = 100
starting_pattern = [['north',500,500],['south', -10, -10]], ['l','l','l','r','r','.','.','.','.','x'], [0,0,0]
 
Game.init_screen(width, height)
seed(random_seed)
Game.tick, dict_list = Game.load_from_file(save_file, 0, [])
Worm.to_obj(dict_list)
Worm.first_init(*starting_pattern)
while Game.running == True:
	Worm.clean_list(log_file)
	Worm.check_collision(width, height, unit) #takes up about 90% of the overall execution time
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
Game.dump_save(save_file, Game.tick, Worm.to_dict())