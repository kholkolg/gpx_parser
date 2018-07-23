from datetime import datetime
from typing import Tuple, List
from unittest import TestCase, main as ut_main

from .test_utils import random_point
from ..GPXTrackSegment import GPXTrackSegment as TS
from ..GPXTrack import GPXTrack as T
from ..GPX import GPX


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
        gpx0:GPX = GPX()
        tracks:List[T] = [self.t0, self.t1]
        gpx0.tracks = tracks
        self.assertListEqual(gpx0.tracks, tracks)

    def test_version(self):
        self.assertEqual(self.gpx.version, '1.0')
        gpx0:GPX = GPX()
        self.assertIsNone(gpx0.version)
        version:str = '1.1'
        gpx0.version = version
        self.assertEqual(gpx0.version, version)

    def test_creator(self):
        self.assertIsNone(self.gpx.creator)
        creator:str = 'creator'
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
        result:List[str] = ['<?xml version="1.0" encoding="UTF-8"?>',]
        version = self.gpx.version.replace('.', '/')
        result.append('\n<gpx xmlns="http://www.topografix.com/GPX/{}" ' \
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '        \
        'xsi:schemaLocation="http://www.topografix.com/GPX/{} '         \
        'http://www.topografix.com/GPX/{}/gpx.xsd" '.format(version, version, version))
        result.append('version="%s" '% self.gpx.version)
        result.append('creator="gpx_parser.py">')
        result.extend([t.to_xml() for t in self.gpx.tracks])
        result.append('\n</gpx>')
        self.assertEqual(''.join(result), self.gpx.to_xml())

    def test_reduce_points(self):
        self.seg1.points.sort(key=lambda p: p.time)
        l: int = len(self.gpx)
        dist: float = self.seg1.length_2d() / l

        self.gpx.reduce_points(dist)
        self.assertLessEqual(len(self.gpx), l)

        l = len(self.gpx)
        self.gpx.reduce_points(dist)
        self.assertEqual(len(self.gpx), l)

    def test_length_2d(self):
        self.assertEqual(len(GPX()), 0)
        length: float = self.t0.length_2d() + self.t1.length_2d()
        self.assertEqual(self.gpx.length_2d(), length)

    def test_get_time_bounds(self):
        self.seg1.points.sort(key=lambda p: p.time)
        self.seg2.points.sort(key=lambda p: p.time)
        b1: Tuple[datetime, datetime] = self.seg1.get_time_bounds()
        b2: Tuple[datetime, datetime] = self.seg2.get_time_bounds()
        self.assertTupleEqual(self.gpx.get_time_bounds(), (b1[0], b2[1]))

    def test_get_bounds(self):
        b1: Tuple[float, float, float, float] = self.seg1.get_bounds()
        b2: Tuple[float, float, float, float] = self.seg2.get_bounds()
        min_lat: float = min(b1[0], b2[0])
        max_lat: float = max(b1[1], b2[1])
        min_lon: float = min(b1[2], b2[2])
        max_lon: float = max(b1[3], b2[3])
        self.assertTupleEqual(self.gpx.get_bounds(), (min_lat,
                                                     max_lat,
                                                     min_lon,
                                                     max_lon))

    def test_get_points_no(self):
        self.assertEqual(self.gpx.get_points_no(), self.t0.get_points_no() + self.t1.get_points_no())

    def test_walk(self):
        clone:GPX = self.gpx.clone()
        self.assertEqual(self.gpx.to_xml(), clone.to_xml())


if __name__ == '__main__':
    ut_main()