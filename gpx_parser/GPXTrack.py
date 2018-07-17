from typing import Union, Optional, List, Iterator, Iterable

from gpx_parser.GPXTrackSegment import GPXTrackSegment as TrackSegment


class GPXTrack:

    __slots__ = ('name', 'number', 'segments')

    def __init__(self, name:Optional[str]=None, number:Optional[str]=None, segments:Optional[List[TrackSegment]]=None):
        self.name:Optional[str] = name
        self.number:Optional[int] = int(number)
        self.segments:List[TrackSegment] = segments if segments else [] # use sets instead??

    def __repr__(self)->str:
        return 'GPXTrack(%s  %s)(%s)(segments=%s)' % (self.name, self.number, len(self.segments), self.segments)

    def __len__(self)->int:
        return len(self.segments)

    def __iter__(self)->Iterator[TrackSegment]:
        return iter(self.segments)

    def __getitem__(self, key:int)->Union[TrackSegment, List[TrackSegment]]:
        if isinstance(key, int):
            return self.segments[key]
        elif isinstance(key,slice):
            return self.segments[key.start:key.stop:key.step]
        else:
            raise TypeError('Index must be int, not {}'.format(type(key).__name__))


    def __contains__(self, item:TrackSegment)->bool:
        return item in self.segments

    def append(self, item:TrackSegment):
        self.segments.append(item)

    def extend(self, items:Iterable[TrackSegment]):
        self.segments.extend(items)

    def remove(self,item:TrackSegment):
        self.segments.remove(item)


    def get_points_no(self)->int:
        """

        :return: total number of points in all the segments of the track
        """
        return sum([len(seg) for seg in self.segments])


if __name__ == '__main__':

    from gpx_parser.GPXTrackPoint import GPXTrackPoint as TrackPoint

    x = "50.0164596"
    y =  "14.4547907"
    lat = 'lat'
    lon = 'lon'
    t = 'time'

    p1 = TrackPoint({'lat':x, 'lon':y, t:'2017-11-22T07:03:36Z'})
    p2 = TrackPoint({lat:y, lon:x, t:'2017-11-23T07:03:36Z'})
    p3 = TrackPoint({lat:y, lon:y, t:'2017-12-23T08:11:06Z'})
    p4 = TrackPoint({lat:x, lon:x, t:'2020-12-23T08:11:06Z'})
    seg1 = TrackSegment([p1, p2, p3])
    seg2 = TrackSegment([p2, p3, p4])
    track = GPXTrack('800003627_337', '0')
    print(track)
    track.append(seg1)
    print('Len 1: ',  len(track))
    seg3 = TrackSegment([p4, p1])
    track.extend([seg2, seg3])
    print('Len 2: ', len(track) , 'Points: ', track.get_points_no())
    print('Slice: ', track[2:])

    for s in track:
        print(s)

    track.remove(seg1)
    print('Len 3: ', len(track))
