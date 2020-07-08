# SemanticSearch2020

Implementation of a search tool that searhces based off of semantics insteaad of keywords.

Uses universal sentence encoder from:
https://tfhub.dev/google/universal-sentence-encoder/4
to encode queries and entries. For this project, entries are scraped from the Mist company's documentation websites.
https://www.mist.com/documentation

The results are loaded into an Elasticseach index, which which can be queried using a simple flask web app that acts like a testing harness.

Key Files:
my_first_scraper/spiders/paragraphs.py - the spider that crawls mist.com for all entries that will eventually be searched over.

my_first_scraper/items.jl - this contains the raw information scraped from https://www.mist.com/documentation

SmartSearch/items_filtered.jl - This file is items.jl after it has been run through item_processor.sh. This removes all special unicode characters, all line feeds, and all non-documentation related pages.

SmartSearch/items_sem_title_w_snippet.jl - This file contains all entries in items_filtered.jl aafter it has been run through USE_embed.py. This attaches the snippet_vector field to each entry, which uses the universal semantic encoder to create a semantic vector for each entry.

SmartSearch/items_es_ready.jl - This file is items_sem_title_w_snippet.jl each it is interleaved with {"index":{}} between entries. This file is ready to be input into an Elasticsearch instance with an appropriate curl command that can be found in load_into_es.sh

