from typing import Optional, List, Union, Iterator, Iterable, Tuple
import math as mod_math

from gpx_parser.GPXTrack import GPXTrack as Track


class GPX:
    """
    
    """

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

    def to_xml(self)->str:
        #TODO
        return 'Not yet implemented'
        

    def reduce_points(self, max_points_no=None, min_distance=None)->None:
        """
        Reduces the number of points. Points will be updated in place.

        Parameters
        ----------

        max_points : int
            The maximum number of points to include in the GPX
        min_distance : float
            The minimum separation in meters between points
        """
        if max_points_no is None and min_distance is None:
            raise ValueError("Either max_point_no or min_distance must be supplied")

        if max_points_no is not None and max_points_no < 2:
            raise ValueError("max_points_no must be greater than or equal to 2")

        points_no = len(list(self.walk()))
        if max_points_no is not None and points_no <= max_points_no:
            # No need to reduce points only if no min_distance is specified:
            if not min_distance:
                return

        length = self.length_2d()

        min_distance = min_distance or 0
        max_points_no = max_points_no or 1000000000

        min_distance = max(min_distance, mod_math.ceil(length / float(max_points_no)))

        for track in self.tracks:
            track.reduce_points(min_distance)



    def get_time_bounds(self)->Tuple[float, float]:
        """
        Gets the time bounds (start and end) of the GPX file.

        Returns
        ----------
        time_bounds : TimeBounds named tuple
            start_time : datetime
                Start time of the first segment in track
            end time : datetime
                End time of the last segment in track
        """
        start_time = None
        end_time = None

        for track in self.tracks:
            track_start_time, track_end_time = track.get_time_bounds()
            if not start_time:
                start_time = track_start_time
            if track_end_time:
                end_time = track_end_time

        return start_time, end_time

    def get_bounds(self):
        """
        Gets the latitude and longitude bounds of the GPX file.

        Returns
        ----------
        bounds : Bounds named tuple
            min_latitude : float
                Minimum latitude of track in decimal degrees [-90, 90]
            max_latitude : float
                Maxium latitude of track in decimal degrees [-90, 90]
            min_longitude : float
                Minium longitude of track in decimal degrees [-180, 180]
            max_longitude : float
                Maxium longitude of track in decimal degrees [-180, 180]
        """
        min_lat = None
        max_lat = None
        min_lon = None
        max_lon = None
        for track in self.tracks:
            bounds = track.get_bounds()

            if not mod_utils.is_numeric(min_lat) or bounds.min_latitude < min_lat:
                min_lat = bounds.min_latitude
            if not mod_utils.is_numeric(max_lat) or bounds.max_latitude > max_lat:
                max_lat = bounds.max_latitude
            if not mod_utils.is_numeric(min_lon) or bounds.min_longitude < min_lon:
                min_lon = bounds.min_longitude
            if not mod_utils.is_numeric(max_lon) or bounds.max_longitude > max_lon:
                max_lon = bounds.max_longitude

        return GPXBounds(min_lat, max_lat, min_lon, max_lon)

    def get_points_no(self):
        """
        Get the number of points in all segments of all track.

        Returns
        ----------
        num_points : integer
            Number of points in GPX
        """
        result = 0
        for track in self.tracks:
            result += track.get_points_no()
        return result



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


