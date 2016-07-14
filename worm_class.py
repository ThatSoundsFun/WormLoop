import pygame
from game_class import *
from copy import copy, deepcopy
from random import randrange
from collections import deque

dead_color = (240,240,240)

class Worm:
	list = []
	
	def init(body, gene, color):
		#registers the worm to list before actually initializes it
		index = len(Worm.list)
		Worm.list.append(None)
		Worm.list[-1] = Worm(deepcopy(body), copy(gene), copy(color))
		return index
		
	def first_init(*parameters):
		#prevents the worm from initializing again after start
		print(len(Worm.list))
		if len(Worm.list) == 0:
			Worm.init(*parameters)
		
		
	def __init__(self, body, gene, color):
		self.body = body
		self.body_length = len(body)
		self.gene = gene
		self.color = color
		
		self.age = 0
		self.is_dead = False
		self.will_replicate = False
			
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
		body  = str(self.body_length)
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
			gene.rotate(1)
		return ''.join(gene).replace('x','') 

	def check_collision():
		for worm1 in Worm.list:
			for worm2 in Worm.list:
				#body[0][1:] is the head of the worm without the direction string
				#body[1:] is the worm excluding head
				
				for part in worm2.body[1:]:
					if worm1.body[0][1:] == part[1:]:
						#collision with body excluding head
						worm1.is_dead = True
						break
					
				if worm1.body[0][1:] == worm2.body[0][1:] and worm1 is not worm2:
					#collision with head
					worm1.is_dead = True
					
				if worm1.body[0][1] < 0 or worm1.body[0][1] >= width or worm1.body[0][2] < 0 or worm1.body[0][2] >= height:
					#collision with boundary
					worm1.is_dead = True
					
	def start_replication():
		for worm1 in Worm.list:
			if worm1.will_replicate == True and worm1.is_dead == False:
				worm2 = Worm.list[Worm.init(worm1.body, worm1.gene, worm1.color)]
				direction = worm1.body[0][0]
				worm1.body[0][0] = Worm.left_turn_table(direction)
				worm2.body[0][0] = Worm.right_turn_table(direction)
				worm1.age = 0
				worm1.will_replicate = False
				
	def can_replicate(sunlight_chance):
		for worm1 in Worm.list:
			for worm1_part in worm1.body:
				if worm1_part[0] == 'north' and Worm.can_get_sunlight(worm1_part) == True and int(randrange(0,sunlight_chance)) == 0:
					worm1.will_replicate = True
					break
				
	def can_get_sunlight(worm1_part):
		for worm2 in Worm.list:
			for worm2_part in worm2.body:
				if worm1_part[1] < worm2_part[1] and worm1_part[2] == worm2_part[2]:

					return False
		return True	
		
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
			self.gene.rotate(1)
			if self.gene[0] == 'x':
				self.gene.rotate(1)
		
	def move_snake(self, unit):
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
				
		del self.body[-1]
					
	def mutation(self, mutation_chance):
		if int(randrange(0,1000)) == 0:
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
				self.mutation_remove_body_length()
					
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
		self.body_length += 1
		
	def mutation_remove_body_length(self):
		if len(self.body) > 1:
			self.body_length -= 1
			del self.body[-1]
			
	def new_color(self):
		color = bin(randrange(0,63)).replace('0b', '').zfill(6)
		
		red   = color[0:2]
		green = color[2:4]
		blue  = color[4:6]
		
		#red must not go above 200 or else the worm can become white or light grey which are the colors of the background and dying worms
		red   = int(red,2)  * 60	
		green = int(blue,2) * 80
		blue  = int(blue,2) * 80
		
		self.color = [red, green, blue]
				
		if all([c >= 200 for c in self.color]) == True:
			#this prevents the worm from becoming white or light grey, which the background and dead worm uses.
			self.color = [150,150,150]
			self.new_color()
			
			
	def display(self, unit):
		if Game.toggle_render == True:
			if self.is_dead == False:
				#colors it normally if it didn't die.
				for part in self.body:
					pygame.draw.rect(screen, self.color, [part[1], part[2], unit, unit])
			else:
				#colors it gray if it did die.
				for part in self.body:
					pygame.draw.rect(screen, dead_color, [part[1], part[2], unit, unit])
					
	def debug(self):
		print(self.body)
	