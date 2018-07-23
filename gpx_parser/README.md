# gpx-parser

Simple parser for loading  track points from .gpx files.

### GPX Data
Typical project data consists of tracks, track segments, 
and trackpoints with coordinates and optitonal timestamp. 

##### Sample .gpx file
```
<gpx version="1.0" creator="gpx_parser.py ">
  <trk>
    <name>800003627_337</name>
    <number>0</number>
    <trkseg>
      <trkpt lat="50.0164596" lon="14.4547907">
        <time>2017-11-22T07:03:36Z</time>
      </trkpt>
      <trkpt lat="50.0164596" lon="14.4547907">
        <time>2017-11-22T07:07:42Z</time>
      </trkpt>
    </trkseg>
  </trk>
</gpx>
```
Inside the gpx tag parser only extracts trk, trkseg, and trkpt tags.
All other tags are ignored.

### Prerequisites
Python 3.4 or higher.

### Examples of usage
```python
import gpx_parser as parser

with open('file_name', 'r') as gpx_file:
    gpx = parser.parse(gpx_file)
print("{} tracks loaded".format(len(gpx)))

for track in gpx:
    print('Track #{}, "{}", with {} segments and {} points'.
          format(track.number, track.name, 
                 len(track), track.get_points_no()))
    print('Min latitude = %.2f, max latitude = %.2f, \
           min longitude = %.2f, max longitude = %.2f' % track.get_bounds())
    print('Start %s, end %s' % track.get_time_bounds())
    print('Total length = %.2f' % track.length_2d())

    for segment in track:
        print('Segment: {} points, length = ')
        print('Bounds %.2f, %.2f, %.2f, %.2f' % segment.get_bounds())
        print('Time bounds %.2f, %.2f' % segment.get_time_bounds())
        
        for point in segment:
            print('Point: lat = %.2f, lon = %.2f' % (point.latitude, point.longitude))
            
```



