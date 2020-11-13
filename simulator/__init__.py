"""Save Humans!

Usage:
	simulator <simulation>

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

from os import kill
from sys import stderr
from typing import Any, Callable, Dict, List, Tuple, Type, Union

from docopt import docopt

from codeingame import Ash, Human, Point, Zombie, Game, Field

import sys
import os

try:
	import pygame
except:
	pass

def main(simulation: str = None, enable_graphics: bool = True):
	if not simulation:
		arguments = docopt(__doc__)
		simulation = arguments['<simulation>']

	ash = None
	humans = []
	zombies = []

	file = os.path.join(os.getcwd(), 'simulations', f'{simulation}.siml')

	if not os.path.exists(file):
		print(f'Simulation {file}.siml does not exists')
		sys.exit(1)

	with open(file) as f:
		for entity in f.read().split('\n'):
			print(f'parsing entity {entity}', entity)

			if entity.startswith('A'):
				ash = Ash(*[int(i) for i in entity.split()[1:]])

			elif entity.startswith('H'):
				humans.append(Human(*[int(i) for i in entity.split()[1:]]))

			elif entity.startswith('Z'):
				zombies.append(Zombie(*[int(i) for i in entity.split()[1:]]))

			else:
				if entity:
					print(f'unparsable entity: {entity}', file=sys.stderr, flush=True)

	if not ash or not humans or not zombies:
		print('missing something')
		print('ash', ash)
		print('humans', humans)
		print('zombies', zombies)
		sys.exit(1)

	return GameController(ash, humans, zombies, graphic_engine=enable_graphics).run_game()

# === GameController === ===================================================== #

BACKGROUND = (255, 255, 255)
TEXT = (0, 0, 0)
ASH = (0, 0, 255)
ASH_RANGE = (255, 255, 0)
HUMAN = (0, 255, 0)
ZOMBIE = (255, 0, 0)
ZOMBIE_RANGE = (0, 255, 255)

def make_interpolater(left_min, left_max, right_min, right_max):
	# Figure out how 'wide' each range is
	left = left_max - left_min
	right = right_max - right_min

	# Compute the scale factor between left and right values
	scale = float(right) / float(left) if left != 0 else float(left)

	# create interpolation function using pre-calculated scaleFactor
	def interp_fn(value):
			return right_min + (value - left_min) * scale

	return interp_fn


def animate(fn):
	def wrapper(game_controller):
		if not game_controller.graphic_engine:
			return fn(game_controller)

		# before = game_controller.entities.copy()
		# retr = fn(game_controller)
		# after = game_controller.entities

		# print('equals', before == after)

		# return retr
		return fn(game_controller)

	return wrapper


class GameController(object):
	ENGINE: Type[Game] = Game

	ash: Ash
	humans: List[Human]
	zombies: List[Zombie]

	TICK: 60

	SCALE: int = 10
	WIDTH: int = int(Field.WIDTH / SCALE)
	HEIGHT: int = int(Field.HEIGHT / SCALE)

	entities: Dict[Union[Ash, Human, Zombie], Tuple[int, int]]
	old_entities: Dict[Union[Ash, Human, Zombie], Tuple[int, int]]

	interpolator_w: Callable
	interpolator_h: Callable

	screen: Any
	font: Any
	clock: Any

	graphic_engine: bool

	def __init__(self, ash: Ash, humans: List[Human], zombies: List[Zombie], graphic_engine: bool = True):
		self.graphic_engine = graphic_engine

		if self.graphic_engine:
			pygame.init()

			self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
			self.clock = pygame.time.Clock()

			self.interpolator_w = make_interpolater(0, Field.WIDTH, 0, self.WIDTH)
			self.interpolator_h = make_interpolater(0, Field.HEIGHT, 0, self.HEIGHT)
			self.entities = {}

			self.font = pygame.font.SysFont(None, 48)


		self.ash = ash
		self.humans = humans
		self.zombies = zombies
		self.score = 0

	def run_game(self):

		if self.graphic_engine:
			self.entities[self.ash] = self.translate(self.ash)

			for human in self.humans:
				self.entities[human] = self.translate(human)

			for zombie in self.zombies:
				self.entities[zombie] = self.translate(zombie)

			print(self.entities)

		while self.humans and self.zombies:
			if self.graphic_engine:
				for event in pygame.event.get():
				# Did the user hit a key?
					if event.type == pygame.constants.KEYDOWN:
						# Was it the Escape key? If so, stop the loop.
						if event.key == pygame.constants.K_ESCAPE:
							break

					# Did the user click the window close button? If so, stop the loop.
					elif event.type == pygame.constants.QUIT:
						break

			self.move_zombies()
			self.ash_move()
			self.ash_attak()
			self.zombie_attak()

			if self.graphic_engine:
				self.update()
				self.clock.tick(1)

		if self.graphic_engine:
			if self.humans:
				text = self.font.render("You Win", True, TEXT)
			# pygame.quit()

			else:
				text = self.font.render("You Lost", True, TEXT)

		else:

			if self.humans:
				# Win
				return True

			else:
				# Lose
				return False

	@animate
	def move_zombies(self):
		for zombie in self.zombies:
			zombie.move_to(zombie.nearest(self.humans + [self.ash]))

			if self.graphic_engine:
				self.entities[zombie] = self.translate(zombie.point())

	@animate
	def ash_move(self):

		try:
			game = self.ENGINE(self.ash, self.humans, self.zombies)
			point = Point(*[int(i) for i in str(game.play()).split()])

		except BaseException as e:
			print(e)
			sys.exit(1)

		self.ash.move_to(point)

		if self.graphic_engine:
			self.entities[self.ash] = self.translate(self.ash.point())

	@animate
	def ash_attak(self):
		kills = [zombie for zombie in self.zombies if self.ash.reach(zombie)]

		if kills:
			for kill in kills:
				self.zombies.remove(kill)

				if self.graphic_engine:
					del self.entities[kill]

	@animate
	def zombie_attak(self):
		for zombie in self.zombies:
			killables = [human for human in self.humans if zombie.reach(human)]

			if killables:
				nearest = zombie.nearest(killables)
				zombie.move_to(nearest)
				self.humans.remove(nearest)

				if self.graphic_engine:
					del self.entities[nearest]

	def update(self):
		self.screen.fill(BACKGROUND)

		for entity, position in self.entities.items():
			if isinstance(entity, Ash):
				pygame.draw.circle(self.screen, ASH_RANGE, position, entity.RANGE / self.SCALE)
				pygame.draw.circle(self.screen, ASH, self.translate(entity), self.SCALE)

			elif isinstance(entity, Human):
				pygame.draw.circle(self.screen, HUMAN, position, self.SCALE)

			elif isinstance(entity, Zombie):
				pygame.draw.circle(self.screen, ZOMBIE_RANGE, position, entity.RANGE / self.SCALE)
				pygame.draw.circle(self.screen, ZOMBIE, position, self.SCALE)

		pygame.display.flip()

	def animate(self, fn):
		pass

	def translate(self, point: Point) -> Tuple[int, int]:
		return (self.interpolator_w(point.x),
						self.interpolator_h(point.y))
