

class GPXTrackSegment:
    __slots__ = ('points')

    def __init__(self, points=None):
        self.points = points if points else []

    def __repr__(self):
        return 'GPXTrackSegment(%s)(points=%s)' % (len(self.points), self.points)

    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        if isinstance(key, int):
            return  self.points[key]

        elif isinstance(key, slice):
            return self.points[key.start:key.stop:key.step]

        else:
            raise TypeError('Index must be int, not {}'.format(type(key).__name__))


    def __iter__(self):
        return iter(self.points)

    def __contains__(self, item):
        return item in self.points

    def append(self, item):
        self.points.append(item)


    def extend(self, items):
        self.points.extend(items)

    def remove(self, item):
        self.points.remove(item)



    def get_points_no(self):
        """
        Gets the number of points in segment.

        Returns
        ----------
        num_points : integer
            Number of points in segment
        """
        return len(self.points)



# if __name__ == '__main__':
#
#     from gpx_parser.GPXTrackPoint import GPXTrackPoint
#
#     x = "50.0164596"
#     y =  "14.4547907"
#     p1 = GPXTrackPoint(x, y, '2017-11-22T07:03:36Z')
#     p2 = GPXTrackPoint(y, x, '2017-11-23T07:03:36Z')
#     p3 = GPXTrackPoint(y, y, '2017-12-23T08:11:06Z')
#     p4 = GPXTrackPoint(x, x, '2020-12-23T08:11:06Z')
#     seg = GPXTrackSegment()
#     print(seg)
#     seg.append(p1)
#     print(len(seg))
#     seg.extend([p2,p3])
#     print(seg[0])
#     print(seg)
#
#
#     for p in seg:
#         print(p)
#
#     print(p1 in seg)
#     print(p4 in seg)
#
#     print(seg[1:2:2])
#     print(seg['a'])
