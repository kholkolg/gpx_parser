from datetime import datetime
from typing import Callable, Dict, Optional


DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def parse_time(string:str, time_format:str=DATE_FORMAT, parser:Callable = datetime.strptime)->datetime:
    return parser(string, time_format)


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


