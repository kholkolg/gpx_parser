name='gpx-parser'

from gpx_parser.GPX import GPX


def parse(xml_or_file)->GPX:
    """
    Parse xml (string) or file object. This is just an wrapper for
    GPXParser.parse() function.

    gpx_parser may be 'lxml', 'minidom' or None (then it will be automatically
    detected, lxml if possible).

    xml_or_file must be the xml to parse or a file-object with the XML.

    version may be '1.0', '1.1' or None (then it will be read from the gpx
    xml node if possible, if not then version 1.0 will be used).
    """

    from . import parser

    parser = parser.GPXParser(xml_or_file)
    return parser.parse()
