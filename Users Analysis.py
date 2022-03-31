#!/usr/bin/env python
# coding: utf-8

# In[11]:


#code from lesson 13 Exploring users

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    return


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if element.tag == 'node' or element.tag == 'way' or element.tag == 'relation':
            users.add(element.attrib['user'])
        pass

    return users



def test():

    users = process_map('Greenville')
    pprint.pprint(users)
    assert len(users) == 6



if __name__ == "__main__":test()


# In[12]:



def get_user(element):
    return


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        try:
            users.add(element.attrib['uid'])
        except KeyError:
            continue

    return users


def test():

    users = process_map('Greenville')
    pprint.pprint(len(users))

if __name__ == "__main__":
    test()


# In[ ]:




