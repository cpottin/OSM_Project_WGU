#!/usr/bin/env python
# coding: utf-8

# In[9]:


##from video lessons
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


# In[10]:


osm_file = 'Greenville'
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

##Expected street types
expected = ['Street', 'Avenue', 'Boulevard', 'Drive', 'Court', 'Place', 'Square', 'Lane', 'Road', 'Trail', 'Parkway', 'Commons', 'Way', 'Highway', 'Plaza', 'Circle']

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


# In[11]:



def is_street_name(elem):
    return (elem.attrib['k'] == 'addr:street')


# In[12]:


def audit(osmfile):
    osm_file = open(osmfile, 'r')
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=('start',)):

        if elem.tag == 'node' or elem.tag == 'way':
            for tag in elem.iter('tag'):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    print(street_types)
    return street_types

audit('Greenville')


# In[ ]:




