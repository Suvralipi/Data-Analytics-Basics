#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/python
import requests
import sys
import shutil
import re
import threading
from bs4 import BeautifulSoup as soup

THREAD_COUNTER = 0
THREAD_MAX     = 5

def requesthandle( link, name ):
    global THREAD_COUNTER
    THREAD_COUNTER += 1
    try:
        r = requests.get( link, stream=True )
        if r.status_code == 200:
            r.raw.decode_content = True
            f = open( name, "wb" )
            shutil.copyfileobj(r.raw, f)
            f.close()
            print("[*] Downloaded Image: %s", name)
    except(Exception, error):
        print("[~] Error Occured with %s : %s", name, error)
    THREAD_COUNTER -= 1


# In[2]:


def get_source( link ):
    r = requests.get( link )
    if r.status_code == 200:
        return soup( r.text )
    else:
        sys.exit( "[~] Invalid Response Received." )


# In[41]:


def filter( html ):
    imgs = html.findAll( "div" )
    if imgs:
        return imgs
    else:
        sys.exit("[~] No images detected on the page.")


# In[50]:



from urllib.request import urlopen as uReq
from urllib.request import urlopen

response = requests.get('https://www.debenhams.com/women/tops/shirts-1#filter/product.noofAlternateImages')
html = soup(response.text, 'html.parser')
allTags = filter(html)
#tags = html.find_all('img')
print(type(allTags))
#print(allTags)


result = html.find('div', {'class': 'dbh-image pw-responsive-image pw-loaded'})
#result = result.find('img').text


f = open("test.txt", "w")
f.write(str(result))
f.close()


# In[24]:


get_ipython().system('pip install urllib2')


# In[19]:


html = get_source( "https://shop.mango.com/gb/men/shirts_c10863844" )

divs = html.findAll("div")
f = open("test.txt", "w")
f.write(str(divs))
f.close()


# In[15]:


html = get_source( "https://shop.mango.com/gb/men/shirts_c10863844" )
    
tags = filter( html )
i=1
for tag in tags:
    src =tag.get( "src" )
    #print(src)
    for s1 in str(src).split(','):
        #s2=s1.strip('None')
        #s2=re.sub(r"\s+", "", s1, flags=re.UNICODE)
        s3=s1.strip('None')
        if s3:
            #print(s3)
            #print(i)
            r = requests.get(s3,  stream=True )
            s='\DebenhamsDataset\men_shirt_'+str(i)+'.jpg'
            open(s, 'wb').write(r.content)
            i=i+1
            


# ## Remove Duplicate images from the folder

# In[40]:



import hashlib
from scipy.misc import imread, imresize, imshow
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
get_ipython().run_line_magic('matplotlib', 'inline')
import time
import numpy as np

import os


def file_hash(filepath):
    with open(filepath, 'rb') as f:
        return md5(f.read()).hexdigest()


# In[41]:


os.getcwd()


# In[51]:



os.chdir(r'C:\Users\Suvralipi\Marks&Spenser\women\tshirts')
os.getcwd()


# In[57]:



file_list = os.listdir()
print(len(file_list))


# In[54]:


import hashlib, os
from PIL import Image
duplicates = []
hash_keys = dict()
for index, filename in  enumerate(os.listdir('.')):  #listdir('.') = current directory
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            #filehash = hashlib.md5(f.read()).hexdigest()
            filehash = dhash(Image.open(f))
        if filehash not in hash_keys: 
            hash_keys[filehash] = index
        else:
            duplicates.append((index,hash_keys[filehash]))


# In[ ]:


path = os.getcwd()


# In[46]:


dirs = os.listdir( path )

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((200,260), Image.ANTIALIAS)
            imResize.save(f, 'JPEG', quality=90)

resize()


# In[55]:


len(duplicates)


# In[56]:



for index in duplicates:
    os.remove(file_list[index[0]])


# In[29]:


def dhash(image, hash_size = 8):
    # Grayscale and shrink the image in one step.
    image = image.convert('L').resize(
            (hash_size + 1, hash_size),
            Image.ANTIALIAS,
        )
    pixels = list(image.getdata())
# Compare adjacent pixels.
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)
# Convert the binary array to a hexadecimal string.
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0
    return ''.join(hex_string)


# In[ ]:




