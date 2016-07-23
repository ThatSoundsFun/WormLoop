import pygame
from copy import copy, deepcopy
from random import randrange

dead_color = (230,230,230)

class Worm:
	list = []
	
	def json_init(version, json_list):
		#initializes worms that was stored from json
		if version == '1.1':
			Worm.list = json_list
			for self in Worm.list:
				self.gene = list(self.gene)	#converts deque to list
				self.ancestor = ''			#ancestor was added in 1.2
		else:
			for dict in json_list:
				Worm.init(dict)
		
	def init(entries):
		#registers the worm to list before actually initializes it
		index = len(Worm.list)
		Worm.list.append(None)
		Worm.list[-1] = Worm(entries)
		return index
			
	def __init__(self, entries):
		self.__dict__ = entries
			
	def clean_list(log_file, tick):
		Worm.list[:] = [worm for worm in Worm.list if worm.is_completely_gone(log_file, tick) == False]
		
	def is_completely_gone(self, log_file, tick):
		if self.is_dead == True and len(self.body) == 0:
			self.write_worm_info(log_file, tick)
			return True
		return False
		
	def write_worm_info(self, log_file, tick):
		#appends info about dying worm to file 
		gene     = self.pretty_print_gene()
		body     = str(self.length)
		color    = '{} {} {}'.format(str(self.color[0]).zfill(3), str(self.color[1]).zfill(3), str(self.color[2]).zfill(3))
		ancestor = self.ancestor
		age      = str(self.age).zfill(3)
		
		space1 = abs(20 - len(gene))     * ' '
		space2 = abs(20 - len(ancestor)) * ' '
		space3 = abs(5  - len(body))     * ' '
		space4 = abs(15 - len(color))    * ' '
		space5 = abs(10 - len(age))      * ' '
		
		text = 'gene: {}{} ancestor: {}{} length: {}{} color: {}{} age: {}{} tick: {}\n'.format(gene,space1,ancestor,space2,body,space3,color,space4,age,space5,tick)
		with open(log_file, 'a') as file:
			file.write(text)
				
	def pretty_print_gene(self):
		#returns the gene in string form and with marker shifted to the end
		gene = copy(self.gene)
		while gene[-1] != 'x':
			tmp = gene.pop()
			gene.insert(0,tmp)
		return ''.join(gene).replace('x','') 
		
	def loop(function, *parameters):
		#modifies a function so that it loops through Worm.list
		for self in Worm.list:
			function(self, *parameters)

	def check_collision(self, width, height, update_var):
		worm1 = self
		if worm1.is_dead == False:
			for worm2 in Worm.list:
				#body[0][1:] is the head of the worm without the direction string
				#body[1:] is the worm excluding head
				
				if worm1.head_to_head(worm2) == True:
					worm1.is_dead = True
					worm2.is_dead = True
					worm1.grey_out(*update_var)
					worm2.grey_out(*update_var)
					break
				
				if worm1.head_to_body(worm2) == True:
					worm1.is_dead = True
					worm1.grey_out(*update_var)
					break
					
			if worm1.head_to_wall(width, height) == True:
				#collision with boundary
				worm1.is_dead = True
				worm1.grey_out(*update_var)
					
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
					
	def grey_out(self, unit, toggle, screen):
		if toggle == True:
			for segment in self.body:
				pygame.draw.rect(screen, dead_color, (segment[1], segment[2], unit, unit))
				pygame.display.update(segment[1], segment[2], unit, unit)
					
	def start_replication(self):
		worm1 = self
		if worm1.will_replicate == True and worm1.is_dead == False:
			index = Worm.init({
			'body'          : deepcopy(worm1.body),
			'gene'          : copy(worm1.gene),
			'color'         : copy(worm1.color),
			'length'        : len(worm1.body),
			'ancestor'      : worm1.ancestor,
			'age'           : 0,
			'is_dead'       : False,
			'will_replicate': False
			})
			worm2                = Worm.list[index]
			direction            = worm1.body[0][0]
			worm1.body[0][0]     = Worm.left_turn_table(direction)
			worm2.body[0][0]     = Worm.right_turn_table(direction)
			worm1.age            = 0
			worm1.will_replicate = False
				
	def can_replicate(self, sunlight_chance):
		worm1 = self
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
			
	def update_tail(self, unit, toggle, screen):
		if toggle == True:
			pygame.draw.rect(screen, (255,255,255), (self.body[-1][1],self.body[-1][2], unit, unit))
			pygame.display.update(self.body[-1][1],self.body[-1][2], unit, unit)
			
	def move_worm(self, unit, update_var):
		#every single tail must be updated first before the heads
		#todo: maybe move the update part to a seperate function
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
			self.update_head(*update_var)
			
		del self.body[-1]

	def update_head(self, unit, toggle, screen):
		if toggle == True:
			pygame.draw.rect(screen, self.color, (self.body[0][1],self.body[0][2] , unit, unit))
			pygame.display.update(self.body[0][1],self.body[0][2], unit, unit)
			
	def rotate_gene(self):
		if self.will_replicate == False:
			tmp = self.gene.pop()
			self.gene.insert(0,tmp)
			if self.gene[0] == 'x':
				#'x' is a marker and must be ignored 
				tmp = self.gene.pop()
				self.gene.insert(0,tmp)
		
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
	
	def mutation(self, mutation_chance, update_var):
		if self.is_dead == False and int(randrange(0,mutation_chance)) == 0:
			type = int(randrange(0,6))
			if type == 0:
				self.ancestor = self.pretty_print_gene()
				self.mutation_add_turn_gene()
				self.new_color()
			elif type == 1:
				self.ancestor = self.pretty_print_gene()
				self.mutation_remove_turn_gene()
				self.new_color()
			elif type == 2:
				self.mutation_add_forward_gene()
			elif type == 3:
				self.mutation_remove_forward_gene()
			elif type == 4:
				self.mutation_add_body_length()
			elif type == 5:
				self.update_tail(*update_var)
				self.mutation_remove_body_length()
					
	def mutation_add_turn_gene(self):
		turn_type = int(randrange(0,2))
		if turn_type == 0:
			self.gene.append('l')
		elif turn_type == 1:
			self.gene.append('r')
			
	def mutation_remove_turn_gene(self):
		if len(self.gene) > 1:
			for index, gene in enumerate(self.gene):	
				if gene == 'l' or gene == 'r':
					del self.gene[index]
					break
				
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
		
	def mutation_remove_body_length(self):
		if len(self.body) > 1:
			self.length -= 1
			del self.body[-1]
				
	def new_color(self):
		#One of the colors must not go above 200 or else the worm can become white or light grey which are the colors of the background and dying worms.
		#Red was chosen because the human eye can see more shades red then the other 2 colors.
		#There are 64 possible colors a worm can be.
		red   = randrange(0,4) * 65
		green = randrange(0,4) * 85
		blue  = randrange(0,4) * 85
		
		self.color = [red, green, blue]
		
	def at_click_location(click_pos, unit):
		for self in Worm.list:
			for segment in self.body:
				#checks if worm is at a 2 * 2 square with the mouse_pos at the center
				#if any of the if statements are true, then the worm is not in the square
				if click_pos[0] + unit < segment[1]:
					continue
				if click_pos[0] - unit > segment[1] + unit:
					continue
				if click_pos[1] + unit < segment[2]:
					continue
				if click_pos[1] - unit > segment[2] + unit:
					continue
				else:
					return 'gene: {} length:{}'.format(self.pretty_print_gene(), self.length)
		return 'Nothing Here'
		
	def to_dict():
		#converts objects from Worm.list to dictionaries so it can be dumped to json
		return [worm.__dict__ for worm in Worm.list]
		
	def debug(self):
		print()
	