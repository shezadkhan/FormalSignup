import lxml.etree as ET
from lxml.etree import XMLParser
import re


def FormalNumber(html):
    parser = XMLParser(ns_clean=True, recover=True)
    tree = ET.fromstring(html, parser)
    tmp = []
    for elem in tree.iter():
        if elem.tag == '{http://www.w3.org/1999/xhtml}div':
            for ii in elem.items():
                if (ii[0].lower() == 'class') and ('cme_center' in ii[1]):
                    tmp.append(elem)

    for i in tmp[0]:
        for ii in i.items():
            item = i

    lnk = item.getchildren()[0]
    m = re.search('(?<=http://castlejcr.com/index.php/formals/view/)\w+', lnk.items()[0][1])
    if m == None:
        return False
    else:
        return m.group(0)
