from typing import Optional, List, Union, Iterator, Iterable

from gpx_parser.GPXTrack import GPXTrack as Track


class GPX:

    __slots__ = ('_version', '_creator', '_tracks')

    def __init__(self, version:Optional[str]=None, creator:Optional[str]=None, tracks:Optional[List[Track]]=None):
        self._version:Optional[str] = version
        self._creator:Optional[str] = creator
        self._tracks:List[Track] = tracks if tracks else []


    def __repr__(self)->str:
        return 'GPX(%s)(tracks=%s)' % (len(self._tracks), self._tracks)

    def __getitem__(self, key:Union[int, slice])-> Union[Track,List[Track]]:
        if isinstance(key, int):
            return self._tracks[key]
        elif isinstance(key, slice):
            return self._tracks[key.start:key.stop:key.step]
        else:
            raise TypeError('Index must be int, not {}'.format(type(key).__name__))

    def __len__(self)->int:
        return len(self._tracks)

    def __contains__(self, item:Track)->bool:
        return item in self._tracks

    def __iter__(self)-> Iterator[Track]:
        return iter(self._tracks)

    @property
    def tracks(self):
        return self._tracks

    @tracks.setter
    def tracks(self, tracks:List[Track]):
        self._tracks = tracks

    @property
    def version(self)->str:
        return self._version

    @version.setter
    def version(self, ver:str):
        self._version = ver

    @property
    def creator(self)->str:
        return self._creator

    @creator.setter
    def creator(self, creator:str):
        self._creator = creator

    def append(self, item:Track):
        self._tracks.append(item)

    def extend(self, items:Iterable[Track]):
        self._tracks.extend(items)

    def remove(self, item:Track):
        self._tracks.remove(item)




if __name__ == '__main__':

    from gpx_parser.GPXTrackPoint import GPXTrackPoint as TrackPoint
    from gpx_parser.GPXTrackSegment import GPXTrackSegment as TrackSegment

    x = "50.0164596"
    y = "14.4547907"
    p1 = TrackPoint(x, y, '2017-11-22T07:03:36Z')
    p2 = TrackPoint(y, x)
    p3 = TrackPoint(y, y, '2617-11-13T08:11:09Z')
    p4 = TrackPoint(x, x)
    seg1 = TrackSegment([p1, p2, p3])
    seg2 = TrackSegment([p2, p3, p4])
    seg3 = TrackSegment([p4, p1])
    track1 = Track('800003627_337', '0', [seg1, seg2, seg3])
    track2 = Track('800003627_908', None, [seg2, seg3])
    track3 = Track(None, '2', [TrackSegment([p4])])
    print('Track with name, number, 3 segments: ',track1)
    print('Track with name,no number, 2 segments: ',track2)
    print('Track with no name, number, 1 segment: ', track3)

    gpx = GPX('1.0','gpx.py -- https://github.com/tkrajina/gpxpy')
    print('Empty gpx with version and creator: ', gpx)
    gpx.append(track1)
    print('1 track added: ', gpx)
    gpx.extend([track2,track3])
    print('2 more tracks added, len = ', gpx)

    print('Slice: ', gpx[0:1])
    print('third track: ', gpx[2])

    print('Iterator')
    for t in gpx:
        print(t)

    gpx.remove(track3)
    print('.tracks after 1 track removed: ', gpx.tracks)


