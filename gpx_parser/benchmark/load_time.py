import timeit
from functools import wraps
from typing import Callable, List
from os import path, listdir
from time import process_time


from gpxpy.parser import GPXParser as OriginalParser
from ..parser import GPXParser as MyParser
from .test_utils import  make_result_string, get_time
from ..GPX import  GPX


MB = 1000*1000


def timer(func:Callable)->Callable:
    @wraps(func)
    def wrapper(*args, **kwargs)->float:
        best_time = min(timeit.Timer(lambda:func(*args, **kwargs)).repeat(repeat=10, number=1))
        print('time = ', best_time)
        return best_time
    return wrapper



@timer
def  measure_load1(fname:str):
    with open(fname, 'r') as xml_file:
        parser =  MyParser(xml_file)
    parser.parse()


@timer
def  measure_load2(fname:str):
    with open(fname, 'r') as xml_file:
        parser =  OriginalParser(xml_file)
    parser.parse()


@timer
def convert_values(gpx_content:GPX):
    all_points = [pt for tr in gpx_content for seg in tr for pt in seg]
    for i in range(10):
        coords = [c for c in map(lambda  pt : (pt.latitude, pt.longitude), all_points)]


def measure_conversion(fname:str):
    with open(fname, 'r') as xml_file:
        parser = MyParser(xml_file)
        gpx = parser.parse()
        return convert_values(gpx)



def measure_time(func:Callable, test_dir:str, result_dir:str, result_name:str, *args):

    filenames:List[str] = [path.join(test_dir, fn) for fn in listdir(test_dir)]
    filenames.sort(key=lambda fn: path.getsize(fn))

    sizes:List[float] = [round(path.getsize(name)/MB,2) for name in filenames]
    start:float = process_time()
    times:List[float] = [n for n in map(lambda name : func(name), filenames)]
    total_time:float = process_time() - start
    print(times)
    string:str = make_result_string(2, ['Mbs', 'Time'], sizes, times)
    string += '\n\n\nTotal time: {:10.2f} minutes\n'.format(total_time / 60)
    print(string)

    result_fn:str = path.join(result_dir, result_name + get_time() + '.txt')
    with open(result_fn, 'w') as out_file:
        out_file.write(string)



TEST_DIR = "/home/olga/Documents/GPX/load_test"
RESULTS_DIR = "/home/olga/Documents/GPX/test_results"

measure_time(measure_load1, TEST_DIR, RESULTS_DIR,  'final_load_mine_')
measure_time(measure_load2, TEST_DIR, RESULTS_DIR,  'final_load_other_')
measure_time(measure_conversion, TEST_DIR, RESULTS_DIR,  'final_load_conversion_mine_')
