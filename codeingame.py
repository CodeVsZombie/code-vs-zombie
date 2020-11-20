from typing import List, Optional, Set

import sys
import math


class Behaviour(object):
    def __init__(self, ash: "Ash", zombies: List["Zombie"], humans: List["Human"]):
        self.ash = ash
        self.zombies = zombies
        self.humans = humans


class ReachMostDangerousZombie(Behaviour):

    def __init__(self, ash: "Ash", zombies: List["Zombie"], humans: List["Human"]):
        super().__init__(ash, zombies, humans)

    def reach_most_dangerous_zombie(self):
        most_dangerous_zombies = list(
            filter(lambda h: h != {}, [human.most_dangerous() for human in self.humans])
        )

        killable_zombies = [most_dangerous_zombie for most_dangerous_zombie in most_dangerous_zombies
                            if not (most_dangerous_zombie.turns_to_reach(most_dangerous_zombie.human_target) - self.ash.turns_to_reach(most_dangerous_zombie) < -2)
                            ]

        if len(killable_zombies) > 0:
            print(f"REACH MOST DANGEROUS ZOMBIE", file=sys.stderr, flush=True)
            most_dangerous_zombie = min(killable_zombies,
                                        key=lambda killable_zombie:
                                        killable_zombie.turns_to_reach(killable_zombie.human_target) and
                                        killable_zombie.distance(killable_zombie.human_target),
                                        default=[])
            segment = Segment(most_dangerous_zombie.human_target, most_dangerous_zombie)
            mid_most = segment.midpoint()
            mid_most = Point(mid_most.x + self.ash.RANGE - 1300, mid_most.y + self.ash.RANGE - 1300)
        else:
            print(f"REACH CLOSEST HUMAN", file=sys.stderr, flush=True)
            mid_most = ReachClosestZombieBehaivour(self.ash, self.zombies, self.humans).reach_closest_zombie()  # StayWithClosestHumanBehaivour(self.ash, self.zombies, self.humans).reach_closest_human()  # self.ash

        return mid_most


class StayWithClosestHumanBehaivour(Behaviour):

    def __init__(self, ash: "Ash", zombies: List["Zombie"], humans: List["Human"]):
        super().__init__(ash, zombies, humans)

    def reach_closest_human(self):
        return min(self.humans, key=lambda human: self.ash.distance(human)).point()


class ReachClosestZombieBehaivour(Behaviour):

    def __init__(self, ash: "Ash", zombies: List["Zombie"], humans: List["Human"]):
        super().__init__(ash, zombies, humans)

    def reach_closest_zombie(self):
        return min(self.zombies, key=lambda zombie: self.ash.distance(zombie)).point()


# === Point === ============================================================== #

class Point(object):
    x: int
    y: int

    def __init__(self, x: int, y: int) -> "Point":
        if not isinstance(x, int):
            raise ValueError(f'x must be int, got {type(x)} => {x}')

        if not isinstance(y, int):
            raise ValueError(f'y must be int, got {type(y)} => {y}')

        self.x = round(x)
        self.y = round(y)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"{self.x} {self.y}"

    def __eq__(self, other: "Point") -> bool:
        if not other:
            return False

        return self.x == other.x and self.y == other.y

    def __iter__(self):
        return (self.x, self.y).__iter__()

    def distance(self, other: "Point") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def angle(self, other: "Point") -> float:
        return math.atan2(other.y - self.y, other.x - self.x) * 180 / math.pi

    def point(self):
        return Point(self.x, self.y)

    def line(self, other: "Point") -> "Line":
        return Line.from_points(self, other)

    def segment(self, other: "Point") -> "Segment":
        return Segment(self, other)

    def nearest(self, others: List["Point"]) -> "Point":
        return min(others, key = lambda p: p.distance(self))

    def farest(self, others: List["Point"]) -> "Point":
        return max(others, key = lambda p: p.distance(self))

    def polar(self, angle: float, distance: int) -> "Point":
        x = round(distance * math.cos(math.radians(angle)))
        y = round(distance * math.sin(math.radians(angle)))

        return Point(self.x + (x),
                     self.y + (y))

# === Line === =============================================================== #

class Line(object):
    m: float
    q: float

    def __init__(self, m: float, q: float) -> "Line":
        self.m = m
        self.q = q

    def __str__(self) -> str:
        return f"y = {self.m}x + {self.q}"

    def __repr__(self) -> str:
        return f"Line({self.m}, {self.q})"

    def __eq__(self, other: "Line") -> bool:
        return self.m == other.m and self.q == other.q

    def __contains__(self, point: "Point"):
        if not isinstance(point, Point):
            raise TypeError('can only be done with Point')

        return self.intersect(point)

    @staticmethod
    def from_points(p1: Point, p2: Point) -> "Line":
        if p1 == p2:
            raise ValueError(f'same point {p1}')

        if p1.x == p2.x:
            return Line(m=math.inf, q=p1.x)

        return Line(m=(p1.y - p2.y) / (p1.x - p2.x),
                    q=((p1.x * p2.y) - (p2.x * p1.y)) / (p1.x - p2.x))

    def intersect(self, point: Point) -> bool:
        if self.m == math.inf:
            return -1 < self.q - point.x < 1

        return -1 < point.x * self.m + self.q - point.y < 1

    def parallel(self, other: "Line") -> bool:
        return self.m == other.m

    def perpendicular(self, other: "Line") -> bool:
        if self.m == math.inf:
            return other.m == 0

        if other.m == math.inf:
            return self.m == 0

        return self.m == -other.m


# === Segment === ============================================================ #

class Segment(Line):
    p1: "Point"
    p2: "Point"

    def __init__(self, p1: Point, p2: Point) -> "Segment":
        l = Line.from_points(p1, p2)
        self.p1 = p1
        self.p2 = p2

        self.m = l.m
        self.q = l.q

    def __str__(self) -> str:
        return f"[{self.p1}, {self.p2}]"

    def __repr__(self) -> str:
        return f"Segment({repr(self.p1)}, {repr(self.p2)})"

    def __eq__(self, other: "Segment") -> bool:
        return self.p1 == other.p1 and self.p2 == other.p2

    def __truediv__(self, parts: int) -> List["Segment"]:
        segments: List["Segment"] = []
        current: "Point" = self.p1
        length = self.length() / parts

        for _ in range(parts):
            forward = current.polar(current.angle(self.p2), length)
            segments.append(Segment(current, forward))
            current = forward

        return segments

    def __floordiv__ (self, length: int) -> List["Segment"]:
        segments: List["Segment"] = []
        current: Point = self.p1

        while current.distance(self.p2) >= length:
            forward = current.polar(current.angle(self.p2), length)
            segments.append(Segment(current, forward))
            current = forward

        if current != self.p2:
            segments.append(Segment(current, self.p2))

        return segments

    def __contains__(self, point: "Point"):
        if not isinstance(point, Point):
            raise TypeError('can only be done with Point')

        return self.intersect(point)

    def __iter__(self):
        return (self.p1, self.p2).__iter__()

    """def intersect(self, point: Point) -> bool:
        return (super().intersect(point)
                and min(self.p1.x, self.p2.x) <= point.x <= max(self.p1.x, self.p2.x)
                and min(self.p1.y, self.p2.y) <= point.y <= max(self.p1.y, self.p2.y))"""

    def intersect(self, point: Point) -> bool:
        return round(self.p1.distance(point) + self.p2.distance(point), 1) == round(self.length(), 1)

    def length(self) -> float:
        return self.p1.distance(self.p2)

    def midpoint(self) -> Point:
        return Point(round((self.p1.x + self.p2.x) / 2),
                     round((self.p1.y + self.p2.y) / 2))

# === PointId === ============================================================ #

class PointId(Point):
    id: int

    def __init__(self, id, x, y) -> "PointId":
        super().__init__(x, y)
        self.id = id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id}, {self.x}, {self.y})"

    def __str__(self) -> str:
        return f"{self.id} {self.x} {self.y}"

    def __eq__(self, other: "PointId") -> bool:
        return super().__eq__(other) and self.id == other.id

    def __iter__(self):
        return (self.id, self.x, self.y).__iter__()


# === WalkerMixIn === ======================================================== #
def WalkerMixIn(speed: int, range: int):
    class Walker(object):
        SPEED: int = speed
        RANGE: int = range

        def turns_to_reach(self, other: Point) -> int:
            return math.floor((self.distance(other) - self.RANGE) / self.SPEED)

        def move_to(self, target: Point) -> Point:
            self.x, self.y = self.polar(self.angle(target), self.SPEED)

        def simulate_moves(self, target: Point) -> List[Segment]:
            return Segment(self, target) / self.SPEED

        def converge(self, target: Point, converge: Point) -> Point:
            pass

        def reach(self, point: Point) -> bool:
            return math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2) < self.RANGE

    return Walker


# === Ash === ================================================================ #

class Ash(Point, WalkerMixIn(speed=1000, range=2000)):

    def __hash__(self) -> int:
        return hash('ash')

    def simulate_moves(self, zombie: "Zombie") -> List[Segment]:
        return super().simulate_moves(zombie)

# === Human === ============================================================== #

class Human(PointId):
    # zombies: Set["Zombie"]

    def __init__(self, id, x, y) -> "Human":
        super().__init__(id, x, y)
        self.zombies = []  # set()

    def __str__(self) -> str:
        return f"H {self.id} {self.x} {self.y}"

    def __eq__(self, other: "Human") -> bool:
        return super().__eq__(other) and self.zombies == other.zombies

    def __hash__(self) -> int:
        return hash(f'HUMAN-{self.id}')

    def bind_zombies(self, zombies: List["Zombie"]) -> None:
        for zombie in zombies:
            if zombie.is_attakking(self):
                zombie.human_target = self
                self.zombies.append(zombie)

    def most_dangerous(self):
        return min(self.zombies, key=lambda zombie: zombie.distance(zombie.human_target)) if self.zombies else {}

#    def is_rescuable(self):



# === Zombie === ============================================================= #

class Zombie(PointId, WalkerMixIn(speed=400, range=400)):
    human_target: Optional[Human]
    x_next: int
    y_next: int

    def __init__(self, id, x, y, x_next, y_next, human_target=None) -> "Zombie":
        super().__init__(id, x, y)
        self.human_target = human_target
        self.x_next = x_next
        self.y_next = y_next

    def __repr__(self) -> str:
        if self.human_target:
            return f"Zombie({self.id}, {self.x}, {self.y}, {self.x_next}, {self.y_next}, human_target={repr(self.human_target)})"

        return f"Zombie({self.id}, {self.x}, {self.y}, {self.x_next}, {self.y_next})"

    def __str__(self) -> str:
        return f"Z {self.id} {self.x} {self.y} {self.x_next} {self.y_next}"

    def __eq__(self, other: "Zombie") -> str:
        return (super().__eq__(other)
                and self.x_next == other.x_next
                and self.y_next == other.y_next
                and self.human_target == other.human_target)

    def __iter__(self):
        return (self.id, self.x, self.y, self.x_next, self.y_next).__iter__()

    def __hash__(self) -> int:
        return hash(f'ZOMBIE-{self.id}')

    def next(self) -> Point:
        return Point(self.x_next, self.y_next)

    def is_attakking(self, human: Human) -> bool:
        return self.next() in Segment(self, human)

    def fake_bind(self, human: Human) -> None:
        self.human_target = human

# === GameField === ========================================================== #

class Field(object):
    WIDTH: int = 16000
    HEIGHT: int = 9000

    ash: Ash
    humans: List[Human]
    zombies: List[Zombie]

    def __init__(self, ash: Ash, humans: List[Human], zombies: List[Zombie]) -> "Field":
        self.ash = ash
        self.humans = humans
        self.zombies = zombies
        self.__scan()

    def __repr__(self) -> str:
        return f"Field({repr(self.ash)}, {repr(self.humans)}, {repr(self.zombies)})"

    def __str__(self) -> str:
        return (f"A {str(self.ash)}"
                + '\n'
                + "\n".join([str(human) for human in self.humans])
                + '\n'
                + "\n".join([str(zombie) for zombie in self.zombies]))

    def __eq__(self, other: "Field") -> bool:
        return (self.ash == other.ash
                and self.humans == other.humans
                and self.zombies == other.zombies)

    def __scan(self) -> None:
        for human in self.humans:
            human.bind_zombies(self.zombies)

    def predict(self, ash: Ash) -> "Field":
        pass

# === Game === =============================================================== #

# 1. Zombie move closest (Human | Ash)
# 2. Ash Move
# 3. Ash Kill Zombie < 2000
# 4. Zombie eat if < 400 and get the position


class Prediction(object):
    pass


# === Game === =============================================================== #

class Game(object):

    field: Field
    # predictions: MinMax[Field]

    def __init__(self, ash: Ash, humans: List[Human], zombies: List[Zombie]) -> "Game":
        self.field = Field(ash, humans, zombies)

    def to_simulation(self):
        print(self.field, file=sys.stderr, flush=True)
        return "Copy ^ into .siml file"

    def predict(self):
        """must return a tree with all possible prediction
        """
        pass

    def play(self) -> Point:
        return ReachMostDangerousZombie(self.field.ash, self.field.zombies, self.field.humans).reach_most_dangerous_zombie()


# ============================================================================ #

if __name__ == '__main__':
    while True:
        game = Game(Ash(*[int(i) for i in input().split()]),
                   [Human(*[int(j) for j in input().split()]) for _ in range(int(input()))],
                   [Zombie(*[int(j) for j in input().split()]) for _ in range(int(input()))])

        print(game.play())
        # print(game.to_simulation())
