from re import sub

try:
    import xml.etree.ElementTree as mod_etree
except ImportError:
    import xml.etree.ElementTree as mod_etree

#from sys import  getsizeof

ElementTree = mod_etree.ElementTree


def load_xml(xml_string:str, ET = mod_etree) ->ElementTree:
    """
    :param filename: xml file
    :return: ElementTree
    """
    xml_string = sub(r'\sxmlns="[^"]+"', '', xml_string , count=1)
    #print(xml_string)
    #print('Size of xml string = ', getsizeof(xml_string))

    root = ET.fromstring(xml_string)
    #print('Size of etree = ', getsizeof(root))
    return root




if __name__ == '__main__':

    fn = '/home/olga/Documents/GPX/load_test/traces10.gpx'
    with open(fn, 'r') as xml_file:
        load_xml(xml_file.read())

