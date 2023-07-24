#################################################################
# FILE : moogle.py
# WRITER : amitai turkel
# DESCRIPTION: A simple program that give a ranking for searched words

#################################################################
import sys
import urllib.parse
import requests
import bs4
import pickle

# Function to read a text file and create a dictionary with a nested empty dictionary for each key
def txt_to_dictionary_in_dictionary(txt):
    # Read the text file
    with open(txt, 'r') as myfile:
        data_dict = {}
        for line in myfile:
            k = line.strip()
            data_dict[k.strip()] = {}  # Create an empty dictionary as the value for each key
    return data_dict


# Function to read a text file and convert each line into an item in a list
def txt_to_list(txt):
    with open(txt, "r") as file:
        txt_list = file.read()
        data_into_list = txt_list.strip().split("\n")
    return data_into_list


# Function to create a rank dictionary with keys from the given dictionary and set all values to 0
def make_rank_dict_from_dict_zero(dictionary):
    rank_dict = {}
    for key in dictionary:
        rank_dict[key] = 0
    return rank_dict


# Function to create a rank dictionary with keys from the given dictionary and set all values to 1
def make_rank_dict_from_dict_one(dictionary):
    rank_dict = {}
    for key in dictionary:
        rank_dict[key] = 1
    return rank_dict


# Function to flatten a nested list and remove duplicates
def list_in_list_in_list_to_one(biggest_list):
    final_list = []
    for first in biggest_list:
        for second in first:
            for word in second:
                if word not in final_list:
                    final_list.append(word)
    return final_list


# Function to calculate the relative points of a given key in the dictionary
def dic_points_rank_given(dictionary, key_give_rank, key_get_rank):
    if key_give_rank not in dictionary.keys() or key_get_rank not in dictionary.keys():
        return False
    sum_of_pointers = sum(dictionary[key_give_rank].values())
    points_given = (dictionary[key_give_rank][key_get_rank]) / sum_of_pointers
    return points_given


# Function to crawl web pages, extract links, and create a dictionary of links
def crawl(base_url, txt, out_file):
    moogle_dictionary = txt_to_dictionary_in_dictionary(txt)
    for first_key in moogle_dictionary:
        full_url = urllib.parse.urljoin(base_url, first_key)
        response = requests.get(full_url)
        html = response.text
        soup = bs4.BeautifulSoup(html, "html.parser")
        for p in soup.find_all("p"):
            for link in p.find_all("a"):
                target = link.get("href")
                if target in moogle_dictionary.keys():
                    if target not in moogle_dictionary[first_key].keys():
                        moogle_dictionary[first_key][target] = 1
                    else:
                        moogle_dictionary[first_key][target] += 1
    with open(out_file, "wb") as f:
        pickle.dump(moogle_dictionary, f)


# Function to calculate the ranking of pages using the PageRank algorithm
def page_rank(iterations: int, dict_name, out_file):
    with open(dict_name, "rb") as f:
        dict_file = pickle.load(f)
    rank_dict = make_rank_dict_from_dict_one(dict_file)
    if int(iterations) == 0:
        with open(out_file, "wb") as f:
            pickle.dump(rank_dict, f)
    for iteration in range(iterations):
        new_rank_dict = make_rank_dict_from_dict_zero(dict_file)
        for give_key in rank_dict:
            for get_key in new_rank_dict:
                if get_key in dict_file[give_key]:
                    new_rank_dict[get_key] += (rank_dict[give_key]) * (dic_points_rank_given(dict_file, give_key, get_key))
        rank_dict = new_rank_dict
    with open(out_file, "wb") as f:
        pickle.dump(rank_dict, f)


# Function to create a dictionary with word frequencies for each site
def words_dict(base_url, index_file, out_file):
    # Read the list of site URLs from the index file
    list_of_site = txt_to_list(index_file)

    # Initialize an empty list to store the words for each site
    list_of_word_in_site = []

    # Crawl each site, extract words from <p> tags, and store them in the list
    for site in list_of_site:
        full_url = urllib.parse.urljoin(base_url, site)
        response = requests.get(full_url)
        html = response.text
        soup = bs4.BeautifulSoup(html, "html.parser")
        words_in_site = []
        for p in soup.find_all("p"):
            content = (p.text.strip()).split()
            if len(content) > 0:
                words_in_site.append(content)
        list_of_word_in_site.append(words_in_site)

    # Flatten the nested list to get a list of all unique words across all sites
    list_of_word_total = list_in_list_in_list_to_one(list_of_word_in_site)

    # Initialize an empty dictionary to store word frequencies for each site
    dict_of_words = {}

    # Iterate through each site again to count word frequencies
    for site in list_of_site:
        full_url = urllib.parse.urljoin(base_url, site)
        response = requests.get(full_url)
        html = response.text
        soup = bs4.BeautifulSoup(html, "html.parser")
        for p in soup.find_all("p"):
            content = (p.text.strip()).split()
            for word in list_of_word_total:
                if word not in dict_of_words.keys():
                    dict_of_words[word] = {}
                for count_word in content:
                    if count_word == word:
                        if site not in dict_of_words[word].keys() and site != '"':
                            # If the word is encountered for the first time on the site, initialize its count to 1
                            dict_of_words[word][site] = 1
                        else:
                            # If the word has been encountered before on the site, increment its count
                            dict_of_words[word][site] += 1

    # Write the dictionary containing word frequencies to a pickle file
    with open(out_file, "wb") as f:
        pickle.dump(dict_of_words, f)

    # Return the dictionary containing word frequencies
    return dict_of_words


# Function to extract the first item from a list of tuples
def take_tuples(list_of_tuples):
    list_of_first = []
    for first in list_of_tuples:
        list_of_first.append(first[0])
    return list_of_first


# Function to collect the sites for each word in the list of queries
def collect_list_sites(list_of_query, words_dict):
    dict_of_sites = {}
    for search_word in list_of_query:
        sites = words_dict[search_word].keys()
        dict_of_sites[search_word] = sites
    return dict_of_sites


# Function to find the intersection of sites for all the words in the query list
def collect_intersect_sites(list_of_query, dict_of_sites):
    unique_sites = None
    for search_word in list_of_query:
        if not unique_sites:
            unique_sites = set(dict_of_sites[search_word])
        else:
            unique_sites = unique_sites.intersection(dict_of_sites[search_word])
    return unique_sites


# Function to search for the given query words in the ranking dictionary and return the top-ranked sites
def search(list_of_query, ranking_dict_file, words_dict_file, max_result):
    with open(ranking_dict_file, "rb") as f:
        ranking_dict = pickle.load(f)
    with open(words_dict_file, "rb") as f:
        words_dict = pickle.load(f)
    new_list_of_query = [word for word in list_of_query.split() if word in words_dict]
    site_dict = collect_list_sites(new_list_of_query, words_dict)
    site_dict_intersection = collect_intersect_sites(new_list_of_query, site_dict)
    first_ranked_sites_list = []
    for first_ranked_site in site_dict_intersection:
        rank = ranking_dict[first_ranked_site]
        first_ranked_sites_list.append((first_ranked_site, rank))
    sorted_first_ranked_sites = sorted(first_ranked_sites_list, key=lambda x: x[1], reverse=True)
    sorted_first_ranked_sites = sorted_first_ranked_sites[:max_result]
    sorted_sites = take_tuples(sorted_first_ranked_sites)
    return sorted_sites


def main():
    args = sys.argv[1:]
    if len(args) == 4 and args[0] == 'crawl':
        crawl(args[1], args[2], args[3])
    elif len(args) == 4 and args[0] == 'page_rank':
        page_rank(int(args[1]), args[2], args[3])
    elif len(args) == 4 and args[0] == 'words_dict':
        words_dict(args[1], args[2], args[3])
    elif len(args) == 5 and args[0] == 'search':
        result_sites = search(args[1], args[2], args[3], int(args[4]))
        print(result_sites)


if __name__ == "__main__":
    main()
