
# coding: utf-8

# ## Data Auditing
# 
# Before submitting data to the database, we first need to investigate data if there is any problem in it. We declare our packages to use, and original file name. Then, we count tags in the file.

# In[5]:

import xml.etree.cElementTree as ET
import re
from collections import defaultdict
import pprint

OSM_FILE = "C:\\jupyter\\\openmapstreet\\istanbul_turkey.osm"

# A function to show some elements declared in parameters
def get_elements(filename):
    context = iter(ET.iterparse(filename, events=('start', 'end')))
    _, root = next(context) 
    
    for event, elem in context:
        if event == 'end':
            yield elem
            root.clear()

# A function to count elements in the node
def count_elements(elements):
    tags = {}
    
    for element in elements:
        if element.tag not in tags:
            tags[element.tag] = 1
        else:
            tags[element.tag] += 1
            
    return tags

elements = get_elements(OSM_FILE)
tags_counted = count_elements(elements)

print("Elements counted in the file:")
print(tags_counted)


# In the following we are building XML file structure.

# In[7]:

# A function to build the hierarchy of the file.

def get_element_hierarchy(root):
    tags = {}

    for element in root:
        sub_tags = get_element_hierarchy(element)
        
        if element.tag not in tags:
            tags[element.tag] = {}
            
        if len(list(sub_tags)) > 0:
            tags[element.tag] = sub_tags
            
    return tags

tree = ET.parse(OSM_FILE)
root = tree.getroot()

tags = get_element_hierarchy(root)

print("The hierarchy of the XML file")
pprint.pprint(tags)


# With this information, we know the tags in the XML file. So, let's investigate these elements' attributes.

# In[8]:

# A function to get all element within the tags sent as parameter

def get_elements_in(filename, tag):
    context = iter(ET.iterparse(filename, events=('start', 'end')))
    _, root = next(context) 
    
    for event, elem in context:
        if event == 'end' and elem.tag == tag:
            yield elem
            root.clear()

elements_attributes = {}

# We counted all the tags in the file, so we can iterate.

for tag in tags_counted:
    elements = get_elements_in(OSM_FILE, tag)

    for element in elements:
        attributes = []

        for attribute in element.attrib:
            if attribute not in attributes:
                attributes.append(attribute)

        if element.tag not in elements_attributes:
            elements_attributes[element.tag] = attributes
        else:
            for attribute in attributes:
                if attribute not in elements_attributes[element.tag]:
                        elements_attributes[element.tag].append(attribute)

print("Attributes of the elements")
pprint.pprint(elements_attributes)


# We need to give special attention to the <i>tag</i> tag, because it has <i>k</i> and <i>v</i> attributes, very suitable for entering data casually. Let's investigate <i>k</i> attribute's values.

# In[10]:

k_tag_values = []

elements = get_elements_in(OSM_FILE, 'tag')

for elem in elements:
    if elem.get('k') not in k_tag_values:
        k_tag_values.append(elem.get('k'))

k_tag_values.sort()
pprint.pprint(k_tag_values)


# As we can see there are lots of different <i>k</i> attribute in the <i>tag</i> tag. But we will be only interested in <i>addr:street</i> and <i>addr:postcode</i> values becuase of the project scope. By the way, we see in the output, some values are in lowercase but not all, and problematic characters. Let's see how many:

# In[11]:

# Regex declerations for key type

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Function to search 'k' element attribute's context to find any anomalies

def key_type(element, keys):
    if element.tag == "tag":
        for tag in element.iter('tag'):
            k = tag.get('k')
            
            if lower.search(k):
                keys['lower'] = keys['lower'] + 1
            elif lower_colon.search(k):
                keys['lower_colon'] = keys['lower_colon'] + 1
            elif problemchars.search(k):
                keys['problemchars'] = keys['problemchars'] + 1
            else:
                keys['other'] = keys['other'] + 1
        pass
        
    return keys

keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}


for element in get_elements(OSM_FILE):
    keys = key_type(element, keys)

pprint.pprint(keys)


# We are ready to see all values for <i>addr:street</i> and <i>addr:postcode</i> tags.

# In[15]:

osm_file = open(OSM_FILE, "r", encoding="utf-8")

tag_key_values = defaultdict(set)
expected = ['addr:street', 'addr:city']

for event, elem in ET.iterparse(osm_file, events=("start",)):

    if elem.tag == "node" or elem.tag == "way":
        for tag in elem.iter("tag"):
            if tag.attrib['k'] in expected:
                tag_key_values[tag.attrib['k']].add(tag.attrib['v'])

osm_file.close()
pprint.pprint(tag_key_values)


# In[ ]:



