#from __future__ import division

import json
from HTMLParser import HTMLParser
import requests
from bs4 import BeautifulSoup
from lxml import html
import urllib2
import nltk, re, pprint
from nltk import word_tokenize
from collections import Counter
import math
import pickle
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def parse_json():
    json_dict = {}
    with open("bookkeeping.json") as json_file:
        json_dict = json.load(json_file)

   #path = "D:/Jason/PyCharm/CS 121 Assignment 3/WEBPAGES_RAW/1/2"
   # this is to individually test specific files instead of working with everything     #for efficiency reasons
   #with open(path) as html_file:
       #raw = html_file.read().decode('utf8')
       #soup = BeautifulSoup(raw, 'html.parser')
       #print soup.body.renderContents()
    #inverted_index = {}

    freq = {}
    size_of_file = len(json_dict.keys())

    temp_dict = defaultdict(list)
    inverted_index = defaultdict(list)
    counter = 0
    stop_words = set(stopwords.words('english'))
    df_counter = {}
    item_list_list = []
    item_list = []

    for key in json_dict.keys():

        path = "/Users/Kayvaan/PycharmProjects/CS121_Project3/WEBPAGES_RAW/" + key
        with open(path) as html_file:
            occur = 0
            #raw = html_file.read().decode('utf8')
            raw = html_file.read().decode('utf-8-sig', 'ignore')
            soup = BeautifulSoup(raw, 'html5lib')
            if soup.body:
                body_text = soup.body
                [s.extract() for s in body_text('script')]
                #print body_text.get_text().lower()
                #body = soup.body.renderContents()
                #body = str(soup)
                #print soup.body

                tokens = nltk.tokenize.word_tokenize(body_text.get_text().lower()) #body)
                filtered_tokens = [word for word in tokens if word not in stop_words]
                freq = Counter(filtered_tokens)
                filtered_tokens = set(filtered_tokens)
                #print freq

                for token in filtered_tokens:
                    item_list.append(key)   #first element is doc ID
                    item_list.append(freq[token])   # second element is tf
                    #item_list_list.append(item_list)
                    #inverted_index[token].append(key)
                    inverted_index[token].append(item_list)  #make list of lists for every docID and the tf
                    item_list = []

                    if token not in df_counter:
                        df_counter[token] = 1
                    else:
                        df_counter[token] += 1

        print key
    for key in inverted_index.keys():
        idf = math.log10(size_of_file / df_counter[key])
        inverted_index[key].append(idf)
        for value in inverted_index[key]:
            if isinstance(value, float):
                pass
            else:
                tf_idf = value[1] * idf
                value.append(tf_idf)

    """for token in tokens:
                    index = soup.body.find(token)
                    indices.append(index)
                    occur = occur + 1
                ##ge

                for token in tokens:
                    temp_list.append(freq[token])
                    doc_index[key].append(temp_list) #tf
                    if token not in inverted_index.keys():
                        inverted_index[token] = doc_index

                for token in tokens:
                    tf = freq[token]
                    for key, value in inverted_index.items():
                        df = len([item for item in value if item])
                    idf = math.log10(size_of_file / df)
                    temp_list.append(tf * idf)
                    doc_index[key] = temp_list
                    if token not in inverted_index.keys():
                        inverted_index[token] = doc_index
                    inverted_index[token] = doc_index
                    inverted_index[token] = idf
                    print "Working..."""

    """temp_list.append(key) #doc id
                    temp_list.append(freq[token]) #tf
                    temp_list.append(indices) #index positions
                    #tf = freq[token]
                    #idf = math.log10(size_of_file / )

                    inverted_index[token].append(temp_list)"""
    with open("dict.json", "wb") as file_out:   #pickle_out
        json.dump(inverted_index, file_out)   #or pickle.dump
    #pickle_out = open("/Users/Kayvaan/PycharmProjects/CS121_Project3/dict.pickle")
    #pickle.dump(inverted_index, pickle_out)
    #pickle_out.close()
    print "\n\n\ndone\n\n\n"

def main():
    parse_json()


if __name__ == '__main__':
   main()

