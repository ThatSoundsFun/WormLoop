import pygame
from worm_class import *
from game_class import *
from random import seed
from collections import deque

#config 
save_file = 'wormloop_save.p'
log_file  = 'wormloop-log.txt'
max_fps = 100

unit = 5
random_seed = 0
sunlight_chance = 10	#actual chance is 1 / value
mutation_chance = 1000	#actual chance is 1 / value
starting_pattern = [['north', 400, 400],['south', -10, -10]], deque(['r','r','l','l','l','.','.','.','x']), [0,0,0]

seed(random_seed)
Worm.list, Game.tick = Game.load_from_file(save_file, Worm.list, Game.tick)
Worm.first_init(*starting_pattern)
while Game.running == True:
	Worm.clean_list(log_file)
	Worm.check_collision()
	Worm.start_replication()
	Worm.can_replicate(sunlight_chance)
	for self in Worm.list:
		self.rotate_gene()
		self.move_snake(unit)
		self.change_direction()
		self.mutation(mutation_chance)
		self.display(unit)
		self.age += 1
	Game.tick += 1
	Game.events()
	Game.update_screen(max_fps)

pygame.quit()
Game.dump_save((Worm.list, Game.tick), save_file)
