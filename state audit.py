#!/usr/bin/env python
# coding: utf-8

# In[22]:


##clean the data, using street audit as starter code

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "Greenville"


# In[12]:


def is_state_name(elem):
    return (elem.attrib['k'] == "addr:state")

state_types = defaultdict(int)

##look at the SC value, if the state name doesn't match SC print name
def audit_state_name(state_types, state_name):
    if state_name != 'SC':
        state_types[state_name] +=1
        print(state_name)

#does the work iter over the file
for event, elem in ET.iterparse(OSMFILE, events = ('start',)):
    if elem.tag == 'node' or elem.tag =='way':
        for tag in elem.iter('tag'):
            if is_state_name(tag):
                audit_state_name(state_types, tag.attrib['v'])



# In[30]:




##look at the SC value, if the state name doesn't match SC print name
def update_state_name(elem):
    if elem.tag == 'node' or elem.tag == 'way':
        for tag in elem.iter('tag'):
            if is_state_name(tag):
                if tag.attribu['v'] != 'SC':
                    print('State:', tag.attribu['v'], 'updated to SC')
                    tag.attrib['v'] = 'SC'
                    

  


# In[ ]:




