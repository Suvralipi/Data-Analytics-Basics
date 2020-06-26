#!/usr/bin/env python
# coding: utf-8

# In[3]:


from selenium import webdriver


browser = webdriver.Chrome() #replace with .Firefox(), or with the browser of your choice
url = "https://www.debenhams.com/women/tops/shirts-1#filter"
browser.get(url) #navigate to the page


# In[6]:


innerHTML = browser.execute_script("return document.body.innerHTML")


# In[18]:


def filter( html ):
    imgs = html.findAll( "img" )
    if imgs:
        return imgs
    else:
        sys.exit("[~] No images detected on the page.")


# In[19]:


from bs4 import BeautifulSoup as soup
html = soup( innerHTML , "html" )


# In[20]:


allTags = filter(html)


# In[24]:


import os
os.getcwd()


# In[ ]:


import requests

i=1
for tag in allTags:
    src =tag.get( "srcset" )
    print(src)
    for s1 in str(src).split('https://'):
        #s2=s1.strip('None')
        #s2=re.sub(r"\s+", "", s1, flags=re.UNICODE)
        print("Outer Loop")
        print(s1)
        s3=s1.strip('None')
        if s3:
            print('inside If')
            print(s3)
            print(i)
            r = requests.get('https://'+ s3,  stream=True )
            s='DebenhamsDataset\women_shirt_'+str(i)+'.jpg'
            open(s, 'wb').write(r.content)
            i=i+1


# In[ ]:




