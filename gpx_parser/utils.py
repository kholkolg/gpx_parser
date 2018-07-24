from datetime import datetime
from typing import Callable, Dict, Optional



def parse_time(string:str, parser:Callable = datetime.strptime)->datetime:
    DATE_FORMATS = [ "%Y-%m-%dT%H:%M:%S.%fZ", '%Y-%m-%dT%H:%M:%SZ']
    for time_format in DATE_FORMATS:
        try:
            return parser(string, time_format)
        except ValueError:
            pass
    raise ValueError('Invalid time format in string %s' % string)


def to_xml(tag:str, attributes:Optional[Dict[str, str]]=None,
           content:Optional[str]=None)->str:
    attributes = attributes or {}
    result = []
    result.append('\n' +'<{0}'.format(tag))

    if attributes:
        for k,v in attributes.items():
            result.append(' %s="%s"' % (k, v))

    if content is None:
        result.append('/>')

    result.append('>%s</%s>' % (content, tag))


    return ''.join(result)


