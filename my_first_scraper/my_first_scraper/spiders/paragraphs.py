

from bs4 import BeautifulSoup
import scrapy
import time


def isEmptyString(x):
    if len(x) == 0:
        return False
    else:
        return True

class LinkCheckerSpider(scrapy.Spider):
    name = 'paragraph_cralwer'
    allowed_domains = ['www.mist.com']
    start_urls = ['https://www.mist.com/documentation']
#    start_urls = ["https://www.mist.com/documentation/category/getting-started/"]

    def parse(self, response):

        soup = BeautifulSoup(response.text, 'lxml')

        # Scrapes general info from the page
        type_ = soup.find('span', itemprop='name')

        type_name = "Null"
        if type_ is not None:
            type_name = type_.find(text=True)

        title = soup.find('h1', 'content-title')
        title_name = "Null"
        if title is not None:
            title_name = title.find(text=True)

        articles = soup.find_all('article')

        paragraph = 1
        for article in articles:

            subtitle_html = article.find('h2', class_='entry-title')
            subtitle_name = "Null"
            if title is not None:
                subtitle_name = subtitle_html.find(text=True)

            entry = article.find('div', class_='entry-content')
            snippet = "Null"
            if entry is not None:
                snippet = entry.find(text=True)

            # CHANGE THE ORDER OF THESE, url SHOULD COME AFTER image
            yield {
                'url': response.request.url,
                'paragraph_number': paragraph,
                'snippet': str(snippet).strip(),
                'subtitle': str(subtitle_name),
                'title': str(title_name),
                'image': "null",
                'image_url': "null",
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

