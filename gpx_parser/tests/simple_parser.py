from time import process_time
from os import path, listdir
import timeit
from gpx_parser.xml_loader import  load_xml
from roadmaptools.load_test.test_utils import  make_result_string



def parse_file(filename:str)->list:
    """
    Parse .gpx file to list of elements.
    Tracks, consisting of list of segments, consisting of list of points.
    Point is a dictionary with latitude, longitude, and time

    :param name: filename
    :return: list of tracks
    """

    root = load_xml(filename)
    tracks = []
    for track in root.iterfind('trk'):
        new_track = []
        for segment in track.iterfind('trkseg'):
            new_segment = []
            for point in segment.iterfind('trkpt'):
                new_point = point.attrib #attrib is a dictionary
                #print(point)
                new_point['time'] = point.find('time').text
                print(new_point)
                new_segment.append(new_point)
            new_track.append(new_segment)
        # print('Name: ' + track[0].text)
        # print('Number: ' + track[1].text)
        tracks.append(new_track)
    return tracks


def test_dir(dir:str, result_file:str):
    mbs = []
    times = []
    start = process_time()

    filenames = [path.join(dir, fn) for fn in listdir(dir)]
    filenames.sort(key=lambda fn: path.getsize(fn))

    for name in filenames:
        mbs.append(round(path.getsize(name) / MB, 2))
        print("File {}, size {:0.2f} Mb".format(name, path.getsize(name) / MB))
        best_time = min(timeit.Timer(lambda: parse_file(name)).repeat(repeat=10, number=1))
        print('{:0.2}'.format(best_time))
        times.append(best_time)

    total_time = process_time() - start
    string = make_result_string(2, ['Mbs', 'Time'], mbs, times)
    string += '\n\n\nTotal time: {:10.2f} minutes\n'.format(total_time / 60)
    print(string)

    with open(result_file, 'w') as out_file:
        out_file.write(string)


if __name__ == '__main__':
    fn =  '/home/olga/Documents/GPX/test1.gpx'
    with open(fn, 'r') as f:
        gpx = parse_file(f.read())
    print(gpx)
    #test_dir(TEST_DIR, path.join(RESULTS_DIR, 'simple_parser_timeit'+ get_time() +'.txt'))