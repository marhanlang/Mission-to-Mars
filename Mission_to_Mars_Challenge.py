#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import urllib


# In[2]:


#set up executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[14]:


df.to_html()


# ### Scrape High-Resolution Mars’ Hemisphere Images and Titles

# In[15]:


# 1. Use browser to visit the URL 
urla = 'https://marshemispheres.com/'

browser.visit(urla)


# In[16]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in range(1):
    #parse html 
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    hemispheres = {}

    def get_urls():
        imgs = img_soup.find_all('img', class_='thumb')
        urls = []
        for img in imgs:
            urlx = img.parent['href']
            urls.append(urlx)
        return urls 
        
    def get_titles():
        div_des = img_soup.find_all('div', class_='description')
        titles = []
        for div in div_des:
            title = div.find('h3').get_text()
            titles.append(title)
        return titles 
    
    #need to combine the base url (urla) with the urls list to create four separate urls to navigate to
    urlx = get_urls()
    urlz = []
    urlone= urla+(urlx[0])
    urltwo= urla+(urlx[1])
    urlthree= urla+(urlx[2])
    urlfour= urla+(urlx[3])
    urlz.append(urlone)
    urlz.append(urltwo)
    urlz.append(urlthree)
    urlz.append(urlfour)
    #print(urlz)
    
    title = get_titles()
    url_links = []
    #print(title)
    
    for j in urlz:
        browser.visit(j)
        html = browser.html
        mars_soup = soup(html, 'html.parser')
       
        
        downloads =mars_soup.find_all('div', class_= 'downloads')
        for dl in downloads:
            link = dl.find('a')
            href = link.get('href')
        
        img_urla = 'https://marshemispheres.com/'+ href
        url_links.append(img_urla)
        
    
    Cerberus = {'title': title[0],
                'img_url' : url_links[0]}
    Schip = {'title': title[1],
                'img_url' : url_links[1]}
    Syrtis = {'title': title[2],
                'img_url' : url_links[2]}
    Valles = {'title': title[3],
                'img_url' : url_links[3]}
    
    hemisphere_image_urls.append(Cerberus)
    hemisphere_image_urls.append(Schip)
    hemisphere_image_urls.append(Syrtis)
    hemisphere_image_urls.append(Valles)
    


# In[17]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[18]:


# 5. Quit browser
browser.quit()


# In[ ]:





# In[ ]:




