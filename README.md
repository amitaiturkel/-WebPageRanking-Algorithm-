# -WebPageRanking-Algorithm-
PageRank-Moogle" is a repository that houses a simple web page ranking system implemented using the PageRank algorithm. The system aims to provide rankings for searched words based on their frequency in crawled web pages. 
# Moogle - Web Page Ranking System

## Overview

Moogle is a simple web page ranking system that provides rankings for searched words based on their frequency in crawled web pages. The system uses the PageRank algorithm to determine the relative importance of web pages.

## Features

- Crawl web pages and create a dictionary of links between them.
- Calculate page rankings using the PageRank algorithm.
- Create a dictionary with word frequencies for each site.
- Perform searches and return the top-ranked sites for a given query.

## Usage

### Crawling Web Pages

To crawl web pages and create a dictionary of links between them, use the `crawl` function:

```python
crawl(base_url, index_file, out_file)

base_url: The base URL to start crawling from.
index_file: A text file containing a list of site URLs to crawl.
out_file: The output pickle file to store the dictionary of links.
Calculating Page Rankings

To calculate page rankings using the PageRank algorithm, use the page_rank function:

page_rank(iterations, dict_name, out_file)

iterations: The number of iterations to perform in the PageRank algorithm.
dict_name: The input pickle file containing the dictionary of links between web pages.
out_file: The output pickle file to store the page rankings.

To create a dictionary with word frequencies for each site, use the words_dict function:

words_dict(base_url, index_file, out_file)

base_url: The base URL to start crawling from.
index_file: A text file containing a list of site URLs to crawl.
out_file: The output pickle file to store the dictionary of word frequencies.

To perform a search and return the top-ranked sites for a given query, use the search function:

search(list_of_query, ranking_dict_file, words_dict_file, max_result)

list_of_query: A space-separated string of query words.
ranking_dict_file: The pickle file containing the page rankings.
words_dict_file: The pickle file containing the dictionary of word frequencies.
max_result: The maximum number of top-ranked sites to return.

Requirements
Python 3.x
requests library
bs4 (Beautiful Soup) library

