#!/usr/bin/env python
# coding: utf-8

# In[1]:


##code taken from lesson video example

import xml.etree.cElementTree as ET
from collections import defaultdict
import re

##open street maps file
osm_file = open('Greenville', 'r')

#use re to 
street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()

        street_types[street_type] += 1


# In[4]:


##creates dictionary
def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print ('%s: %d' % (k, v))


# In[5]:


##returns the street
def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")


# In[6]:


##parse the file
def audit():
    for event, elem in ET.iterparse(osm_file):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])    
    print_sorted_dict(street_types)    

if __name__ == '__main__':
    audit()


# In[ ]:




