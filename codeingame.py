from typing import List, Optional, Set

import math

# === Point === ============================================================== #

class Point(object):
    x: float
    y: float

    def __init__(self, x: int, y: int) -> "Point":
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"{round(self.x)} {round(self.y)}"

    def __eq__(self, other: "Point") -> bool:
        if not other:
            return False

        return self.x == other.x and self.y == other.y

    def distance(self, other: "Point") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def angle(self, other: "Point") -> float:
        return math.atan2(other.y - self.y, other.x - self.x) * 180 / math.pi

    def line(self, other: "Point") -> "Line":
        return Line.from_points(self, other)

    def segment(self, other: "Point") -> "Segment":
        return Segment(self, other)

    def nearest(self, others: List["Point"]) -> "Point":
        return min(others, key = lambda p: p.distance(self))

    def farest(self, others: List["Point"]) -> "Point":
        return max(others, key = lambda p: p.distance(self))

    def polar(self, angle: float, distance: int) -> "Point":
        return Point(self.x + (distance * math.cos(angle)),
                     self.y + (distance * math.sin(angle)))

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
            return self.q == point.x

        return point.x * self.m - self.q == point.y

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

    def intersect(self, point: Point) -> bool:
        return (super().intersect(point)
                and min(self.p1.x, self.p2.x) <= point.x <= max(self.p1.x, self.p2.x)
                and min(self.p1.y, self.p2.y) <= point.y <= max(self.p1.y, self.p2.y))

    def length(self) -> float:
        return self.p1.distance(self.p2)

# === PointId === ============================================================ #

class PointId(Point):
    id: int

    def __init__(self, id, x, y) -> "PointId":
        super().__init__(x, y)
        self.id = id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id}, {self.x}, {self.y})"

    def __eq__(self, other: "PointId") -> bool:
        return super().__eq__(other) and self.id == other.id

# === WalkerMixIn === ======================================================== #

def WalkerMixIn(speed: int, range: int):
    class Walker(object):
        SPEED: int = speed
        RANGE: int = range

        def turns_to_reach(self, other: Point) -> int:
            return math.floor(self.distance(other) - self.RANGE / self.SPEED)

        def simulate_moves(self, target: Point) -> List[Segment]:
            return Segment(self, target) / self.SPEED

        def converge(self, target: Point, converge: Point) -> Point:
            pass

        def inside(self, point: Point) -> bool:
            return math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2) < self.RANGE

    return Walker

# === Ash === ================================================================ #

class Ash(Point, WalkerMixIn(speed=1000, range=2000)):

    def simulate_moves(self, zombie: "Zombie") -> List[Segment]:
        return super().simulate_moves(zombie)

# === Human === ============================================================== #

class Human(PointId):
    zombies: Set["Zombie"]

    def __init__(self, id, x, y) -> "Human":
        super().__init__(id, x, y)
        self.zombies = set()

    def __eq__(self, other: "Human") -> bool:
        return super().__eq__(other) and self.zombies == other.zombies

    def bind_zombies(self, zombies: List["Zombie"]) -> None:
        for zombie in zombies:
            if zombie.is_attakking(self) or zombie.human_target == self:
                self.zombies.add(zombie)
                zombie.human_target = self

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

    def __eq__(self, other: "Zombie") -> str:
        return (super().__eq__(other)
                and self.x_next == other.x_next
                and self.y_next == other.y_next
                and self.human_target == other.human_target)

    def __hash__(self) -> int:
        return hash((self.id, self.x, self.y, self.x_next, self.y_next, self.human_target))

    def next(self) -> Point:
        return Point(self.x_next, self.y_next)

    def is_attakking(self, human: Human) -> bool:
        return Segment(self, human).intersect(self.next())

    def fake_bind(self, human: Human) -> None:
        self.human_target = human

# === GameField === ========================================================== #

class Field(object):
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

# 1. Zombie move
# 2. Ash Move
# 3. Ash Kill Zombie < 2000
# 4. Zombie eat

class Prediction(object):
    pass

# === Game === =============================================================== #

class Game(object):
    WIDTH: int = 16000
    HEIGHT: int = 9000

    field: Field
    # predictions: MinMax[Field]

    def __init__(self, ash: Ash, humans: List[Human], zombies: List[Zombie]) -> "Game":
        self.field = Field(ash, humans, zombies)

    def predict(self):
        """must return a tree with all possible prediction
        """
        pass

    def play(self) -> Point:
        predictions = self.predict()

        return self.field.ash

# ============================================================================ #

if __name__ == '__main__':
    while True:
        game = Game(Ash(*[int(i) for i in input().split()]),
                   [Human(*[int(j) for j in input().split()]) for _ in range(int(input()))],
                   [Zombie(*[int(j) for j in input().split()]) for _ in range(int(input()))])

        print(game.play())
