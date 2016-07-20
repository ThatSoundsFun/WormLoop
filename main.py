import pygame
from worm_class import *
from game_class import *
from random import seed

#config 
save_file = 'wormloop-save-.json'
log_file  = 'wormloop-log-.txt'
max_fps = 1

unit = 5
width = 800
height = 800

sunlight_chance = 10	#actual chance is 1 / value
mutation_chance = 1000	#actual chance is 1 / value

random_seed      = 100
starting_pattern = [['north',500,500],['south', -10, -10]], ['l','l','l','r','r','.','.','.','.','x'], [0,0,0]

#end of config
Game.init_screen(width, height)
seed(random_seed)
Game.tick, json_list = Game.load_from_file(save_file, 0, [])
Worm.json_init(json_list)
Worm.first_init(*starting_pattern)
while Game.running == True: 
	update_var = unit, Game.toggle_render, Game.screen	#variables used for updating the screen
	Worm.clean_list(log_file, Game.tick)
	Worm.check_collision(width, height, update_var) #takes up about 90% of the overall execution time
	Worm.start_replication()
	Worm.can_replicate(sunlight_chance)
	Worm.move_worm(unit, update_var)
	for self in Worm.list:
		self.rotate_gene()
		self.change_direction()
		self.mutation(mutation_chance, update_var)
		self.age += 1
	Game.tick_add(max_fps)
	Game.events(unit)
	
pygame.quit()
Game.dump_save(save_file, Game.tick, Worm.to_dict())