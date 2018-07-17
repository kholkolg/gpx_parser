from typing import Optional, List, Union, Iterator, Iterable

from gpx_parser.GPXTrack import GPXTrack as Track


class GPX:

    __slots__ = ('version', 'creator', 'tracks')

    def __init__(self, version:Optional[str]=None, creator:Optional[str]=None, tracks:Optional[List[Track]]=None):
        self.version:Optional[str] = version
        self.creator:Optional[str] = creator
        self.tracks:List[Track] = tracks if tracks else []


    def __repr__(self)->str:
        return 'GPX(%s)(tracks=%s)' % (len(self.tracks), self.tracks)

    def __getitem__(self, key:Union[int, slice])->Union[Track,List[Track]]:
        if isinstance(key, int):
            return self.tracks[key]
        elif isinstance(key, slice):
            return self.tracks[key.start:key.stop:key.step]
        else:
            raise TypeError('Index must be int, not {}'.format(type(key).__name__))

    def __len__(self)->int:
        return len(self.tracks)

    def __contains__(self, item)->bool:
        return item in self.tracks

    def __iter__(self)->Iterator[Track]:
        return iter(self.tracks)

    def append(self, item:Track):
        self.tracks.append(item)

    def extend(self, items:Iterable[Track]):
        self.tracks.extend(items)

    def remove(self, item:Track):
        self.tracks.remove(item)







if __name__ == '__main__':

    from gpx_parser.GPXTrackPoint import GPXTrackPoint as TrackPoint
    from gpx_parser.GPXTrackSegment import GPXTrackSegment as TrackSegment

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
    seg3 = TrackSegment([p4, p1])
    track1 = Track('800003627_337', '0', [seg1, seg2, seg3])
    track2 = Track('800003627_908', '1', [seg2, seg3])
    track3 = Track('800003456_123', '2', [TrackSegment([p4])])
    print(track1, track2, track3)

    gpx = GPX('1.0','gpx.py -- https://github.com/tkrajina/gpxpy')
    print(gpx)
    gpx.append(track1)
    print('1 track: ', gpx)
    gpx.extend([track2,track3])
    print('3 tracks: ', gpx)

    print('Slice: ', gpx[0:1])
    print('third track: ', gpx[2])

    for t in gpx:
        print(t)

    gpx.remove(track3)
    print(len(gpx))

