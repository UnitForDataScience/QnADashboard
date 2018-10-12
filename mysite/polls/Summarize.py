import os
from nltk.corpus import stopwords
from string import punctuation
from collections import defaultdict
from nltk import sent_tokenize, word_tokenize
from heapq import nlargest

path = os.path.join(os.path.dirname(__file__), '../../', 'Palo')
stopwords = set(
    stopwords.words('english') + list(punctuation) + ['TITLE', 'NRC', 'enclosure', 'nuclear', 'arkansas', 'inspection',
                                                      'report', 'docu', 'entergy', 'nrc', 'DOCUMENT', 'CONTAINS',
                                                      'SAFEGUARDS',
                                                      'INFORMATION'] + list(
        "month day year facility name pvngs unit 2 docket number 05000529 02 18 2009 2009 - 001 - 00 04 20 2009 facility name pvngs unit 3 docket number 05000530 9. operating mode 1 1 1 11. this report is submitted pursuant to the requirements of 10 cfr\u00a7 check all that apply \u2022 20.2201b \u2022 20.2203a3i \u2022 50.73a2ic 0 50.73a2vii \u2022 20.2201d \u2022 20.2203a3ii \u2022 50.73a2iia \u2022 50.73a2viiia \u2022 20.2203a1 \u2022 20.2203a4 k.. 50.73a2iib \u2022 50.73a2viiib \u2022 20.2203a2i \u2022 50.36c1ia \u2022 50.73a2iii \u2022 50.73a2ixa 10. power level 100 100 100 \u2022 20.2203a2ii \u2022 50.36c1iia \u2022 50.73a2iva \u2022 50.73a2x \u2022 20.2203a2iii \u2022 50.36c2 \u2022 50.73a2va \u2022 73.71a4 \u2022 20.2203a2iv \u2022 50.46a3ii 0 50.73a2vb \u2022 73.71a5 \u2022 20.2203a2v \u2022 50.73a2ia 50.73a2vc \u2022 other \u2022 20.2203a2vi 0 50.73a2ib 0 50.73a2vd specify in abstract below or in nrc form 366a 12. licensee contact for this ler facility name ray buzard section leader regulatory affairs telephone number include area code 623-393-5317. sincerely dcmrebdcegat enclosure cc e. e. collins jr. nrc region iv regional administrator j. r. hall nrc nrr project manager r. i. treadway nrc senior resident inspector for pvngs a member of the stars strategic teaming and resource sharing alliance callaway \u2022 comanche peak \u2022 diablo canyon \u2022 palo verde \u2022 san onofre \u2022 south texas \u2022 wolf creek nrc form 366 u.s. nuclear regulatory commission 9-2007 licensee event report ler see reverse for required number of digitscharacters for each block approved by omb no.".split()) + "nrc pdr 1 1 1 1 1 1 1 1 1 1 1 1 nudocs full txt d 0 category 1 regulatory information distribution system rids accession nbr9711280042 doc.date 971112 notarized no docket reactor coolant system charging andreactor coolant pump seal injection flows were restored within five minutes .due to the lop the fuel building essential-ventilation system the control roomessential filtration system and the containment purge system all actuated a sexpected .".split())


def summarize_texts(text, count=10, min_cut=0.6, max_cut=0.8, keywords=[]):
    print('This is problem')
    print(keywords)
    d = defaultdict(lambda: 1)
    exclude = set(punctuation)
    exclude.remove('.')
    exclude.remove('-')
    exclude.remove(('\''))
    text = ''.join(ch for ch in text if ch not in exclude)
    text = text.replace('\t', ' ')
    text = text.lower()
    sentences = sent_tokenize(text)
    word_sent = [word_tokenize(sentence) for sentence in sentences]
    freq = defaultdict(lambda: 0.)
    m = 0
    for s in word_sent:
        for w in s:
            if w not in stopwords and not w.isupper():
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
    print(keywords, found)
    print('This is problem')
    return ans if not found else []


def get_summary(keywords=[]):
    ans = []
    for file in os.listdir(path):
        content = open(path + '/' + file, encoding="utf8", errors='ignore', mode='r').read().replace('\n', '').replace(
            '\t',
            '')
        while '  ' in content:
            content = content.replace('  ', ' ')
        content = content.lower()
        temp = summarize_texts(content, keywords=keywords)
        if temp:
            ans.append(temp)
    return temp
