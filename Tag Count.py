#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xml.etree.ElementTree as ET
from collections import defaultdict
import re
import pprint
import re
import xml.etree.cElementTree as ET


# In[2]:


## code from udacity lessons

osmfile = 'Greenville'

def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename, events=('start', )):
        if elem.tag not in tags:
            tags[elem.tag] = 1
        else:
            tags[elem.tag] += 1
    return tags

def test():

    tags = count_tags(osmfile)
    pprint.pprint(tags)
    

if __name__ == "__main__":
    test()


# In[ ]:




