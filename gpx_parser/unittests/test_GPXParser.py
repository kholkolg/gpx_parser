from unittest import TestCase, main as ut_main
from xml.etree.ElementTree import Element as El
from gpx_parser.GPX import GPX as GPX
from gpx_parser.parser import GPXParser as Parser
from os import path


class TestGPXParser(TestCase):

    def setUp(self):
        with open(path.abspath('./test_data/test1.gpx'), 'r') as xml_file:
            self.parser:Parser = Parser(xml_file)
        self.assertIsInstance(self.parser, Parser)
        self.assertEqual(len(self.parser.gpx), 0)

    def tearDown(self):
        del self.parser


    def test_init(self):
        self.assertIsInstance(self.parser.xml, El)
        self.assertEqual(len(self.parser.xml), 1)

    def test_parse(self):
        gpx = self.parser.parse()
        self.assertIsInstance(gpx, GPX)
        self.assertEqual(len(gpx), 1)
        self.assertEqual(gpx.get_points_no(), 5)
        self.assertIsInstance(self.parser.xml, El)




if __name__ == '__main__':
    ut_main()