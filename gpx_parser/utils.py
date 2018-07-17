import datetime as mod_datetime
from typing import List

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def parse_time(string:str, time_format=DATE_FORMAT, parser = mod_datetime.datetime.strptime):
    return parser(string, time_format)


def get_slice(array:List, slice_item:slice)->List:
    return array
