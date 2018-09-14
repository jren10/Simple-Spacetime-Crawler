import json
import operator
from collections import Counter

def search():
    count_docs = 0
    count_tokens = 0
    results = []
    doc_list = []
    ranker = {}
    index = {}

    with open("dict.json", "rb") as file_in:
        index = json.load(file_in)
    # print index
    with open("bookkeeping.json") as json_file:
        json_dict = json.load(json_file)

    query = str(raw_input("Enter search term(s): "))
    query = query.lower()
    query_tokens = query.split()

    for token in query_tokens:
        for value in index[token]:
            if isinstance(value, float):
                pass
            else:
                temp_doc_id = value[0]
                temp_tf_idf = value[2]
                if temp_doc_id in ranker:
                    ranker[temp_doc_id] += temp_tf_idf
                else:
                    ranker[temp_doc_id] = temp_tf_idf

    sorted_ranker = sorted(ranker.items(), key=operator.itemgetter(1), reverse=True)[:10]

    # print (sorted_ranker)

    for key in sorted_ranker:
        print json_dict[key[0]]

    """
        for value in index[query]:
        if isinstance(value, float):
            pass
        else:
            doc_list.append(value[0])
            if value[0] in ranker:
                ranker[value[0]].append(value[2])
            else:
                ranker[value[0]] = value[2]
    """

    # for key in doc_list:
    # print doc_list[key]
    # doc_list = set(doc_list)
    index = Counter(index)
    """for i in index.keys():
        #print i
        count_tokens += 1

    print count_tokens"""


# for elem in doc_list:
#    results.append(json_dict[elem])
# docs = set(docs)
# print "docs is " + len(docs)
# print "test with duplicate values is " + len(test)
# print "test with lists is" + len(test)
# print len(index.keys())
# print "Search Results:\n"
# for i in results:
#   print i
#   print "\n"
# print results


def main():
    search()


if __name__ == '__main__':
    main()