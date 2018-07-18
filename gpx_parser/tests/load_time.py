from os import listdir, path
import timeit
from time import process_time
from matplotlib import pyplot as plt
import numpy as np
from gpx_parser.tests.test_utils import make_result_string, get_time
from gpx_parser.tests.cons import  MB, TEST_DIR, RESULTS_DIR

import gpx_parser as gpxpy


def load_gpx(filepath) :
    with open(filepath, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    return gpx



def test_dir(dir:str, result_filename:str, graph=False):
    '''
    Benchmarks loading of xml from files in given directory.
    Saves results to file.

    :param dir: path to directory with test files
    :param result_filename: where to save results
    :param graph: show and save graphs
    :return:
    '''
    filenames = [path.join(dir, fn) for fn in listdir(dir)]
    filenames.sort(key=lambda fn: path.getsize(fn))
    mbs = []
    times = []

    global_start = process_time()
    for name in filenames:
        print("File {}, size {:0.2f} Mb".format(name, path.getsize(name)/MB))
        mbs.append(round(path.getsize(name)/MB, 2))
        best_time = min(timeit.
                        Timer(lambda: load_gpx(name)).
                        repeat(repeat=10, number=1))
        times.append(best_time)
        print(best_time)

    total_time = process_time() - global_start

    string = make_result_string(2, ['Mbs', 'Load time'], mbs, times)
    string += '\n\n\nTotal time: {:10.2f} minutes\n'.format(total_time/60)
    print(string)

    with open(result_filename,'w') as out_file:
        out_file.write(string)

    if graph:
        fig, ax = plt.subplots()
        line1, = ax.plot(mbs, times)
        line1.set_label('XML')
        ax.legend(loc = 'best').draggable()
        plt.title("From file to xml")
        plt.xlabel("File size, Mb")
        plt.xticks(np.arange(min(mbs) - 10, max(mbs) + 10, step = 50))
        plt.ylabel('Loading time, sec')
        ax.grid(color='gray', linestyle='dotted')
        plt.show()
        fig.savefig(result_filename + '.png', dpi = 300)


if __name__ == '__main__':
    test_name = 'decorators_'
    test_dir(TEST_DIR, path.join(RESULTS_DIR, test_name + get_time() +'.txt'))
