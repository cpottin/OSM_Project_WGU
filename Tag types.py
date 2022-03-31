#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

tree = ET.parse('Greenville')

mylist = []
for elem in tree.iter():
    mylist.append(elem.tag)

mylist = list(set(mylist))

print(mylist)


# In[ ]:




