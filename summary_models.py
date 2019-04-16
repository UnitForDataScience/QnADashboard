from collections import defaultdict
from string import punctuation
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from heapq import nlargest

stop_words = set(
    stopwords.words('english') + list(punctuation))



def summarize_tf(text, count=10, min_cut=0.6, max_cut=0.8, keywords=[]):
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
    word_sent = [word_tokenize(sentence) for sentence in sentences]
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
        if freq[w] > max_cut or freq[w] < min_cut:
            not_this.add(w)
    ranking = defaultdict(lambda: 0.)
    for i, sent in enumerate(word_sent):
        for w in sent:
            if w in freq and w not in not_this:
                ranking[i] += freq[w] * d[w.lower()]
    sent_ids = nlargest(count, ranking, key=ranking.get)
    ans, found = [], set(keywords.copy())
    for i in sent_ids:
        ans.append(sentences[i])
        to_remove = set()
        for x in found:
            if x in sentences[i]:
                to_remove.add(x)
        for x in to_remove:
            found.remove(x)
    return ans if not found else []

