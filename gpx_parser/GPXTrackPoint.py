from datetime import datetime
from typing import Optional, Union, Callable

from gpx_parser.utils import parse_time


class GPXTrackPoint:

    __slots__ = ('_lat', '_lon', '_time')

    def __init__(self, lat:str, lon:str, time:Optional[str]=None):
        #print('Trkpt __init__:',lat, lon ,time)
        self._lat:Union[str,float] = lat
        self._lon:Union[str,float] = lon
        self._time:Optional[Union[str,datetime]] = time
        #print(vals)

    def __repr__(self)->str:
        if self._time:
            return 'GPXTrackPoint({}, {}, {})'.format(self._lat, self._lon, self._time)
        return 'GPXTrackPoint({}, {})'.format(self._lat, self._lon)

    @property
    def latitude(self)->float:
        if isinstance(self._lat, str):
            self._lat = float(self._lat)
        return  self._lat

    @property
    def longitude(self) -> float:
        if isinstance(self._lon, str):
            self._lon = float(self._lon)
        return self._lon

    @property
    def time(self, converter:Callable = parse_time)-> datetime:
        if isinstance(self._time, str):
            self._time = converter(self._time)
        return self._time

    @time.setter
    def time(self, time:Union[datetime,str]):
        self._time = time


if __name__ == '__main__':

    p1 = GPXTrackPoint('50.0164596', '14.4547907','2017-11-22T07:25:02Z')
    print('Point with time: ', p1)
    print('.latitude=%s, .longitude=%s, .time=%s'%( p1.latitude, p1.longitude, p1.time))

    p2 = GPXTrackPoint('70.6978', '41.0749454')
    print('Point without time: ',p2)
    print('.time=',p2.time)
    p2.time = '1234-11-22T07:25:02Z'
    print('set time:', p2)
    print('.time=', p2.time)