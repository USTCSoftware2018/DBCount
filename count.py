import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re
import urllib.request
import datetime
import threading
import multiprocessing


# count = -1 means TLE
# count = 0 means there is nothing in the database
def NCBI_count(term, all_result):  # find all databases which are concerning with the item
    stime = datetime.datetime.now()
    timelimit=5
    result = {}
    results = []
    name_dic = {'assembly': 'Assembly', 'biocollections': 'Biocollections', 'bioproject':
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
    # if found nothing in NCBI then url is the homepage of NCBI.

    if (datetime.datetime.now() - stime).seconds > timelimit:
        result = {
            'title': 'NCBI',
            'count': -1,
            'url': 'https://www.ncbi.nlm.nih.gov/',
        }
        print("Time Limit Exceed.")
        return result
    if webdata is None:
        result = {
            'title': 'NCBI',
            'count': 0,
            'url': 'https://www.ncbi.nlm.nih.gov/',
        }
        return None
    soup = BeautifulSoup(webdata, 'lxml')
    names = soup.select('dbname')
    nums = soup.select('count')

    for name, num in zip(names, nums):
        join_name = name_dic[name.get_text()]
        result = {
            'title': join_name,
            'count': int(num.get_text()),
            'url': 'https://www.ncbi.nlm.nih.gov/' + name.get_text() + '/?term=' + term
        }
        results.append(result)
        all_result.append(result)
    # print('ncbi: %f' % (datetime.datetime.now() - stime).seconds)

    return results


def NLM_count(keyword, all_result):
    stime = datetime.datetime.now()
    timelimit = 3
    url = 'https://ghr.nlm.nih.gov/search?query=%s&show=xml&count=1' % keyword
    xml = urllib.request.urlopen(url).read()
    if (datetime.datetime.now() - stime).seconds > timelimit:
        result = {
            'title': 'NLM',
            'count': -1,
            'url': 'https://ghr.nlm.nih.gov/search?query=%s' % keyword
        }
        print("Time Limit Exceed.")
        return result
    if xml is None:
        result = {
            'title': 'NLM',
            'count': 0,
            'url': 'https://ghr.nlm.nih.gov/search?query=%s' % keyword
        }
        return result
    soup = BeautifulSoup(xml, 'lxml')
    if soup.find('search_results') is None:
        return None
    count = int(soup.find('search_results').attrs['count'])
    result = {
        'title': 'NLM',
        'count': count,
        'url': 'https://ghr.nlm.nih.gov/search?query=%s' % keyword
    }
    all_result.append(result)

    # print('nlm: %f' % (datetime.datetime.now() - stime).seconds)
    return result


def RCSB_count(keyword, all_result):
    stime = datetime.datetime.now()
    timelimit = 3
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

    if (datetime.datetime.now() - stime).seconds > timelimit:
        result = {
            'title': 'RCSB',
            'count': -1,
            'url': 'http://www.rcsb.org/pdb/search/navbarsearch.do?f=&q=%s' % keyword,
        }
        print("Time Limit Exceed.")
        return result

    res = urllib.request.urlopen(req).read()
    if res is None:
        result = {
            'title': 'RCSB',
            'count': -1,
            'url': 'http://www.rcsb.org/pdb/search/navbarsearch.do?f=&q=%s' % keyword,
        }
        return result

    count = str(res).count('\\n')
    search_url = 'http://www.rcsb.org/pdb/search/navbarsearch.do?f=&q=%s' % keyword
    result = {
        'title': 'RCSB',
        'count': count,
        'url': search_url,
    }
    all_result.append(result)

    # print('rcsb: %f' % (datetime.datetime.now() - stime).seconds)

    return result


def iGEMParts_count(keyword, all_result):
    # 因为igem的query service(看起来是10年的一个参赛项目)已经挂掉了,    没办法用API获得模糊搜索的结果, 目前爬取的是原网站.
    stime = datetime.datetime.now()
    url = 'http://parts.igem.org/Special:Search?search=%s' % keyword
    headers = {
        'accept': 'text / html, application / xhtml + xml, application /    xml; q = 0.9, image / webp, image / apng, * / *;q = 0.8'
    }
    req = urllib.request.Request(url, headers=headers)

    if (datetime.datetime.now() - stime).seconds > 3:
        result = {
            'title': 'iGEM Parts',
            'count': -1,
            'url': 'http://parts.igem.org/Special:Search?search=%s' % keyword,
        }
        print("Time Limit Exceed.")
        return result
    html = urllib.request.urlopen(req).read()

    if html is None:
        result = {
            'title': 'iGEM Parts',
            'count': 0,
            'url': 'http://parts.igem.org/Special:Search?search=%s' % keyword,
        }
        return result

    soup = BeautifulSoup(html, 'lxml')
    div = soup.find(attrs={'class': 'results-info'})

    if div is None:
        result = {
            'title': 'iGEM Parts',
            'count': 0,
            'url': 'http://parts.igem.org/Special:Search?search=%s' % keyword,
        }
        return result

    count = int(div.find_all('strong')[-1].text)
    search_url = 'http://parts.igem.org/Special:Search?search=%s' % keyword
    result = {
        'title': 'iGEM Parts',
        'count': count,
        'url': search_url,
    }
    all_result.append(result)

    # print('igem: %f' % (datetime.datetime.now() - stime).seconds)
    return result


def UniProt_count(keyword, all_result):
    stime = datetime.datetime.now()
    timelimit=2
    query_string = urlencode({'query': keyword})
    query_url = 'https://www.uniprot.org/uniprot/?%s&sort=score' % query_string
    response = requests.get(query_url)

    if (datetime.datetime.now() - stime).seconds > timelimit:
        result = {
            'title': 'UniProt',
            'count': -1,
            'url': query_url,
        }
        print("Time Limit Exceed.")
        return result
    bs = BeautifulSoup(response.content, features='html.parser')
    if bs.find('div', class_='main-aside') is None or bs.find('div', class_='main-aside').find('script') is None:
        result = {
            'title': 'UniProt',
            'count': 0,
            'url': query_url,
        }
        return result

    count = int(re.findall("\d+", bs.find('div', class_='main-aside').find('script').text)[0])
    result = {
        'title': 'UniProt',
        'count': count,
        'url': query_url,
    }
    all_result.append(result)

    # print('uniprot: %f' % (datetime.datetime.now() - stime).seconds)
    return result


def Taxonomy_count(keyword, all_result):
    stime = datetime.datetime.now()

    query_string = urlencode({'query': keyword})
    query_url = 'https://www.uniprot.org/taxonomy/?%s&sort=score' % query_string
    response = requests.get(query_url)
    if (datetime.datetime.now() - stime).seconds > 2:
        result = {
            'title': 'Taxonomy',
            'count': -1,
            'url': query_url,
        }
        print("Time Limit Exceed.")
        return result

    if response is None:
        result = {
            'title': 'Taxonomy',
            'count': 0,
            'url': query_url,
        }
        return result

    bs = BeautifulSoup(response.content, features='html.parser')
    if bs.find('div', class_='main-aside').find('script') is None:
        result = {
            'title': 'Taxonomy',
            'count': 0,
            'url': query_url,
        }
        return result

    count = int(re.findall("\d+", bs.find('div', class_='main-aside').find('script').text)[0])
    result = {
        'title': 'Taxonomy',
        'count': count,
        'url': query_url,
    }
    all_result.append(result)

    # print('tax: %f' % (datetime.datetime.now() - stime).seconds)
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
        stime = datetime.datetime.now()
        print(stime)
        for spider in self.all_spiders:
            spider(self.keyword, [])
        print('All time cost: %f' % (datetime.datetime.now() - stime).seconds)

    def count_multithread(self):
        stime = datetime.datetime.now()
        total_timeout = 5  # total time limit
        for th in self.thread_pool:
            th.setDaemon(True)
            th.start()

        for th in self.thread_pool:

            if (datetime.datetime.now() - stime).seconds > total_timeout:
                raise TimeoutError("Timeout")
            threading.Thread.join(th, timeout=1)  # single thread time limit

        print('All time cost: %f' % (datetime.datetime.now() - stime).seconds)
        return self.results

    def count_multiproccess(self):
        stime = datetime.datetime.now()
        total_timeout = 5
        for th in self.process_pool:
            th.start()

        for th in self.process_pool:
            if (datetime.datetime.now() - stime).seconds > total_timeout:
                print("Time Limit Exceed.")
            multiprocessing.Process.join(th, timeout=1)
        print('All time cost: %d' % (datetime.datetime.now() - stime).seconds)


if __name__ == "__main__":
    s = Spiders(input("Input the term: "))
    print(s.count_multithread())
