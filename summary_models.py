from collections import defaultdict
from string import punctuation
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from heapq import nlargest, heappush, heappop
import pandas as pd
import numpy as np
import networkx as nx

from sklearn.metrics.pairwise import cosine_similarity

stop_words = set(
    stopwords.words('english') + list(punctuation))


def summarize_tf(text, count=10, min_cut=0.5, max_cut=0.8, keywords=[]):
    temp_keywords = set(keywords)
    d = defaultdict(lambda: 1)
    exclude = set(punctuation)
    exclude.remove('.')
    exclude.remove('-')
    exclude.remove('\'')
    text = text.replace('\n', '').replace('\t', ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')
    text = ''.join(ch for ch in text if ch not in exclude)
    sentences = sent_tokenize(text)
    word_sent = [word_tokenize(sentence.lower()) for sentence in sentences]
    freq = defaultdict(lambda: 0.)
    m = 0
    for s in word_sent:
        for w in s:
            if w not in stop_words and not w.isupper():
                freq[w] += 1
                m = max(m, freq[w])
    not_this = set()
    for w in freq:
        freq[w] /= m
        if freq[w] > max_cut or freq[w] < min_cut and w not in temp_keywords:
            not_this.add(w)
    ranking = defaultdict(lambda: 0.)
    for i, sent in enumerate(word_sent):
        for w in sent:
            if w in freq and w not in not_this:
                ranking[i] += (freq[w] if w not in temp_keywords else float('inf')) * d[w]

    sent_ids = sorted(nlargest(count, ranking, key=ranking.get))
    ans, found = [], set(keywords.copy())
    for i in sent_ids:
        ans.append(sentences[i])
    return ans


f = open('./vectors.txt', encoding='utf-8')
vectors = f.readlines()

word_embeddings = {}

for line in vectors:
    values = line.split()
    word_start = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word_start] = coefs


def remove_stopwords(sen):
    stop_words = stopwords.words('english')
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new


def summarize_page_rank(text, keywords=[], n=10):
    print('came here')
    sentences = sent_tokenize(text)
    # remove punctuations, numbers and special characters
    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
    # make alphabets lowercase
    clean_sentences = [s.lower() for s in clean_sentences]
    clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]

    sentence_vectors = []
    personalized_vectors = {}
    count = 0
    for i in clean_sentences:
        if len(i) != 0:
            list_a = i.split()
            personalized_vectors[count] = len(set(list_a) & set(keywords)) + 1
        else:
            personalized_vectors[count] = 1
        count += 1

    for i in clean_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((50,))) for w in i.split()]) / (len(i.split()) + 0.001)
        else:
            v = np.zeros((50,))
        sentence_vectors.append(v)
    sim_mat = cosine_similarity(sentence_vectors, sentence_vectors)
    for i in range(len(sim_mat)):
        sim_mat[i][i] = 0
    nx_graph = nx.from_numpy_array(sim_mat)

    result = []
    try:
        scores = nx.pagerank(nx_graph, max_iter=200, personalization=personalized_vectors)
        for i, x in enumerate(sentences):
            heappush(result, (scores[i], x, i))
            if len(result) > n:
                heappop(result)
        result = list(map(lambda x: x[1], sorted(result, key=lambda x: x[2])))
    except Exception as e:
        print(e)
        result.append("Exception occurred")
    return result
