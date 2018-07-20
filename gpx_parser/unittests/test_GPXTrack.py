from datetime import datetime
from typing import Tuple, List
from unittest import TestCase, main as ut_main
from gpx_parser.unittests.test_utils import random_point
from gpx_parser.GPXTrackSegment import GPXTrackSegment as TS
from gpx_parser.GPXTrack import GPXTrack as T



class TestGPXTrack(TestCase):


    def setUp(self):
        self.seg0:TS = TS()
        self.seg1:TS = TS([random_point() for i in range(3)])
        self.seg1:TS = TS([random_point() for i in range(3)])
        self.seg2:TS = TS([random_point() for i in range(5)])
        self.t0:T = T()
        self.t1:T = T('2345_34','0',[self.seg1, self.seg2])


    def tearDown(self):
        del self.seg0
        del self.seg1
        del self.seg2
        del self.t0
        del self.t1


    def test_name(self):
        self.assertIsNone(self.t0.name)
        self.assertEqual(self.t1.name, '2345_34')

    def test_name_set(self):
        name:str = '800234342_300'
        self.t0.name = name
        self.assertEqual(self.t0.name, name)

    def test_number(self):
        self.assertIsNone(self.t0.number)
        self.assertEqual(self.t1.number, 0)

    def test_number_set(self):
        self.t0.number = 3
        self.assertEqual(self.t0.number, 3)

    def test_segments(self):
        self.assertListEqual(self.t0.segments, [])
        self.assertListEqual(self.t1.segments, [self.seg1, self.seg2])

    def test_points(self):
        self.assertListEqual(self.t0.points, [])
        self.t0.append(self.seg0)
        self.assertListEqual(self.t0.points, [])
        self.seg0.append(random_point())
        self.assertEqual(len(self.t0.points), 1)
        self.assertEqual(len(self.t1.points), 8)

    def test_get_points_no(self):
        self.assertEqual(self.t0.get_points_no(), 0)
        self.assertEqual(self.t1.get_points_no(), 8)

    def test_append(self):
        self.t0.append(self.seg0)
        self.assertEqual(len(self.t0), 1)
        self.t0.append(self.seg1)
        self.assertEqual(len(self.t0), 2)

    def test_extend(self):
        self.t0.extend([self.seg0, self.seg1, self.seg2])
        self.assertEqual(len(self.t0), 3)

    def test_remove(self):
        self.assertIn(self.seg1, self.t1)
        l:int = len(self.t1)
        self.t1.remove(self.seg1)
        self.assertNotIn(self.seg1, self.t1)
        self.assertEqual(len(self.t1), l - 1)

    def test_reduce_points(self):
        self.seg1.points.sort(key=lambda p :  p.time)
        l:int = len(self.t1)
        dist:float = self.seg1.length_2d()/l

        self.t1.reduce_points(dist)
        self.assertLessEqual(len(self.t1), l)

        l:int = len(self.t1)
        self.t1.reduce_points(dist)
        self.assertEqual(len(self.t1), l)

    def test_remove_empty(self):
        l:int = len(self.t1)
        self.t1.remove_empty()
        self.assertEqual(len(self.t1), l)
        self.t1.append(self.seg0)
        self.assertIn(self.seg0, self.t1)
        self.t1.remove_empty()
        self.assertNotIn(self.seg0, self.t1)

    def test_length_2d(self):
        self.assertEqual(self.t0.length_2d(), 0)
        length:float = self.seg1.length_2d() + self.seg2.length_2d()
        self.assertEqual(self.t1.length_2d(), length)

    def test_get_time_bounds(self):
        self.seg1.points.sort(key=lambda p:p.time)
        self.seg2.points.sort(key=lambda p: p.time)
        b1:Tuple[datetime, datetime] = self.seg1.get_time_bounds()
        b2:Tuple[datetime, datetime] = self.seg2.get_time_bounds()
        self.assertTupleEqual(self.t1.get_time_bounds(), (b1[0], b2[1]))


    def test_get_bounds(self):
        b1:Tuple[float, float, float, float] = self.seg1.get_bounds()
        b2:Tuple[float, float, float, float] = self.seg2.get_bounds()
        min_lat:float = min(b1[0], b2[0])
        max_lat:float = max(b1[1], b2[1])
        min_lon:float = min(b1[2], b2[2])
        max_lon:float = max(b1[3], b2[3])
        self.assertTupleEqual(self.t1.get_bounds(), (min_lat,
                                                     max_lat,
                                                     min_lon,
                                                     max_lon))

    def test_get_duration(self):
        d1:float = self.seg1.get_duration()
        d2:float = self.seg2.get_duration()
        self.assertEqual(self.t1.get_duration(), d1+d2)

    def test_to_xml(self):
        result:List[str] = ['\n<trk>\n<name>2345_34</name>\n<number>0</number>',]
        result.extend(map(lambda s:s.to_xml(), self.t1.segments))
        result.append('\n</trk>')
        self.assertEqual(''.join(result), self.t1.to_xml())


    def test_clone(self):
        clone:T = self.t1.clone()
        self.assertEqual(self.t1.to_xml(), clone.to_xml())



if __name__ == '__main__':
    ut_main()