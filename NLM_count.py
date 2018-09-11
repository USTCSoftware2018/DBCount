# coding=utf-8
import urllib
from bs4 import BeautifulSoup


def nlm(query):
    url = 'https://ghr.nlm.nih.gov/search?query=%s&show=xml&count=1' % query
    xml = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(xml, 'lxml')
    count = int(soup.find('search_results').attrs['count'])
    return {
        'title': 'NLM',
        'count': count,
        'url': 'https://ghr.nlm.nih.gov/search?query=%s' % query
    }


if __name__ == '__main__':
    print(nlm('TP53'))