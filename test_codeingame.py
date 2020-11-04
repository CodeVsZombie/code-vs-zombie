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


def test_invalid_line():
	with pytest.raises(ValueError):
		Line.from_points(Point(0, 0), Point(0, 0))


def test_calculate_not_parallel():
	a = Line(1.5, 1)
	b = Line(3.5, 1)

	assert not a.parallel(b)

	a = Line(1.5, 1)
	b = Line(-1.5, 1)

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
	a = Line(1.5, 1)
	b = Line(3.5, 1)

	assert not a.perpendicular(b)

	a = Line(1.5, 1)
	b = Line(1.5, 1)

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
	b = Point(1, 1)
	l = Line.from_points(a, b)

	c = Point(0.5, 1)
	d = Point(1.5, 1)
	e = Point(-1.5, -1)

	assert not l.intersect(c)
	assert not l.intersect(d)
	assert not l.intersect(e)


def test_line_intersect_point():
	a = Point(0, 0)
	b = Point(1, 1)
	l = Line.from_points(a, b)

	c = Point(0.5, 0.5)
	d = Point(1.5, 1.5)
	e = Point(-1.5, -1.5)

	assert l.intersect(c)
	assert l.intersect(d)
	assert l.intersect(e)


def test_segment_not_intersect_point():
	a = Point(0, 0)
	b = Point(1, 1)
	s = Segment(a, b)

	c = Point(0.5, 1)
	d = Point(1.5, 1.5)
	e = Point(-1.5, -1.5)

	assert not s.intersect(c)
	assert not s.intersect(d)
	assert not s.intersect(e)

def test_segment_intersect_point():
	a = Point(0, 0)
	b = Point(1, 1)
	s = Segment(a, b)

	c = Point(0.5, 0.5)
	d = Point(0.3, 0.3)
	e = Point(0.9, 0.9)

	assert s.intersect(c)
	assert s.intersect(d)
	assert s.intersect(e)


def test_split_segment():
	s = Segment(
		Point(0,0),
		Point(5,0)
	)

	ss = s / 1

	assert len(ss) == 5
	assert ss[0] == Segment(Point(0, 0), Point(1, 0))
	assert ss[1] == Segment(Point(1, 0), Point(2, 0))
	assert ss[2] == Segment(Point(2, 0), Point(3, 0))
	assert ss[3] == Segment(Point(3, 0), Point(4, 0))
	assert ss[4] == Segment(Point(4, 0), Point(5, 0))

	s = Segment(
		Point(0,0),
		Point(4.5,0)
	)

	ss = s / 1

	assert len(ss) == 5
	assert ss[0] == Segment(Point(0, 0), Point(1, 0))
	assert ss[1] == Segment(Point(1, 0), Point(2, 0))
	assert ss[2] == Segment(Point(2, 0), Point(3, 0))
	assert ss[3] == Segment(Point(3, 0), Point(4, 0))
	assert ss[4] == Segment(Point(4, 0), Point(4.5, 0))


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
	assert zombie == eval(repr(zombie))

	field = Field(ash, [human], [zombie])
	assert field == eval(repr(field))
