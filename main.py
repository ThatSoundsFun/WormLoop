import pygame
from worm_class import *
from game_class import *
from random import seed

save_file = 'wormloop-save.json'
log_file  = 'wormloop-log.txt'
max_fps = 1

starting_config = {
'width'           : 600,
'height'          : 600,
'unit'            : 2,
'sunlight_chance' : 10,
'mutation_chance' : 1000,
'random_seed'     : 5
}

starting_worm = [{
'body'          : [['north', 100, 400],['south', -10, -10],['south', -10, -10],['south', -10, -10],['south', -10, -10],['south', -10, -10]],
'gene'          : ['r','l','r','l','l','.','x'],
'color'         : [0,0,0],
'age'           : 0,
'ancestor'      : '',
'is_dead'       : False,
'will_replicate': False
}]

version, tick, config, json_list = Game.load_from_file(save_file, '1.2', 0, starting_config, starting_worm)

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
	seed(random_seed + tick)
	Worm.clean_list(log_file, tick)
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
	tick += 1
	Game.fps(max_fps)
	Game.events(unit)
	
pygame.quit()
Game.dump_save(save_file, '1.2', tick, config, Worm.to_dict())