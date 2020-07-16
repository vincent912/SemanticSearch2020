SemanticSearch2020
================
July 15, 2020
-------------

The functionality of the search tool on [Mist's documenation](https://www.mist.com/documentation) page currently uses some form of keyword searches that fails to return relevant search results. For example, when I enter into the search bar "AP Upgrades" and look at the [results](https://www.mist.com/?s=AP+upgrades), the search tool does not return the page titled [AP Upgrades](https://www.mist.com/documentation/ap-upgrades/).  


This project creates a better search tool that finds the semantics of a query and finds the results that have the closest meaning to the search. More details on the motivation for the project can be found in the project_motivation.pdf file.

Overview
-----------
All useful information from [Mist's documenation](https://www.mist.com/documentation) is first scraped using scrapy. The resulting entries with snippets are then cleaned, and then their semantic vectors are calculated using a [universal sentence encoder](https://tfhub.dev/google/universal-sentence-encoder/4). The data is loaded into an Elasticsearch index, which is capable of scoring and querying based on cosine similarity. A simple flask web app serves as a testing harness, which takes a query string, finds its semantic vector, then queries the Elasticsearch index. The index returns results whose semantic vectors have the highest cosine similarity to the query's semantic vector, which are then displayed to the user by the Flask app. 

Process Details
----------
First, I used scrapy, an open source python web scraper, to scrape [Mist's documentation](https://www.mist.com/documentation) pages. The scraper crawls over all pages that have a mist.com url, and then yields every snippet (essentially every useful piece of text generally found in an article or block tag in the html) into a json lines file titled `items.jl`. For example, the [Getting Started](https://www.mist.com/documentation/category/getting-started/) page will yield an entry for each of the roughly 10 text paragraphs.  

The `items.jl` file contains entries from the website that are not from the documentation page, entries with empty snippets, or snippets that contain special unicode characters and miscellaneous new lines from the html. Thus I ran the json lines file through a shell script `item_processor.sh` that uses the stream editor tool and regex to filter out entries that contain empty snippets and to remove all special characters from entries that are kept. The resulting file is named `items_filtered.jl`.  

To find the semantics of each entry/snippet, this [universal sentence encoder](https://tfhub.dev/google/universal-sentence-encoder/4) is used. This package has the ability to turn strings into a 512 dimensional vector that represents the semantics of the input string. Using this package, every entry has its semantic vector calculated and then appended to its json lines entry. Once encoded using the universal sentence encoder, how close the semantics of two strings are can be calculated by finding the cosine similarity or the inner product of the vectors. The higher the resulting value, the closer the string's semantics are. The `items_es_ready.jl` file contains all entries in `items_filtered.jl` with semantic vectors attached, and properly formatted for loading into the elasticsearch index.

Before the data can be loaded into Elasticsearch, an index_template `elasticsearch_template.txt` was created that outlined the "shape" of the data that was going to be loaded. This included information about each entry like what the name of each piece or information is, what data type each piece of info is, how many dimensions the semantic vector is, etc. Afterwards, the data in a json lines file, consisting of entries representing paragraphs from Mist's documentation including its semantic vector, was formatted properly and then loaded into an elasticsearch index using a curl command. Now, queries can be made by issuing a request to the elasticsearch data base.  

To make testing and performance evaluation easier, I created a Flask app to act as a test harness for this search engine. The app only consists of one page, which has a search bar and an enter button. Once text is entered into the search bar, the flask app takes it and calculates its semantic vector using the [universal sentence encoder](https://tfhub.dev/google/universal-sentence-encoder/4). It then queries the elasticsearch index, which returns results such that the first result's semantic vector has the highest cosine similarity to the query's semantic vector, and the last result has the lowest cosine similarity. The top five unique urls that contain the most similar snippet's are then displayed in the web app.

Performance
---------------
In order to give a concrete measure of performance, I took questions found from [Mist's Documentation Wifi FAQ](https://www.mist.com/documentation/category/wifi-faq/) page and used those as test queries. If the relevant page from the FAQ is found in the top 5 results, the test will be considered a success. Otherwise, we will consider the test a failure. The performance of SemanticSearch will then be compared to the results of the current search tool. I took the first 20 questions on that FAQ page to test each search tool. The results:  
> SemanticSearch: 20 successes out of 20
> Current search tool: 3 successes out of 20 

Based on this test alone, we can see that the SemanticSearch tool is performing better than the current search tool. Despite the fact that a search tool's power can't really be measured just by one test like this, I can see from this test that all of the top five results that SemanticSearch returns are all relevant in some way to the query in question. This is in contrast to the current search tool that gets caught up on popular keywords in the query like Mist and AP, and returns results based off of those hot keywords instead of taking  the whole query into account.  



Key Files:
-----------
Code Files:
- `load_into_es.sh`: shell script that creates a new elasticsearch index from a properly formatted json lines file. Takes two arguments, the first is the name of the index you want to create, and the second is the name of the file containing the json entries
- `SmartSearch/item_processor.sh`: shell script that removes special characters, new lines, empty entries, and non-documentation entries from the input file. Takes two entries, the first is the input filename and the second is the output filename.
- `my_first_scraper/spiders/paragraphs.py`: the spider that crawls [mist.com](http://mist.com/) for all entries that will eventually be searched over. Outputs `items.jl`.
- `SmartSearch/USE_embed.py`: attaches semantic vector using universal sentence encoder to each entry. Also weaves in `{"index":{}}` between each entry so that the file can be loaded into an elasticsearch index
- `elasticsearch_template.txt`: the index_template that defines the "shape" of the index that will be created by the `items_es_ready.jl` file. Is a PUT http request that can be executed by Kibana.

Data:
- `my_first_scraper/items.jl`:  contains the raw information scraped from https://www.mist.com/documentation
- `SmartSearch/items_filtered.jl`: the results after items.jl has been run through item_processor.sh. This removes all special unicode characters, all line feeds, and all non-documentation related pages as well as pages with empty snippets. 
- `SmartSearch/items_es_ready.jl` - the results after items_sem_title_w_snippet.jl each it is interleaved with {"index":{}} between entries. This file is ready to be input into an Elasticsearch instance with an appropriate curl command that can be found in load_into_es.sh

