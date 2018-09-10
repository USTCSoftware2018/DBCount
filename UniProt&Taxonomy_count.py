from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urlencode
import re

class UniProtCount():
    def __init__(self, keyword: str):
        self.keyword = keyword
        
    def get_info(self):
        query_string = urlencode({'query':self.keyword})
        query_url = 'https://www.uniprot.org/uniprot/?%s&sort=score' % query_string
        response = requests.get(query_url)
        bs = BeautifulSoup(response.content, features='html.parser')
        result = int(re.findall("\d+",bs.find('div',class_='main-aside').find('script').text)[0])
        return {
                'title': 'UniProt',
                'url': query_url,
                'count':result,
                }
        
class TaxonomyCount():
    def __init__(self, keyword: str):
        self.keyword = keyword
        
    def get_info(self):
        query_string = urlencode({'query': self.keyword})
        query_url = 'https://www.uniprot.org/taxonomy/?%s&sort=score' % query_string
        response = requests.get(query_url)
        bs = BeautifulSoup(response.content, features='html.parser')
        result = int(re.findall("\d+",bs.find('div',class_='main-aside').find('script').text)[0])
        return {
                'title': 'Taxonomy',
                'url': query_url,
                'count':result,
                }
