# gpx-parser

Simple parser for loading basic information about track points from .gpx files.
Inside the gpx tag parser only extracts trk, trkseg, and trkpt tags.
All other tags are ignored.
Resulting GPX structure is a container with track list. Each track is in it's turn a list of segments, and segment is
a list of track points, the leaf elements of the structure.
GPX, GPXTrack, an GPXTrackSegment support most of the list methods.


### Prerequisites
Python 3.4 or higher

xml or lxml


### Examples of usage
```python
import gpx_parser as parser

with open('file_name', 'r') as gpx_file:
    gpx = parser.parse(gpx_file)
print("{} tracks loaded".format(len(gpx)))
```

```
for track in gpx:
    print('Track with {} segments and {} points'.
          format(len(track), track.get_points_no()))
    for segment in track:
        print('Segment with %s points % len(segment))
        for point in segment:
            print(point)
            
```
##### GPX
  
```
gpx.tracks                   # list of tracks
gpx.version                  # str or None
gpx.creator                  # str or None
gpx.points                   # list of all points from all tracks

len(gpx))                    # number of tracks in gpx
gpx.get_points_no()          # total number of points in all segments of all tracks
gpx[0]                       # 0th track, same as gpx.tracks[0]
gpx[1:3]                     # = gpx.tracks[1:3]
gpx.contains(track)          # = gpx.tracks.contains(track)
gpx.append(track)            # = gpx.tracks.append(track)
gpx.extend(tracks)           # = gpx.tracks.extend(tracks)
gpx.remove(track)            # = gpx.tracks.remove(tracks)
gpx.clone()                  #  returns deepcoopy of the object   

gpx.to_xml()                 # str, point with xml tags
gpx.length_2d()              # total 2d  distance of the track
gpx.get_bounds()             # min and max latitude and logitude
gpx.get_time_bounds()        # start and end time
gpx.walk()                   # generator, yields (point, track_num, segment_num, point_num)

```
##### GPXTrack
 ```
 track.name                 # str or None
 track.number               # int or None
 track.segments             # list of all segments in the track
 track.points               # list of all points from all segments
 
 len(track)                 # number of segments in the track
 track[0]                   #
 track[::2]                 # shorcuts for
 track.contains(segment)    # track.segments
 track.append(segment)      #
 track.extend(segmengs)     #
 track.remove(segment)      #

 
 track.to_xml()             #
 track.length_2d()          # same as for gpx
 track.get_bounds()         #
 track.get_time_bounds()    #
 track.get_points_no()      #
 track.clone()              #
 
 track.get_duration()      # float, duration of track in seconds
 track.remove_empty()      # removes empty segments from the track
 
```
##### GPXTrackSegment

```
 seg.points               # list of points in the segment

 len(seg)                 # 
 seg[0]                   #
 seg[::2]                 # shortcuts for
 seg.contains(segment)    # seg.points
 seg.append(segment)      #
 seg.extend(segmengs)     #
 seg.remove(segment)      #

 
 seg.to_xml()             #
 seg.length_2d()          # same as for gpx
 seg.get_bounds()         #
 seg.get_time_bounds()    #
 seg.get_points_no()      #
 seg.clone()              # 
 
 seg.get_duration()       # float, duration of track in seconds
 seg.remove_empty()       # removes empty segments from the track

```
 ##### GPXTrackPoint
 ```
 point.latitude         
 point.longitude        
 point.time             
 
 point.to_xml()         
            
 point.distance_2d(other_point)          # distance in meters
 point.time_difference(other_point)      # time in seconds, or None, if one of the points doesn't have time attribute.
 point.speed_between(other_point)        # speed, i m/s, or None, if one of the points doesn't have time attribute.
```