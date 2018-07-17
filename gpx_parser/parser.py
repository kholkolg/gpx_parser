from gpx_parser.GPX import GPX
from gpx_parser.GPXTrack import GPXTrack
from gpx_parser.GPXTrackSegment import GPXTrackSegment
from gpx_parser.GPXTrackPoint import GPXTrackPoint
from gpx_parser.xml_loader import load_xml





class GPXParser:

    def __init__(self, xml_or_file):
       #print("Init: ", xml_or_file)
        self.init(xml_or_file)
        self.gpx = GPX()

    def init(self, xml_or_file, loader = load_xml):
        #print('parser.init: ', xml_or_file)
        text = xml_or_file.read() if hasattr(xml_or_file, 'read') else xml_or_file
        #print('text: ', text, type(text))
        self.xml = loader(text)

    def parse(self) ->GPX:
        for track in self.xml.iterfind('trk'):
            new_track = GPXTrack(track[0].text, track[1].text)
            for segment in track.iterfind('trkseg'):
                new_segment = GPXTrackSegment()
                for point in segment.iterfind('trkpt'):
                    values = point.attrib
                    values['time'] = point[0].text
                    #print('PARSER: ', point[0].text)
                    #print(values, '###')
                    new_point = GPXTrackPoint(point.attrib) # attrib is a dictionary
                    new_segment.append(new_point)
                new_track.append(new_segment)
            #print('Name: ' + track[0].text)
            #print('Number: ' + track[1].text)
            self.gpx.append(new_track)


        return self.gpx



#
# fn = '/home/olga/Documents/GPX/test1.gpx'
# with open(fn, 'r') as xml_file:
#     parser = GPXParser(xml_file)
# gpx = parser.parse()
# print(type(gpx))
# print(gpx)

