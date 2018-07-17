from datetime import datetime
from typing import Dict, Optional, Union

from gpx_parser.utils import parse_time


class GPXTrackPoint:

    __slots__ = ('values')

    def __init__(self, vals:Dict[str,Optional[Union[str, float]]]):
        #print('Trkpt __init__:',vals)
        self.values:Dict[str:Optional[Union[str, float]]] =\
            {'latitude': vals['lat'], 'longitude': vals['lon'], 'time':vals['time']}
        #print(vals)

    def __repr__(self)->str:
        if self.values['time']:
            return 'GPXTrackPoint({}, {}, {})'.format(self.values['latitude'],
                                       self.values['longitude'],
                                       self.values['time'])
        return 'GPXTrackPoint({}, {})'.format(self.values['latitude'],
                                       self.values['longitude'])

    def __getattr__(self, key:str)->Union[float,datetime]:
        #print('getattr '+ item)
        if isinstance(self.values[key], str):
            self.from_string(key)
        return self.values[key]

    def from_string(self, key:str, time_converter = parse_time):
        if key != 'time':
            self.values[key] = float(self.values[key])
        else:
            self.values[key] = time_converter(self.values[key])


if __name__ == '__main__':

    p = GPXTrackPoint({'lat':'50.0164596', 'lon': '14.4547907','time':'2017-11-22T07:25:02Z'})
    print(p)
    lat = p.latitude
    lon = p.longitude
    time = p.time
    print(lat, lon, time)

