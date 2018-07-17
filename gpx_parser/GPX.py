class GPX:

    __slots__ = ('version', 'creator', 'tracks')


    def __init__(self, version = None, creator = None, tracks = None):
        self.version = version
        self.creator = creator
        self.tracks = tracks if tracks else []


    def __repr__(self):
        return 'GPX(%s)(tracks=%s)' % (len(self.tracks), self.tracks)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.tracks[key]
        elif isinstance(key, slice):
            return self.tracks[key.start:key.stop:key.step]
        else:
            raise TypeError('Index must be int, not {}'.format(type(key).__name__))

    def __len__(self):
        return len(self.tracks)

    def __contains__(self, item):
        return item in self.tracks

    def __iter__(self):
        return iter(self.tracks)


    def append(self, item):
        self.tracks.append(item)

    def extend(self, items):
        self.tracks.extend(items)

    def remove(self, item):
        self.tracks.remove(item)







# if __name__ == '__main__':
#
#     from gpx_parser.GPXTrackPoint import GPXTrackPoint
#     from gpx_parser import GPXTrackSegment
#     from gpx_parser import GPXTrack
#
#     x = "50.0164596"
#     y =  "14.4547907"
#     p1 = GPXTrackPoint(x, y, '2017-11-22T07:03:36Z')
#     p2 = GPXTrackPoint(y, x, '2017-11-23T07:03:36Z')
#     p3 = GPXTrackPoint(y, y, '2017-12-23T08:11:06Z')
#     p4 = GPXTrackPoint(x, x, '2020-12-23T08:11:06Z')
#     seg1 = GPXTrackSegment([p1, p2, p3])
#     seg2 = GPXTrackSegment([p2, p3, p4])
#     seg3 = GPXTrackSegment([p4, p1])
#     track1 = GPXTrack('800003627_337', '0', [seg1, seg2, seg3])
#     track2 = GPXTrack('800003627_908', '1', [seg2, seg3])
#     track3 = GPXTrack('800003456_123', '2', [GPXTrackSegment([p4])])
#     print(track1, track2, track3)
#
#     gpx = GPX('1.0','gpx.py -- https://github.com/tkrajina/gpxpy')
#     print(gpx)
#     gpx.append(track1)
#     print('1 track: ', gpx)
#     gpx.extend([track2,track3])
#     print('3 tracks: ', gpx)
#
#     print('Slice: ', gpx[0:1])
#     print('2 item: ', gpx[2])
#
#     for t in gpx:
#         print(t)
#
#     gpx.remove(track3)
#     print(len(gpx))

