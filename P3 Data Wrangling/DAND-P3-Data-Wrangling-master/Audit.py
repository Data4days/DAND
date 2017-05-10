
# coding: utf-8

# In[1]:

"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

osmfile = "sample.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons","Close","Crescent","Grove"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Straat": "Street",
            "Street)": "Street",
            "street": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
            "RD": "Road",
            "road": "Road",
            "Cresent": "Crescent",
            "Ext": "Extension",
            "Ext.": "Extension"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):

    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            if street_type in mapping.keys():
                name = re.sub(street_type_re, mapping[street_type], name)

    return name


def audit_postcode(osmfile):
    osm_file = open(osmfile, "r")
    postal = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == "addr:postcode":
                    if len(tag.attrib['v']) != 4:
                        print(tag.attrib['v'])
                    
    osm_file.close()

    
def test():
    
    st_types = audit(osmfile)
    pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        if st_type in mapping:
            for name in ways:
                better_name = update_name(name, mapping)
                print name, "=>", better_name
            


if __name__ == '__main__':
    test()
    audit_postcode(osmfile)


# In[ ]:



