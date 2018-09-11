# coding=utf-8
import urllib
from bs4 import BeautifulSoup


def rcsb(query):
    query_text = """
        <orgPdbQuery>
        <queryType>org.pdb.query.simple.AdvancedKeywordQuery</queryType>
        <keywords>%s</keywords>
        </orgPdbQuery>""" % query
    data = query_text.encode('utf-8')
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    url = 'https://www.rcsb.org/pdb/rest/search'
    req = urllib.request.Request(url, data=data, headers=headers)
    result = urllib.request.urlopen(req).read()
    count = str(result).count('\\n')
    search_url = 'http://www.rcsb.org/pdb/search/navbarsearch.do?f=&q=%s' % query
    return {
            'title': 'RCSB',
            'url': search_url,
            'count': count,
            }


def igem_parts(query):
    # 因为igem的query service(看起来是10年的一个参赛项目)已经挂掉了, 没办法用API获得模糊搜索的结果, 目前爬取的是原网站.
    url = 'http://parts.igem.org/Special:Search?search=%s' % query
    headers = {
        'accept': 'text / html, application / xhtml + xml, application / xml; q = 0.9, image / webp, image / apng, * / *;q = 0.8'
    }
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find(attrs={'class': 'results-info'})
    count = int(div.find_all('strong')[-1].text)
    search_url = 'http://parts.igem.org/Special:Search?search=%s' % query
    return {
            'title': 'iGEM Parts',
            'url': search_url,
            'count': count,
            }


if __name__=='__main__':
    print(rcsb('p53'))
    print(igem_parts('p53'))
