from datetime import timedelta, datetime
from typing import Union, Optional, List, Iterator, Iterable, Tuple
import copy as mod_copy


from gpx_parser.GPXTrackPoint import GPXTrackPoint as TrackPoint, GPXTrackPoint


class GPXTrackSegment:
    __slots__ = ('_points')

    def __init__(self, points:Optional[List[TrackPoint]]=None):
        self._points = points if points else []

    def __repr__(self)-> str:
        return 'GPXTrackSegment(%s)(points=%s)' % (len(self._points), self._points)

    def __len__(self)-> int:
        return len(self._points)

    def __getitem__(self, key:Union[int, slice])-> Union[TrackPoint, List[TrackPoint]]:
        if isinstance(key, int):
            return  self.points[key]

        elif isinstance(key, slice):
            return self.points[key.start:key.stop:key.step]

        else:
            raise TypeError('Index must be int, not {}'.format(type(key).__name__))


    def __iter__(self)->Iterator[TrackPoint]:
        return iter(self.points)

    def __contains__(self, item:TrackPoint)->bool:
        return item in self.points

    @property
    def points(self)->List[TrackPoint]:
        return self._points

    @points.setter
    def points(self, points:List[TrackPoint]):
        self._points = points

    def append(self, item:TrackPoint):
        self._points.append(item)


    def extend(self, items:Iterable[TrackPoint]):
        self._points.extend(items)

    def remove(self, item:TrackPoint):
        self._points.remove(item)


    def get_points_no(self)->int:
        """
        Gets the number of points in segment.
        TODO remove??
        Returns
        ----------
        num_points : integer
            Number of points in segment
        """
        return len(self._points)


    def reduce_points(self, min_distance:float)->None:
        reduced_points = [self.points[0],]
        for point in self.points[1:]:
            if reduced_points:
                distance = reduced_points[-1].distance_2d(point)
                if distance >= min_distance:
                    reduced_points.append(point)
        self.points = reduced_points


    def length_2d(self)->float:
        return sum(map(lambda t :t[0].distance_2d(t[1]), zip(self.points[:-1],
                                                            self.points[0:])))


    def split(self, point_no:int)->('GPXTrackSegment','GPXTrackSegment'):

        part_1 = self.points[:point_no + 1]
        part_2 = self.points[point_no + 1:]
        return GPXTrackSegment(part_1), GPXTrackSegment(part_2)

    def get_time_bounds(self)->Tuple[datetime, datetime]:
        """
        Gets the time bound (start and end) of the segment.

        returns
        ----------
        time_bounds : TimeBounds named tuple
            start_time : datetime
                Start time of the first segment in track
            end time : datetime
                End time of the last segment in track
        """
        start_time = None
        end_time = None

        for point in self.points:
            if point.time:
                if not start_time:
                    start_time = point.time
                if point.time:
                    end_time = point.time

        return start_time, end_time

    def get_bounds(self)->Tuple[float, float,float, float]:
        """
        Gets the latitude and longitude bounds of the segment.

        Returns
        ----------
        bounds : Bounds named tuple
            min_latitude : float
                Minimum latitude of segment in decimal degrees [-90, 90]
            max_latitude : float
                Maxium latitude of segment in decimal degrees [-90, 90]
            min_longitude : float
                Minium longitude of segment in decimal degrees [-180, 180]
            max_longitude : float
                Maxium longitude of segment in decimal degrees [-180, 180]
        """
        min_lat:float = min(map(lambda pt : pt.latitude, self.points))
        max_lat:float = max(map(lambda pt : pt.latitude, self.points))
        min_lon:float = min(map(lambda pt : pt.longitude, self.points))
        max_lon:float = max(map(lambda pt : pt.longitude, self.points))

        return min_lat, max_lat, min_lon, max_lon


    def get_duration(self)->Optional[float]:

        if len(self.points) < 2:
            return 0

        first:GPXTrackPoint = self.points[0]
        last:GPXTrackPoint = self.points[-1]
        if not first.time or not last.time:
            print('Time data is missing')
            return None

        return (last.time - first.time).total_seconds()


    def get_location_at(self, time:datetime)->Optional[GPXTrackPoint]:
        """
        Gets approx. location at given time. Note that, at the moment this
        method returns an instance of GPXTrackPoint in the future -- this may
        be a mod_geo.Location instance with approximated latitude, longitude
        and elevation!
        """
        if not self.points:
            return None

        first = 0
        while not self.points[first]:
            first += 1
        if first.time >= time:
            return self.points[first]

        last = -1
        while not last.time:
            last -= 1
        if last.time <= time:
            return self.points[last]

        p1 = self.points[first]
        p2 = self.points[last]
        lat:float = round((p1.latitude+p2.latitude)/2. ,7)
        lon:float = round((p1.longitude + p2.longitude) / 2., 7)
        return GPXTrackPoint(str(lat), str(lon), None)

    def get_nearest_location(self, location:TrackPoint)->Optional[Tuple[GPXTrackPoint, int]]:
        """ Return the (location, track_point_no) on this track segment """
        if not self.points:
            return None

        result:GPXTrackPoint = None
        current_distance:float = None
        result_track_point_no:int = None
        for i in range(len(self.points)):
            track_point:GPXTrackPoint = self.points[i]
            if not result:
                result = track_point
            else:
                distance:float = track_point.distance_2d(location)
                if not current_distance or distance < current_distance:
                    current_distance = distance
                    result = track_point
                    result_track_point_no = i

        return result, result_track_point_no

    def clone(self):
        return mod_copy.deepcopy(self)



if __name__ == '__main__':

    x = "50.0164596"
    y =  "14.4547907"
    p1 = TrackPoint(x, y, '2017-11-22T07:03:36Z')
    p2 = TrackPoint(y, x)
    p3 = TrackPoint(y,y, '2617-11-13T08:11:09Z')
    p4 = TrackPoint(x, x)
    seg = GPXTrackSegment()
    print('Empty segment: ', seg)
    seg.append(p1)
    print('Length,  1 point: ', len(seg))
    seg.extend([p2,p3])
    print('0th element: ', seg[0])
    print('Segment with 3 points: ', seg)
    print('seg.points: ', seg.points)
    print('bounds %s %s %s %s'% seg.get_bounds())

    print('Point in segment: %s, not in segment: %s ' % (
        p1 in seg, p4 in seg))

    print('Slice: ', seg[1:2:2])
    print('Iterator:')
    for p in seg:
        print(p)
    print('Split 1: %s 2 %s'% seg.split(1))

