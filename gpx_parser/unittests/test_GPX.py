from datetime import datetime
from typing import Tuple, List
from unittest import TestCase, main as ut_main
from gpx_parser.unittests.test_utils import random_point
from gpx_parser.GPXTrackSegment import GPXTrackSegment as TS
from gpx_parser.GPXTrack import GPXTrack as T
from gpx_parser.GPX import GPX


class TestGPX(TestCase):

    def setUp(self):
        self.seg0: TS = TS()
        self.seg1: TS = TS([random_point() for i in range(3)])
        self.seg1: TS = TS([random_point() for i in range(3)])
        self.seg2: TS = TS([random_point() for i in range(5)])
        self.t0: T = T('name0', '0', [self.seg1, self.seg2])
        self.t1: T = T('name1', '1', [self.seg0, ])
        self.gpx:GPX = GPX('1.0', None, [self.t0, self.t1])

    def tearDown(self):
        del self.seg0
        del self.seg1
        del self.seg2
        del self.t0
        del self.t1
        del self.gpx

    def test_tracks(self):
        self.assertListEqual(self.gpx.tracks, [self.t0, self.t1])
        self.assertListEqual(GPX().tracks, [] )
        gpx0 = GPX()
        tracks = [self.t0, self.t1]
        gpx0.tracks = tracks
        self.assertListEqual(gpx0.tracks, tracks)

    def test_version(self):
        self.assertEqual(self.gpx.version, '1.0')
        gpx0 = GPX()
        self.assertIsNone(gpx0.version)
        version = '1.1'
        gpx0.version = version
        self.assertEqual(gpx0.version, version)

    def test_creator(self):
        self.assertIsNone(self.gpx.creator)
        creator = 'creator'
        self.gpx.creator = creator
        self.assertEqual(self.gpx.creator, creator)


    def test_append(self):
        gpx0:GPX = GPX()
        self.assertNotIn(self.t1, gpx0)
        gpx0.append(self.t1)
        self.assertIn(self.t1, gpx0)

    def test_extend(self):
        gpx0:GPX = GPX()
        self.assertNotIn(self.t1, gpx0)
        gpx0.extend([self.t1, self.t0])
        self.assertIn(self.t1, gpx0)
        self.assertEqual(len(gpx0), 2)

    def test_remove(self):
        self.assertIn(self.t1, self.gpx)
        self.gpx.remove(self.t1)
        self.assertNotIn(self.t1, self.gpx)

    def test_to_xml(self):
        self.fail()

    # def test_reduce_points(self):
    #     self.fail()
    #
    # def test_length_2d(self):
    #     self.fail()
    #
    # def test_get_time_bounds(self):
    #     self.fail()
    #
    # def test_get_bounds(self):
    #     self.fail()
    #
    # def test_get_points_no(self):
    #     self.fail()
    #
    # def test_walk(self):
    #     self.fail()


if __name__ == '__main__':
    ut_main()