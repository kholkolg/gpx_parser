from datetime import datetime
from typing import Callable


DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def parse_time(string:str, time_format:str=DATE_FORMAT, parser:Callable = datetime.strptime)->datetime:
    return parser(string, time_format)


