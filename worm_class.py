import pygame
from game_class import *
from copy import copy, deepcopy
from random import randrange

dead_color = (230,230,230)

class Worm:
	list = []
	
	def to_obj(list):
		#converts dictionaries from json to objects
		for dict in list:
			Worm.init(dict)
			
	def first_init(body, gene, color):
		#prevents the worm from initializing again after start
		if len(Worm.list) == 0:
			index = Worm.init({})
			worm = Worm.list[index]
			worm.body           = body
			worm.gene           = gene
			worm.color          = color
			worm.length         = len(body)
			worm.age            = 0
			worm.will_replicate = False
			worm.is_dead        = False
			
	def init(entries):
		#registers the worm to list before actually initializes it
		index = len(Worm.list)
		Worm.list.append(None)
		Worm.list[-1] = Worm(entries)
		return index
			
	def __init__(self, entries):
		self.__dict__ = entries
			
	def clean_list(log_file):
		Worm.list[:] = [worm for worm in Worm.list if worm.is_completely_gone(log_file) == False]
		
	def is_completely_gone(self, log_file):
		if self.is_dead == True and len(self.body) == 0:
			self.write_worm_info(log_file)
			return True
		return False
		
	def write_worm_info(self, log_file):
		#appends info about dying worm to file 
		gene  = self.rotated_marker()
		body  = str(self.length)
		color = '{} {} {}'.format(str(self.color[0]).zfill(3), str(self.color[1]).zfill(3), str(self.color[2]).zfill(3))
		age   = str(self.age)
		tick  = Game.tick
		
		space1 = abs(20 - len(gene))  * ' '
		space2 = abs(5  - len(body))  * ' '
		space3 = abs(15 - len(color)) * ' '
		space4 = abs(10 - len(age))   * ' '
		
		text = 'gene: {}{} length: {}{} color: {}{} age: {}{} tick: {}\n'.format(gene,space1,body,space2,color,space3,age,space4,tick)
		with open(log_file, 'a') as file:
			file.write(text)
				
	def rotated_marker(self):
		#Returns the worms gene in string form with the marker rotated to the end.
		#This is so the same species of worm can easily be identified in the file.
		gene = copy(self.gene)
		while gene[-1] != 'x':
			tmp = gene.pop()
			gene.insert(0,tmp)
		return ''.join(gene).replace('x','') 

	def check_collision(width, height, unit):
		for worm1 in Worm.list:
			if worm1.is_dead == False:
				for worm2 in Worm.list:
					#body[0][1:] is the head of the worm without the direction string
					#body[1:] is the worm excluding head
					
					if worm1.head_to_head(worm2) == True:
						worm1.is_dead = True
						worm2.is_dead = True
						worm1.grey_out(unit)
						worm2.grey_out(unit)
						break
					
					if worm1.head_to_body(worm2) == True:
						worm1.is_dead = True
						worm1.grey_out(unit)
						break
						
				if worm1.head_to_wall(width, height) == True:
					#collision with boundary
					worm1.is_dead = True
					worm1.grey_out(unit)
					
	def head_to_head(self, worm2):
		if self.body[0][1:] == worm2.body[0][1:] and self is not worm2:
			return True
		return False
					
	def head_to_body(self, worm2):
		for segment in worm2.body[1:]:
			if self.body[0][1:] == segment[1:]:
				return True
		return False
		
	def head_to_wall(self, width, height):
		if   self.body[0][1] < 0:
			return True
		elif self.body[0][2] < 0:
			return True 
		elif self.body[0][1] >= width:
			return True
		elif self.body[0][2] >= height:
			return True
		return False
					
	def grey_out(self, unit):
		if Game.toggle_render == True:
			for segment in self.body:
				pygame.draw.rect(Game.screen, dead_color, (segment[1], segment[2], unit, unit))
				pygame.display.update(segment[1], segment[2], unit, unit)
					
	def start_replication():
		for worm1 in Worm.list:
			if worm1.will_replicate == True and worm1.is_dead == False:
				index = Worm.init({'body'          : deepcopy(worm1.body),
								   'gene'          : copy(worm1.gene),
								   'color'         : copy(worm1.color),
								   'length'        : len(worm1.body),
								   'age'           : 0,
								   'is_dead'       : False,
								   'will_replicate': False})
								   
				worm2                = Worm.list[index]
				direction            = worm1.body[0][0]
				worm1.body[0][0]     = Worm.left_turn_table(direction)
				worm2.body[0][0]     = Worm.right_turn_table(direction)
				worm1.age            = 0
				worm1.will_replicate = False
				
	def can_replicate(sunlight_chance):
		for worm1 in Worm.list:
			for worm1_segment in worm1.body:
				if worm1_segment[0] == 'north' and int(randrange(0,sunlight_chance)) == 0 and Worm.can_get_sunlight(worm1_segment) == True:
					worm1.will_replicate = True
					break
					
				
	def can_get_sunlight(worm1_segment):
		#checks if no other worm is blocking this worm segment for sunlight
		for worm2 in Worm.list:
			for worm2_segment in worm2.body:
				if worm1_segment[1] < worm2_segment[1] and worm1_segment[2] == worm2_segment[2]:
					return False
		return True	
			
			
	def move_worm(unit):
		#every single tail must be updated first before the heads
		#todo: maybe move the update part to a seperate function
		for self in Worm.list:
			self.update_tail(unit)
				
		for self in Worm.list:
			if self.is_dead == False:
				self.body.insert(0, self.body[0].copy())
				if self.body[0][0] == 'north':
					self.body[0][2] -= unit
				elif self.body[0][0] == 'south':
					self.body[0][2] += unit
				elif self.body[0][0] == 'west':
					self.body[0][1] -= unit
				elif self.body[0][0] == 'east':
					self.body[0][1] += unit
				self.update_head(unit)
				
			del self.body[-1]

	def update_head(self, unit):
		if Game.toggle_render == True:
			pygame.draw.rect(Game.screen, self.color, (self.body[0][1],self.body[0][2] , unit, unit))
			pygame.display.update(self.body[0][1],self.body[0][2], unit, unit)
		
	def update_tail(self, unit):
		if Game.toggle_render == True:
			pygame.draw.rect(Game.screen, (255,255,255), (self.body[-1][1],self.body[-1][2], unit, unit))
			pygame.display.update(self.body[-1][1],self.body[-1][2], unit, unit)
		
	def change_direction(self):
		if self.is_dead == False and self.will_replicate == False:
			#self.will_replicate must be false or else the worm may change it's direction twice and collide against itself.
			if self.gene[0] == 'l':
				self.body[0][0] = Worm.left_turn_table(self.body[0][0])
			elif self.gene[0] == 'r':
				self.body[0][0] = Worm.right_turn_table(self.body[0][0])
					
	def left_turn_table(direction):
		if direction == 'north':
			return 'west'
		elif direction == 'west':
			return 'south'
		elif direction == 'south':
			return 'east'
		elif direction == 'east':
			return 'north'
		
	def right_turn_table(direction):
		if direction == 'north':
			return 'east'
		elif direction =='east':
			return 'south'
		elif direction == 'south':
			return 'west'
		elif direction == 'west':
			return 'north'
			
	def rotate_gene(self):
		if self.will_replicate == False:
			tmp = self.gene.pop()
			self.gene.insert(0,tmp)
			if self.gene[0] == 'x':
				#'x' is a marker and must be ignored 
				tmp = self.gene.pop()
				self.gene.insert(0,tmp)
	
	def mutation(self, mutation_chance, unit):
		if int(randrange(0,mutation_chance)) == 0:
			type = int(randrange(0,6))
			if type == 0:
				self.mutation_add_turn_gene()
			elif type == 1:
				self.mutation_remove_turn_gene()
			elif type == 2:
				self.mutation_add_forward_gene()
			elif type == 3:
				self.mutation_remove_forward_gene()
			elif type == 4:
				self.mutation_add_body_length()
			elif type == 5:
				self.mutation_remove_body_length(unit)
					
	def mutation_add_turn_gene(self):
		turn_type = int(randrange(0,2))
		if turn_type == 0:
			self.gene.append('l')
		elif turn_type == 1:
			self.gene.append('r')
		self.new_color()
			
	def mutation_remove_turn_gene(self):
		if len(self.gene) > 1:
			for index, gene in enumerate(self.gene):	
				if gene == 'l' or gene == 'r':
					del self.gene[index]
					break
		self.new_color()
				
	def mutation_add_forward_gene(self):
		self.gene.append('.')
				
	def mutation_remove_forward_gene(self):
		if len(self.gene) > 1:
			for index, gene in enumerate(self.gene):	
				if gene == '.':
					del self.gene[index]
					break
	
	def mutation_add_body_length(self):
		self.body.append(['south',-10,-10])
		self.length += 1
		
	def mutation_remove_body_length(self, unit):
		if len(self.body) > 1:
			self.length -= 1
			self.update_tail(unit)
			del self.body[-1]
			
	def new_color(self):
		#Red must not go above 200 or else the worm can become white or light grey which are the colors of the background and dying worms.
		#There are 64 possible colors a worm can be.
		red   = randrange(0,4) * 65
		green = randrange(0,4) * 85
		blue  = randrange(0,4) * 85
		
		self.color = [red, green, blue]
		
	def to_dict():
		#converts objects from Worm.list to dictionaries so it can be dumped to json
		return [worm.__dict__ for worm in Worm.list]
		
	def debug(self):
		print()
	