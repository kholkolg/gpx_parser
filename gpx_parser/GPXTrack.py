

class GPXTrack:

    __slots__ = ('name', 'number', 'segments')

    def __init__(self, name=None, number=None, segments=None):
        self.name = name
        self.number = number
        self.segments = segments if segments else [] # use sets instead??

    def __repr__(self):
        return 'GPXTrack(%s  %s)(%s)(segments=%s)' % (self.name, self.number, len(self.segments), self.segments)

    def __len__(self):
        return len(self.segments)

    def __iter__(self):
        return iter(self.segments)



    def __getitem__(self, key):
        if isinstance(key, int):
            return self.segments[key]
        elif isinstance(key,slice):
            return self.segments[key.start:key.stop:key.step]
        else:
            raise TypeError('Index must be int, not {}'.format(type(key).__name__))


    def __contains__(self, item):
        return item in self.segments

    def append(self, item):
        self.segments.append(item)

    def extend(self, items):
        self.segments.extend(items)

    def remove(self,item):
        self.segments.remove(item)


    def get_points_no(self)->int:
        """

        :return: total number of points in all the segments of the track
        """
        return sum([len(seg) for seg in self.segments])


# if __name__ == '__main__':
#
#     from gpx_parser.GPXTrackPoint import GPXTrackPoint
#     from gpx_parser import GPXTrackSegment
#
#     x = "50.0164596"
#     y =  "14.4547907"
#     p1 = GPXTrackPoint(x, y, '2017-11-22T07:03:36Z')
#     p2 = GPXTrackPoint(y, x, '2017-11-23T07:03:36Z')
#     p3 = GPXTrackPoint(y, y, '2017-12-23T08:11:06Z')
#     p4 = GPXTrackPoint(x, x, '2020-12-23T08:11:06Z')
#     seg1 = GPXTrackSegment([p1, p2, p3])
#     seg2 = GPXTrackSegment([p2, p3, p4])
#     track = GPXTrack('800003627_337', '0')
#     print(track)
#     track.append(seg1)
#     print('Len 1: ',  len(track))
#     seg3 = GPXTrackSegment([p4, p1])
#     track.extend([seg2, seg3])
#     print('Len 2: ', len(track) , 'Points: ', track.get_points_no())
#     print('Slice: ', track[2:])
#
#     for s in track:
#         print(s)
#
#     track.remove(seg1)
#     print('Len 3: ', len(track))
#     #track.remove(p1)