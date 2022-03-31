#!/usr/bin/env python
# coding: utf-8

# In[11]:


Schema = {
    'node': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema':{
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'lat': {'required': True, 'type': 'float', 'coerce': float},
            'lon': {'required': True, 'type': 'float', 'coerce': float},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
            }
        }
    },
    'node_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    },
    'way': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
            }
        }
    },
    'way_nodes': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'node_id': {'required': True, 'type': 'integer', 'coerce': int},
                'position': {'required': True, 'type': 'integer', 'coerce': int}
            }
        }
    },
    'way_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    }
}


# In[12]:


get_ipython().system(' pip install schema --user')


# In[13]:


get_ipython().system(' pip install cerberus --user')


# In[14]:


##code provided by data.py on Lesson 13

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET






# In[15]:


import schema


# In[16]:


import cerberus


# In[17]:



OSM_PATH = 'Greenville'

NODES_PATH = 'nodes.csv'
NODE_TAGS_PATH = 'nodes_tags.csv'
WAYS_PATH = 'ways.csv'
WAY_NODES_PATH = 'ways_nodes.csv'
WAY_TAGS_PATH = 'ways_tags.csv'

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.Schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


# In[21]:


##Clean and Shape dict
##will clean postal code and state in sql queries with update statements

##look at the SC value and updates the state value
##per review notes added the update function to the data.py
def update_state_name(elem):
    if elem.tag == 'node' or elem.tag == 'way':
        for tag in elem.iter('tag'):
            if is_state_name(tag):
                if tag.attribu['v'] != 'SC':
                    print('State:', tag.attribu['v'], 'updated to SC')
                    tag.attrib['v'] = 'SC'


# UPDATE THIS VARIABLE
expected = ['Street', 'Avenue', 'Boulevard', 'Drive', 
            'Court', 'Place', 'Square', 'Lane', 'Road', 'Trail', 
            'Parkway', 'Commons', 'Way', 'Highway', 'Plaza', 'Circle']

mapping = {'Ave':'Avenue',
           'Ave.':'Avenue',
           'Blvd':'Boulevard',
           'Blvd.':'Boulevard',
           'Cir':'Circle',
           'Cir.':'Circle',
           'Rd': 'Road',
           'Palza': 'Plaza',
           '29611': 'Drive'
            }

##update street names, combination of code from the street audit file/notebook
##to update the street names
def update_street_name(elem):

    ##creating a set called street types
    street_types = defaultdict(set)
    if elem.tag == 'node' or elem.tag == 'way':
        for tag in elem.iter('tag'):
            if is_street_name(tag):
                audit_street_type(street_types, tag.attrib['v'])
            
        for st_type, ways in steet_types.items()):
        for name in ways:
            for key,value in mapping.items():
                n = street_type_re.search(name)
                if n:
                    street_type = n.group()
                    ##if street type is not in expected use mapping to update
                    if street_type not in expected:
                        if street_type in mapping:
                            better_name = name.replace(key, value)
                            
                            if better_name != name:
                                print (name), "=>", better_name
                                tag.attrib['v'] = better_name
                                return
                                
    
                    

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
  
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    update_street_name(element)
    update_state(element)
    
##node tag fields
    
    if element.tag == 'node':
        
        for n in node_attr_fields:
            node_attribs[n] = element.attrib[n]
        
        for tag in element.iter('tag'):
            k = tag.attrib['k']
              
            ##search is used to see if k has any of the characters in PROBLEMCHARS
            
            if re.search(PROBLEMCHARS, k):
                continue
                
            ##continue forces the next iteration
            else:
                pass
            ##empty dictionary to be used below
            node_tag_dict = {}
            
            ##id
            node_tag_dict['id'] = node_attribs['id']
            
            ##key and type
            #splitting k on the : if it has a value such as addr:state
            split_k = re.split('[:]', k)
            
            ##if the length of k is 1 and set key to k value and type to regular
            if len(split_k) == 1:
                node_tag_dict['key'] = k
                node_tag_dict['type'] = 'regular'
            
            ##if the length of k is 2 after split use the 1 position value for key and 0 position value for type
            elif len(split_k) == 2:
                node_tag_dict['key'] = split_k[1]
                node_tag_dict['type'] = split_k[0]
            
            ##value
            node_tag_dict['value'] = tag.attrib['v']
            tags.append(node_tag_dict)
            
            
            
        return {'node': node_attribs, 'node_tags': tags}
        
    ##way tag fields
    elif element.tag == 'way':
        for w in way_attr_fields:
            way_attribs[w] = element.attrib[w]
            
        for tag in element.iter('tag'):
            k = tag.attrib['k']
            
            ##empty dictionary
            way_tag_dict = {}
            way_tag_dict['id'] = way_attribs['id']
            
            if re.search(PROBLEMCHARS, k):
                continue
            ##continue forces the next iteration
            else:
                pass
            
            
            #splitting k on the : if it has a value such as addr:state
            split_k = re.split('[:]', k)
            
            ##if the length of k is 1 and set key to k value and type to regular
            if len(split_k) == 1:
                way_tag_dict['key'] = k
                way_tag_dict['type'] = 'regular'
            
            ##if the length of k is 2 after split use the 1 position value for key and 0 position value for type
            elif len(split_k) == 2:
                way_tag_dict['key'] = split_k[1]
                way_tag_dict['type'] = split_k[0]
            
            
            way_tag_dict['value'] = tag.attrib['v']
            ##add it to the tag dictionary
            tags.append(way_tag_dict)
    
    #iter through nd under way for way node fields
    
    #setting x to 0 and this will become the postion value 
    x = 0
    for nd in element.iter('nd'):
            ##empty dictionary to be used to add to from below statements
            nd_dict = {}
            
            nd_dict['id'] = way_attribs['id']
            #node ref value becomes node_id
            nd_dict['node_id'] = nd.attrib['ref']
            #x becomes the position value, increasing with each iteration
            nd_dict['position'] = x
            way_nodes.append(nd_dict)
            x+=1
            
            
    return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}



# In[22]:


##helper function

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=Schema):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.items())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: v for k, v in row.items()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)




# In[23]:


##main function

def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w', "utf-8") as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w', "utf-8") as nodes_tags_file,          codecs.open(WAYS_PATH, 'w', "utf-8") as ways_file,          codecs.open(WAY_NODES_PATH, 'w', "utf-8") as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w', "utf-8") as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=False)


# In[ ]:




