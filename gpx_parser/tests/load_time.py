import timeit
from functools import wraps
from typing import Callable, List
from os import path, listdir
from time import process_time

from gpx_parser.parser import GPXParser
from gpx_parser.tests.test_utils import  make_result_string, get_time


MB = 1000*1000


def timer(func:Callable)->Callable:
    @wraps(func)
    def wrapper(*args, **kwargs)->float:
        best_time = min(timeit.Timer(lambda:func(*args, **kwargs)).repeat(repeat=2, number=1))
        print(args)
        print('time = ', best_time)
        return best_time
    return wrapper


@timer
def  measure_time1(fname:str):
    with open(fname, 'r') as xml_file:
        parser = GPXParser(xml_file)
    gpx = parser.parse()


def measure_time(test_dir:str, result_dir:str):

    filenames:List[str] = [path.join(test_dir, fn) for fn in listdir(test_dir)]
    filenames.sort(key=lambda fn: path.getsize(fn))

    sizes:List[float] = [round(path.getsize(name)/MB,2) for name in filenames]

    start:float = process_time()
    times:List[float] = [n for n in map(lambda name : measure_time1(name), filenames)]
    total_time:float = process_time() - start

    string:str = make_result_string(2, ['Mbs', 'Load time'], sizes, times)
    string += '\n\n\nTotal time: {:10.2f} minutes\n'.format(total_time / 60)
    print(string)

    result_fn:str = path.join(result_dir, 'descr_try_catch_' + get_time()+ '.txt')
    with open(result_fn, 'w') as out_file:
        out_file.write(string)


TEST_DIR = "/home/olga/Documents/GPX/load_test"
RESULTS_DIR = "/home/olga/Documents/GPX/test_results"

measure_time(TEST_DIR, RESULTS_DIR)