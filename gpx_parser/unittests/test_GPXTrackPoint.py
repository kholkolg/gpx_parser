from unittest import TestCase, main as ut_main
from datetime import datetime

from gpx_parser.unittests.test_utils import random_point
from gpx_parser.GPXTrackPoint import GPXTrackPoint as TP

class TestGPXTrackPoint(TestCase):

    def setUp(self):
        self.point1:TP = random_point()
        self.point2:TP = random_point()
        self.point3:TP = random_point(with_time=False)
        self.point4:TP = TP("50.0164596","14.4547907","2017-01-22T07:03:36Z")

    def tearDown(self):
        del self.point1
        del self.point2
        del self.point3
        del self.point4

    def test_latitude(self):
        self.assertIsInstance(self.point1.latitude, float)
        self.assertEqual(float(self.point1._strings[0]), self.point1.latitude)
        self.assertIsInstance(self.point2.latitude, float)
        self.assertEqual(float(self.point2._strings[0]), self.point2.latitude)

    def test_longitude(self):
        self.assertIsInstance(self.point1.longitude, float)
        self.assertEqual(float(self.point1._strings[1]), self.point1.longitude)
        self.assertIsInstance(self.point3.longitude, float)
        self.assertEqual(float(self.point3._strings[1]), self.point3.longitude)

    def test_time(self):
        self.assertIsInstance(self.point1.time, datetime)
        self.assertIsNone(self.point3.time, None)


    def test_to_xml(self):
        txt:str = '\n<trkpt lat="50.0164596" lon="14.4547907">' \
              '\n<time>2017-01-22T07:03:36Z</time>\n' \
              '</trkpt>'
        xml:str = self.point4.to_xml()
        self.assertEqual(txt, xml)


    def test_time_difference(self):
        print('time difference: %s and %s = %.3f'% (self.point1.time,
                                                    self.point2.time,
                                                    self.point1.time_difference(self.point2) ))
        self.assertIsNone(self.point3.time_difference(self.point4))


    def test_distance_2d(self):
        print('distance etween: %s and %s = %.3f' % (self.point1,
                                                     self.point2,
                                                    self.point1.distance_2d(self.point2)))

    def test_speed_between(self):
        print('speed between: %s and %s = %.3f' % (self.point1,
                                                   self.point2,
                                                   self.point1.speed_between(self.point2)))
        self.assertIsNone(self.point3.speed_between(self.point4))



if __name__ == '__main__':
    ut_main()