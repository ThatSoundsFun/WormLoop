import pygame
import time
from worm_class import *
from game_class import *
from random import seed

save_file = 'wormloop_save.json'
log_file  = 'wormloop-log.txt'
max_fps = None

starting_config = {
'width'           : 800,
'height'          : 800,
'unit'            : 5,
'sunlight_chance' : 10,
'mutation_chance' : 500,
'random_seed'     : 1
}

starting_worm = [{
'body'          : [['north', 400, 400],['south', -10, -10]],
'gene'          : ['r','r','l','l','l','.','.','.','x'],
'color'         : [0,0,0],
'length'        : 2,
'age'           : 0,
'ancestor'      : '',
'is_dead'       : False,
'will_replicate': False
}]

version, Game.tick, config, json_list = Game.load_from_file(save_file, '1.2', 0, starting_config, starting_worm)

width           = config['width']
height          = config['height']
unit            = config['unit']
sunlight_chance = config['sunlight_chance']
mutation_chance = config['mutation_chance']
random_seed	    = config['random_seed']

Worm.json_init(version, json_list)
Game.screen_init(width, height)
while Game.running == True: 
	update_var = unit, Game.toggle_render, Game.screen	#variables used for updating the screen
	seed(random_seed + Game.tick)
	Worm.clean_list(log_file, Game.tick)
	Worm.loop(Worm.check_collision, width, height, update_var) #takes up about 90% of the overall execution time
	Worm.loop(Worm.start_replication)
	Worm.loop(Worm.can_replicate, sunlight_chance)
	Worm.loop(Worm.update_tail, *update_var)
	for self in Worm.list:
		self.move_worm(unit, update_var)
		self.rotate_gene()
		self.change_direction()
		self.mutation(mutation_chance, update_var)
		self.age += 1
	Game.tick_add(max_fps)
	Game.events(unit)
	
pygame.quit()
Game.dump_save(save_file, '1.2', Game.tick, config, Worm.to_dict())