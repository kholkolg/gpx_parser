from unittest import TestCase, main as ut_main
from functools import reduce
from typing import List
import operator
from gpx_parser.unittests.test_utils import random_point
from gpx_parser.GPXTrackPoint import GPXTrackPoint as TP
from gpx_parser.GPXTrackSegment import GPXTrackSegment as TS


class TestGPXTrackSegment(TestCase):

    def setUp(self):
        self.seg0:TS = TS()
        self.seg1:TS = TS([random_point() for i in range(10)])
        self.seg2:TS = TS([random_point() for i in range(5)])

    def tearDown(self):
        del self.seg0
        del self.seg1
        del self.seg2

    def test_points_getter(self):
        self.assertListEqual([], self.seg0.points)
        self.assertEqual(10, len(self.seg1))
        self.assertTrue(reduce(operator.and_, map(lambda x :isinstance(x, TP), self.seg1), True))

    def test_points_setter(self):
        new_points:List[TP] = [random_point() for i in range(12)]
        self.seg2.points = new_points
        self.assertListEqual(new_points, self.seg2.points)


    def test_append(self):
        new_point:TP = random_point()
        self.seg0.append(new_point)
        self.assertListEqual(self.seg0.points, [new_point])
        self.assertEqual(len(self.seg0), 1)
        self.seg0.append(random_point())
        self.assertEqual(len(self.seg0), 2)

    def test_extend(self):
        l:int = len(self.seg0)
        points:List[TP] = [random_point() for i in range(3)]
        self.seg0.extend(points)
        self.assertEqual(len(self.seg0), l + len(points))

    def test_remove(self):
        l:int = len(self.seg2)
        p:TP = self.seg2[l//2]
        self.assertIn(p, self.seg2)
        self.seg2.remove(p)
        self.assertEqual(l-1, len(self.seg2))
        self.assertNotIn(p, self.seg2)


    def test_reduce_points(self):
        self.seg1.points.sort(key=lambda p :  p.time)
        l:int = len(self.seg1)
        dist:float = self.seg1.length_2d()/l

        self.seg1.reduce_points(dist)
        self.assertLessEqual(len(self.seg1), l)

        l = len(self.seg1)
        self.seg1.reduce_points(dist)
        self.assertEqual(len(self.seg1), l)


    def test_length_2d(self):
        self.assertEqual(0, self.seg0.length_2d())
        length:float = 0
        for i in range(1, len(self.seg1)):
            previous:TP = self.seg1.points[i - 1]
            point:TP = self.seg1.points[i]
            length += point.distance_2d(previous)
        self.assertEqual(length, self.seg1.length_2d())

    def test_split(self):
        l:int = len(self.seg1)
        n:int = l//2
        s1, s2 = self.seg1.split(n-1)
        self.assertEqual(len(s1), n)
        self.assertEqual(len(s2), l-n)
        self.assertIsInstance(s1, TS)
        self.assertIsInstance(s2, TS)

    def test_get_time_bounds(self):
        print('Seg2 %s' % self.seg2)
        print('start = %s, end = %s'%(self.seg2.get_time_bounds()))
        self.assertTupleEqual(self.seg0.get_time_bounds(), (None, None))
        self.seg1.points.sort(key=lambda p : p.time)
        self.assertTupleEqual(self.seg1.get_time_bounds(),
                              (self.seg1[0].time, self.seg1[-1].time))


    def test_get_bounds(self):
        seg1:TS = self.seg1
        seg1.points.sort(key=lambda p : p.latitude)
        min_lat:float = seg1[0].latitude
        max_lat:float = seg1[-1].latitude
        seg1.points.sort(key=lambda p : p.longitude)
        min_lon:float = seg1[0].longitude
        max_lon:float = seg1[-1].longitude
        self.assertTupleEqual(self.seg1.get_bounds(),
                              (min_lat, max_lat, min_lon, max_lon))
        print('lat: min= %.2f, max = %.2f\nlon: min = %.2f, max = %.2f' % (self.seg2.get_bounds()))

    def test_get_duration(self):
        self.seg2.points.sort(key=lambda p :  p.time)
        print('duration = %.2f' % self.seg2.get_duration())
        start, end = self.seg2.get_time_bounds()
        self.assertEqual((end-start).total_seconds(), self.seg2.get_duration())
        self.seg2.append(TP('10', '20'))
        self.assertIsNone(self.seg2.get_duration())

    def test_to_xml(self):
        result:List[str] = ['\n<trkseg>', ]
        result.extend(map(lambda p: p.to_xml(), self.seg2.points))
        result.append('\n</trkseg>')
        self.assertEqual(''.join(result), self.seg2.to_xml())


    def test_clone(self):
        clone:TS = self.seg2.clone()
        self.assertEqual(clone.to_xml(), self.seg2.to_xml())




if __name__ == '__main__':
    ut_main()