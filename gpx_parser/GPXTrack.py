from datetime import datetime
from typing import Union, Optional, List, Iterator, Iterable, Tuple
import copy as mod_copy

from gpx_parser.GPXTrackPoint import GPXTrackPoint as TrackPoint
from gpx_parser.GPXTrackSegment import GPXTrackSegment as TrackSegment


class GPXTrack:

    __slots__ = ('_name', '_number', '_segments')

    def __init__(self, name:Optional[str]=None, number:Optional[str]=None, segments:Optional[List[TrackSegment]]=None):
        self._name:Optional[str] = name
        self._number:Optional[int] = int(number) if number else None
        self._segments:List[TrackSegment] = segments if segments else []

    def __repr__(self)->str:
        return 'GPXTrack(%s  %s)(%s)(segments=%s)' % (self._name, self._number, len(self._segments), self._segments)

    def __len__(self)->int:
        return len(self._segments)

    def __iter__(self)->Iterator[TrackSegment]:
        return iter(self._segments)

    def __getitem__(self, key:int)->Union[TrackSegment, List[TrackSegment]]:
        if isinstance(key, int):
            return self._segments[key]
        elif isinstance(key,slice):
            return self._segments[key.start:key.stop:key.step]
        else:
            raise TypeError('Index must be int, not {}'.format(type(key).__name__))


    def __contains__(self, item:TrackSegment)->bool:
        return item in self._segments


    @property
    def name(self)->str:
        return self._name

    @name.setter
    def name(self, name:str):
        self._name = name

    @property
    def number(self)->int:
        return self._number

    @number.setter
    def number(self,num:str):
        self._number = int(num)

    @property
    def segments(self)->List[TrackSegment]:
        return self._segments

    @segments.setter
    def segments(self, segments:List[TrackSegment])->None:
        self._segments = segments

    @property
    def points(self)->List[TrackPoint]:
        return [pt for seg in self._segments for pt in seg.points]


    def get_points_no(self)->int:
        return sum(map(lambda s : len(s), self._segments))

    def append(self, item:TrackSegment):
        self._segments.append(item)

    def extend(self, items:Iterable[TrackSegment]):
        self._segments.extend(items)

    def remove(self,item:TrackSegment):
        self._segments.remove(item)

    def reduce_points(self, min_distance:float)->None:
        for seg in self._segments:
            seg.reduce_points(min_distance)

    def remove_empty(self)->None:
        self._segments = [s for s in filter(lambda s : len(s) > 0, self._segments)]

    def length_2d(self)->float:
        return sum(map(lambda seg : seg.length_2d(), self._segments ))

    def get_time_bounds(self)->Tuple[datetime, datetime]:
        start_time = None
        end_time = None

        for track_segment in self.segments:
            point_start_time, point_end_time = track_segment.get_time_bounds()
            if not start_time and point_start_time:
                start_time = point_start_time
            if point_end_time:
                end_time = point_end_time

        return start_time, end_time

    def get_bounds(self)->Tuple[float, float, float, float]:

        all_points = [p for seg  in self._segments for p in seg.points]
        min_lat = min(map(lambda pt :pt.latitude, all_points))
        max_lat = max(map(lambda pt :pt.latitude, all_points))
        min_lon = min(map(lambda pt :pt.longitude, all_points))
        max_lon = max(map(lambda pt :pt.longitude, all_points))

        return min_lat, max_lat, min_lon, max_lon


    def get_duration(self)->Optional[float]:
        try:
            return sum(map(lambda seg : seg.get_duration(), self._segments))
        except TypeError:
            return None

    def to_xml(self)->str:
        result:List[str] = ['\n<trk>',]
        if  self._name:
            result.extend(['\n<name>',self._name,'</name>'])
        if self.number is not None:
            result.extend(['\n<number>', str(self._number), '</number>'])
        result.extend(map(lambda s : s.to_xml(), self._segments))
        result +='\n</trk>'
        return ''.join(result)

    def clone(self):
        return mod_copy.deepcopy(self)


if __name__ == '__main__':

    from gpx_parser.GPXTrackPoint import GPXTrackPoint as TrackPoint

    x = "50.0164596"
    y =  "14.4547907"
    p1 = TrackPoint(x, y, '2017-11-22T07:03:36Z')
    p2 = TrackPoint(y, x)
    p3 = TrackPoint(y,y, '2617-11-13T08:11:09Z')
    p4 = TrackPoint(x, x)
    seg1 = TrackSegment([p1, p2, p3])
    seg2 = TrackSegment([p2, p3, p4])
    track = GPXTrack('800003627_337', '0')
    print('Empty track with name and number: ', track)
    track.append(seg1)
    print('1 segment added, len = ',  len(track))
    seg3 = TrackSegment([p4, p1])
    track.extend([seg2, seg3])
    print('2 more segments added, len: ', len(track))
    print('Points in all segments: ', track.get_points_no())
    print('Slice: ', track[2:])
    print('Iterator')
    for s in track:
        print(s)

    track.remove(seg1)
    print('1 segment removed: ', len(track))
