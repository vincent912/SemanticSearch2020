

from bs4 import BeautifulSoup
import scrapy
import time
import os
import re

# sed '/.*www.mist.com\/documentation.*/!d' items.jl > items_filtered.jl

def findtitle(soup):

    title = soup.find('h1', 'content-title')
    title_name = "Null"
    if title is not None:
        title_name = title.find(text=True)
        return title_name

    title = soup.find('h1', class_="entry-title")
    if title is not None:
        title_name = title.find(text=True)
        return title_name


def findtype(soup):
    type_ = soup.find('span', itemprop='name')

    type_name = "Null"
    if type_ is not None:
        type_name = type_.find(text=True)
        return type_name




class LinkCheckerSpider(scrapy.Spider):
    name = 'paragraph_cralwer'
    allowed_domains = ['www.mist.com']
    # start_urls = ['https://www.mist.com/documentation/why-do-clients-disconnect-when-you-add-a-new-wlan']
    start_urls = ['https://www.mist.com/documentation/']
    # start_urls = ["https://www.mist.com/documentation/category/getting-started/"]
    # start_urls = ['https://www.mist.com/documentation/wifi6-802-11ax-overview/']
    # start_urls = ['https://www.mist.com/documentation/mist-ap-mounting/']

    def parse(self, response):

        soup = BeautifulSoup(response.text, 'lxml')

        # Scrapes general info from the page
        type_name = findtype(soup)
        title_name = findtitle(soup)

        # Processes all articles in the page
        articles = soup.find_all('article')
        paragraph = 1
        for article in articles:

            subtitle_html = article.find('h2', class_='entry-title')
            subtitle_name = "Null"
            if subtitle_html is not None:
                subtitle_name = subtitle_html.find(text=True)

            entry = article.find('div', class_='entry-content')
            snippet = "Null"
            if entry is not None:
                snippet = entry.find(text=True)

            # CHANGE THE ORDER OF THESE, url SHOULD COME AFTER image
            yield {
                'url': response.request.url,
                'paragraph_number': paragraph,
                'snippet': re.sub("\u00a9|\u00a0|\u2018|\u201d|\u2019|\u2013", "", str(snippet).strip()),
                'subtitle': str(subtitle_name),
                'title': str(title_name),
                'image': "null",
                'image_url': "null",
                'type': type_name,
                'creationDate': int(time.time()),
                'snippet_vector': ["to be implemented"]

            }
            paragraph = paragraph + 1

        # Processes content that is formatted in paragraphs
        processed_image = False
        blocks = soup.findAll('p', class_=None)
        for i in range(len(blocks)):
            if processed_image:
                processed_image = False
                continue

            snippet = "Null"
            if blocks[i] is not None:
                snippets = blocks[i].findAll(text=True)
                snippet = ""
                for snip in snippets:
                    snippet = snippet + snip

            image_url = "Null"
            image_name = "Null"
            if i < len(blocks) - 2 and blocks[i+1].find('img') is not None:
                image_url = blocks[i+1].find('img').get('src')
                image_name = os.path.basename(image_url)
                processed_image = True

            yield {
                'url': response.request.url,
                'paragraph_number': paragraph,
                'snippet': re.sub("\u00a9|\u00a0|\u2018|\u201d|u\2019|\u2013", "", str(snippet).strip()),
                'subtitle': "Null",
                'title': str(title_name),
                'image': image_name,
                'image_url': image_url,
                'type': type_name,
                'creationDate': int(time.time()),
                'snippet_vector': ["to be implemented"]

            }
            paragraph = paragraph + 1



        # Follows all links to the rest of the webpages reachable from this one
        links = []
        a_selectors = response.xpath("//a")

        for selector in a_selectors:
            links.append(selector.xpath("@href").extract_first())

        for link in links:
            print(link)
            if link is not None:
                request = response.follow(link, callback=self.parse)
                yield request




#        print(str(articles[0]))
#
#        article1 = BeautifulSoup(str(articles[0]), 'lxml')
#
#        title = article1.find('h2', class_='entry-title')
#        title_name = title.find_all(text=True)
#        print("\n\n\n")
#
#
#        print(title)
#
#        print("\n\n\n")
#
#        print(title_name)
#
#
#
#        print("\n\n\n")



        
#        paragraph_number = 1
#        for content in all_content:
#            content = content.strip()
#            soup = BeautifulSoup(response.text, 'lxml')
#
#            if content != "":
#                yield {
#                    'paragraph number':paragraph_number,
#                    'snippet': text_from_content[paragraph_number-1],
#                    'subtitle': "null"
#
#                }
#                paragraph_number = paragraph_number + 1







#    {
#        "paragraph_number" : 2,
#        "snippet" : "On the Client Events in the Insights page, you will see an AP Deauthentication being sent to the clients when the changes are made. You can refer the audit log for the same.",
#        "subtitle" : null,
#        "title" : "Why do clients disconnect when you add a new WLAN?",
#        "image" : "Screen-Shot-2020-03-26-at-2.55.00-PM.png",
#        "url" : "https://www.mist.com/documentation/why-do-clients-disconnect-when-you-add-a-new-wlan",
#        "image_url" : "https://raw.githubusercontent.com/Abe13/Marvin_chatbot/master/images/Screen-Shot-2020-03-26-at-2.55.00-PM.png",
#        "type" : "Wifi-FAQ",
#        "creationDate" : 1589473908412,
#        "snippet_vector" : [
#        ]
#    }

