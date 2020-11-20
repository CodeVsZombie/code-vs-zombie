from codeingame import Point, Line, PointId, Segment, Ash, Human, Zombie, Field

import math
import pytest

def test_calculate_distances():
	a = Point(0, 0)
	b = Point(1, 0)
	c = Point(0, 1)
	d = Point(1, 1)

	assert a.distance(b) == 1
	assert a.distance(c) == 1
	assert a.distance(d) == 1 * math.sqrt(2)


def test_calculate_angles():
	a = Point(0, 0)
	b = Point(1, 0) # 0
	c = Point(0, 1) # 90
	d = Point(1, 1) # 45

	assert a.angle(b) == 0
	assert a.angle(c) == 90
	assert a.angle(d) == 45


def test_calculate_trajectories():
	a = Point(0, 0)
	b = Point(100, 100)

	e = a.angle(b)
	assert e == 45


def test_invalid_line():
	with pytest.raises(ValueError):
		Line.from_points(Point(0, 0), Point(0, 0))


def test_calculate_not_parallel():
	a = Line(1, 1)
	b = Line(4, 1)

	assert not a.parallel(b)

	a = Line(2, 1)
	b = Line(-2, 1)

	assert not a.parallel(b)


def test_calculate_parallel():
	a = Point(0, 0)
	b = Point(0, 1)
	l = Line.from_points(a, b)

	c = Point(1, 0)
	d = Point(1, 1)
	g = Line.from_points(c, d)

	assert l.parallel(g)


	a = Point(0, 0)
	b = Point(1, 0)
	l = Line.from_points(a, b)

	c = Point(0, 1)
	d = Point(1, 1)
	g = Line.from_points(c, d)

	assert l.parallel(g)


def test_calculate_not_perpendicular():
	a = Line(2, 1)
	b = Line(4, 1)

	assert not a.perpendicular(b)

	a = Line(3, 1)
	b = Line(5, 1)

	assert not a.perpendicular(b)


def test_calculate_perpendicular():
	a = Point(0, 0)
	b = Point(0, 1)
	l = Line.from_points(a, b)

	c = Point(0, 1)
	d = Point(1, 1)
	g = Line.from_points(c, d)

	assert l.perpendicular(g)

	a = Point(0, 0)
	b = Point(1, 0)
	l = Line.from_points(a, b)

	c = Point(1, 0)
	d = Point(1, 1)
	g = Line.from_points(c, d)

	assert l.perpendicular(g)


def test_line_not_intersect_point():
	a = Point(0, 0)
	b = Point(5, 5)
	l = Line.from_points(a, b)

	c = Point(3, 1)
	d = Point(2, 1)
	e = Point(-2, -1)

	assert not l.intersect(c)
	assert not l.intersect(d)
	assert not l.intersect(e)


def test_line_intersect_point():
	a = Point(0, 0)
	b = Point(2, 2)
	l = Line.from_points(a, b)

	c = Point(1, 1)
	d = Point(3, 3)
	e = Point(-1, -1)

	assert l.intersect(c)
	assert l.intersect(d)
	assert l.intersect(e)


def test_segment_not_intersect_point():
	a = Point(0, 0)
	b = Point(5, 5)
	s = Segment(a, b)

	c = Point(0, 1)
	d = Point(1, 0)
	e = Point(-2, -2)
	e = Point(7, 7)

	assert not s.intersect(c)
	assert not s.intersect(d)
	assert not s.intersect(e)


def test_segment_intersect_point():
	a = Point(0, 0)
	b = Point(4, 4)
	s = Segment(a, b)

	c = Point(1, 1)
	d = Point(2, 2)
	e = Point(3, 3)

	assert s.intersect(c)
	assert s.intersect(d)
	assert s.intersect(e)


def test_segment_intersect_point_on_y():
	a = Point(0, 8999)
	b = Point(0, 4500)
	s = Segment(a, b)

	c = Point(0, 7999)
	d = Point(0, 6999)
	e = Point(0, 5999)

	external = Point(8250, 9999)  # this is external

	assert s.intersect(c)
	assert s.intersect(d)
	assert s.intersect(e)
	assert not s.intersect(external)


def test_split_segment_equals():
	s = Segment(Point(0,0), Point(10,0))

	ss = s / 2

	assert len(ss) == 2

	assert ss[0] == Segment(Point(0, 0), Point(5, 0))
	assert ss[1] == Segment(Point(5, 0), Point(10, 0))


def test_split_segment_size():
	s = Segment(Point(0,0), Point(3,0))

	ss = s // 1

	assert len(ss) == 3

	assert ss[0] == Segment(Point(0, 0), Point(1, 0))
	assert ss[1] == Segment(Point(1, 0), Point(2, 0))
	assert ss[2] == Segment(Point(2, 0), Point(3, 0))

	s = Segment(Point(0, 0), Point(10, 0))

	ss = s // 2

	assert len(ss) == 5

	assert ss[0] == Segment(Point(0, 0), Point(2, 0))
	assert ss[1] == Segment(Point(2, 0), Point(4, 0))
	assert ss[2] == Segment(Point(4, 0), Point(6, 0))
	assert ss[3] == Segment(Point(6, 0), Point(8, 0))
	assert ss[4] == Segment(Point(8, 0), Point(10, 0))


def test_reprs():
	line = Line(3, 5)
	assert line == eval(repr(line))

	segment = Segment(Point(0, 0), Point(1, 1))
	assert segment == eval(repr(segment))

	point = Point(0, 0)
	assert point == eval(repr(point))

	point_id = PointId(3, 3, 3)
	assert point_id == eval(repr(point_id))

	ash = Ash(5, 7)
	assert ash == eval(repr(ash))

	human = Human(5, 7, 9)
	assert human == eval(repr(human))

	zombie = Zombie(7, 1, 5, 2, 6)
	print("zombie", repr(zombie))
	assert zombie == eval(repr(zombie))

	# field = Field(ash, [human], [zombie])
	# assert field == eval(repr(field))


def test_in_operator_for_line():
	line = Line.from_points(Point(0, 0), Point(2, 2))

	assert Point(-1, -1) in line
	assert Point(3, 3) in line
	assert Point(1, 1) in line
	assert Point(1, 5) not in line


def test_in_operator_for_segment():
	s = Segment(Point(0, 0),Point(2, 2))

	assert Point(-1, -1) not in s
	assert Point(3, 3) not in s
	assert Point(1, 1) in s
	assert Point(1, 5) not in s


def test_midpoint_segment():
	a = Point(0, 0)
	b = Point(2, 2)

	assert Segment(a, b).midpoint() == Point(1, 1)

	a = Point(0, 0)
	b = Point(2, 0)

	assert Segment(a, b).midpoint() == Point(1, 0)

	a = Point(0, 2)
	b = Point(0, 0)

	assert Segment(a, b).midpoint() == Point(0, 1)

	a = Point(0, 0)
	b = Point(3, 3)

	assert Segment(a, b).midpoint() == Point(2, 2)


def test_simulation_encoding_decoding():
	a = Ash(0, 0)
	h1 = Human(0, 1, 1)
	h2 = Human(1, 2, 2)
	h3 = Human(2, 3, 3)
	z1 = Zombie(0, 3, 3, 4, 4, human_target=h1)
	z2 = Zombie(0, 3, 3, 4, 4)

	f = Field(a, [h1, h2, h3], [z1, z2])


def test_nearest_coordinate():
	pass


"""@pytest.mark.skipif(False, reason='i want to skip')
def test_win_simulations():
	from simulator import main

	simulations = ['simple']

	for simulation in simulations:
		assert main(simulation, enable_graphics=False)
"""