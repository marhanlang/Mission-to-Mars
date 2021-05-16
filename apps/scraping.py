# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_img" : hemisphere(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemisphere(browser):
    # 1. Use browser to visit the URL 
    urla = 'https://marshemispheres.com/'

    browser.visit(urla)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(1):
        #parse html 
        html = browser.html
        img_soup = soup(html, 'html.parser')
        

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
        
        #combine the base url (urla) with the urls list to create four separate urls to navigate to
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
        
        title = get_titles()
        url_links = []
        
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
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())