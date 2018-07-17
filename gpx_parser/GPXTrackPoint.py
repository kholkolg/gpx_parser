from typing import Dict
from gpx_parser.utils import parse_time



class GPXTrackPoint:

    __slots__ = ('values')

    def __init__(self, vals:Dict):
        #print('Trkpt __init__:',lat, lon, time)
        self.values = {'latitude': vals['lat'], 'longitude': vals['lon'], 'time':vals['time']}
        #print(vals)

    def __repr__(self):
        if self.values['time']:
            return 'GPXTrackPoint({}, {}, {})'.format(self.values['latitude'],
                                       self.values['longitude'],
                                       self.values['time'])
        return 'GPXTrackPoint({}, {})'.format(self.values['latitude'],
                                       self.values['longitude'])

    def __getattr__(self, item):
        #print('getattr '+ item)
        if isinstance(self.values[item], str):
            self.from_string(item)
        return self.values[item]


    def from_string(self, item, time_converter = parse_time):
        if item != 'time':
            self.values[item] = float(self.values[item])
        else:
            self.values[item] = time_converter(self.values[item])



# if __name__ == '__main__':
#
#     p = GPXTrackPoint({'latitude':'50.0164596', 'longitude': '14.4547907','time':'2017-11-22T07:25:02Z'})
#     print(p)
#     lat = p.latitude
#     lon = p.longitude
#     time = p.time
#     print(lat, lon, time)

