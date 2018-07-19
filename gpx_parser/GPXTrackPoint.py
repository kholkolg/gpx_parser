from datetime import datetime
from typing import Optional, Union, Callable, Tuple

from gpx_parser.utils import parse_time

# @overload
# def utf8(value: None) -> None:
#     pass
# @overload
# def utf8(value: bytes) -> bytes:
#     pass
# @overload
# def utf8(value: unicode) -> bytes:
#     pass
# def utf8(value):
#     <actual implementation>



class GPXTrackPoint:
    __slots__ = ('_lat', '_lon', '_time', '_strings')

    def __init__(self, lat:str, lon:str, time:Optional[str]=None):
        self._strings:Tuple[str, str, Optional[str]] = (lat, lon, time)

    def __repr__(self)->str:
        return 'GPXTrackPoint(%s, %s, %s)'% self._strings

    @property
    def latitude(self)->float:

        try:
            return self._lat
        except AttributeError:
            self._lat:float = float(self._strings[0])

        return self._lat

    @property
    def longitude(self) -> float:
        try:
            return self._lon
        except AttributeError:
            self._lon: float = float(self._strings[1])
        return self._lon

    @property
    def time(self, converter:Callable = parse_time)-> Optional[datetime]:
        try:
            return self._time
        except AttributeError:
            try:
                self._time = converter(self._strings[2])
                return self._time
            except TypeError:
                return None

    @time.setter
    def time(self, time:str):
        self._strings = self._strings[:2] + (time,)



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