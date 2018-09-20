import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re
import urllib.request

import datetime
import threading
import multiprocessing

def NCBI_count(term, all_result):  # find all databases which are concerning with the item
    stime = datetime.datetime.now()

    name_dic = {'gquery': 'All Databases', 'assembly': 'Assembly', 'biocollections': 'Biocollections', 'bioproject':
        'BioProject', 'biosample': 'BioSample', 'biosystems': 'BioSystems', 'books': 'Books', 'clinvar': 'ClinVar',
                'clone': 'Clone', 'cdd': 'Conserved Domains', 'gap': 'dbGaP', 'dbvar': 'dbVar', 'nucest': 'EST',
                'gene': 'Gene', 'genome': 'Genome', 'gds': 'GEO DataSets', 'geoprofiles': 'GEO Profiles', 'nucgss':
                    'GSS', 'gtr': 'GTR', 'homologene': 'HomoloGene', 'ipg': 'Identical Protein Groups', 'medgen':
                    'MedGen', 'mesh': 'MeSH', 'ncbisearch': 'NCBI Web Site', 'nlmcatalog': 'NLM Catalog', 'nuccore':
                    'Nucleotide', 'omim': 'OMIM', 'pmc': 'PMC', 'popset': 'PopSet', 'probe': 'Probe', 'protein':
                    'Protein', 'proteinclusters': 'Protein Clusters', 'pcassay': 'PubChem BioAssay', 'pccompound':
                    'PubChem Compound', 'pcsubstance': 'PubChem Substance', 'pubmed': 'PubMed', 'pubmedhealth':
                    'PubMed Health', 'snp': 'SNP', 'sparcle': 'Sparcle', 'sra': 'SRA', 'structure': 'Structure',
                'taxonomy': 'Taxonomy', 'toolkit': 'ToolKit', 'toolkitall': 'ToolKitAll', 'toolkitbookgh':
                    'ToolKitBookgh', 'unigene': 'UniGene'}
    url_query = 'https://eutils.ncbi.nlm.nih.gov/gquery' + '?term=' + term + '&retmode=xml'
    webdata = requests.get(url=url_query).text
    soup = BeautifulSoup(webdata, 'lxml')
    names = soup.select('dbname')
    nums = soup.select('count')
    result = {}
    results = []
    for name, num in zip(names, nums):
        join_name = name_dic[name.get_text()]
        result['title'] = join_name
        result['count'] = int(num.get_text())
        result['url'] = 'https://www.ncbi.nlm.nih.gov/' + name.get_text() + '/?term=' + term
        temp_results = json.dumps(result)
        join_result = json.loads(temp_results)
        all_result.append(join_result)
        results.append(join_result)
        result.clear()

    print('ncbi: %d' % (datetime.datetime.now() - stime).seconds)

    return results


def NLM_count(keyword, all_result):
    stime = datetime.datetime.now()

    url = 'https://ghr.nlm.nih.gov/search?query=%s&show=xml&count=1' % keyword
    xml = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(xml, 'lxml')
    count = int(soup.find('search_results').attrs['count'])
    result = {
        'title': 'NLM',
        'count': count,
        'url': 'https://ghr.nlm.nih.gov/search?query=%s' % keyword
    }
    all_result.append(result)

    print('nlm: %d' % (datetime.datetime.now () - stime).seconds)
    return result


def RCSB_count(keyword, all_result):
    stime = datetime.datetime.now()

    query_text = """
        <orgPdbQuery>
        <queryType>org.pdb.query.simple.AdvancedKeywordQuery</queryType>
        <keywords>%s</keywords>
        </orgPdbQuery>""" % keyword
    data = query_text.encode('utf-8')
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    url = 'https://www.rcsb.org/pdb/rest/search'
    req = urllib.request.Request(url, data=data, headers=headers)
    res = urllib.request.urlopen(req).read()
    count = str(res).count('\\n')
    search_url = 'http://www.rcsb.org/pdb/search/navbarsearch.do?f=&q=%s' % keyword
    result = {
            'title': 'RCSB',
            'count': count,
            'url': search_url,
    }
    all_result.append(result)

    print('rcsb: %d' % (datetime.datetime.now () - stime).seconds)

    return result


def iGEMParts_count(keyword, all_result):
    # 因为igem的query service(看起来是10年的一个参赛项目)已经挂掉了,    没办法用API获得模糊搜索的结果, 目前爬取的是原网站.
    stime = datetime.datetime.now()
    url = 'http://parts.igem.org/Special:Search?search=%s' % keyword
    headers = {
    'accept': 'text / html, application / xhtml + xml, application /    xml; q = 0.9, image / webp, image / apng, * / *;q = 0.8'
    }
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find(attrs={'class': 'results-info'})
    count = int(div.find_all('strong')[-1].text)
    search_url = 'http://parts.igem.org/Special:Search?search=%s' % keyword
    result = {
            'title': 'iGEM Parts',
            'count': count,
            'url': search_url,
    }
    all_result.append(result)

    print('igem: %d' % (datetime.datetime.now () - stime).seconds)
    return result


def UniProt_count(keyword, all_result):
    stime = datetime.datetime.now()

    query_string = urlencode({'query':keyword})
    query_url = 'https://www.uniprot.org/uniprot/?%s&sort=score' % query_string
    response = requests.get(query_url)
    bs = BeautifulSoup(response.content, features='html.parser')
    count = int(re.findall("\d+",bs.find('div',class_='main-aside').find('script').text)[0])
    result = {
            'title': 'UniProt',
            'count':count,
            'url': query_url,
    }
    all_result.append(result)

    print('uniprot: %d' % (datetime.datetime.now () - stime).seconds)
    return result


def Taxonomy_count(keyword, all_result):
    stime = datetime.datetime.now()

    query_string = urlencode({'query': keyword})
    query_url = 'https://www.uniprot.org/taxonomy/?%s&sort=score' % query_string
    response = requests.get(query_url)
    bs = BeautifulSoup(response.content, features='html.parser')
    count = int(re.findall("\d+",bs.find('div',class_='main-aside').find('script').text)[0])
    result = {
            'title': 'Taxonomy',
            'count':count,
            'url': query_url,
    }
    all_result.append(result)

    print('tax: %d' % (datetime.datetime.now () - stime).seconds)
    return result


class Spiders(threading.Thread):
    all_spiders = [NCBI_count, NLM_count, RCSB_count, iGEMParts_count, UniProt_count, Taxonomy_count, ]
    results = []
    thread_pool = []
    process_pool = []

    def __init__(self, keyword: str):
        super(Spiders, self).__init__()
        self.keyword = keyword
        for spider in self.all_spiders:
            self.thread_pool.append(threading.Thread(target=spider, args=(self.keyword, self.results)))
            self.process_pool.append(multiprocessing.Process(target=spider, args=(self.keyword, [])))

    def count_compare(self):
        stime = datetime.datetime.now ()
        for spider in self.all_spiders:
            spider(self.keyword, [])
        print('All time cost: %d' % (datetime.datetime.now () - stime).seconds)

    def count_multithread(self):
        stime = datetime.datetime.now()
        for th in self.thread_pool:
            th.start()
        for th in self.thread_pool:
            threading.Thread.join(th)
        print('All time cost: %d' % (datetime.datetime.now() - stime).seconds)
        return self.results

    def count_multiproccess(self):
        stime = datetime.datetime.now ()
        for th in self.process_pool:
            th.start()
        for th in self.process_pool:
            multiprocessing.Process.join(th)
        print('All time cost: %d' % (datetime.datetime.now () - stime).seconds)


if __name__ == "__main__":
    s = Spiders('p53')
    print('Time cost for compare:')
    s.count_compare()
    print('Time cost using multiprocessing:')
    s.count_multiproccess()
    print('Time cost using multithreading:')
    print(s.count_multithread())
