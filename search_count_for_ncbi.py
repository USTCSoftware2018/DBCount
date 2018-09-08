import requests
import json
from bs4 import BeautifulSoup


class SearchTerm(object):

    def __init__(self, term):
        self.term = term

    def search_query(self):  # find all databases which are concerning with the item
        name_dic= {'gquery': 'All Databases', 'assembly': 'Assembly', 'biocollections': 'Biocollections', 'bioproject':
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

        url_query = 'https://eutils.ncbi.nlm.nih.gov/gquery' + '?term=' + self.term + '&retmode=xml'
        webdata = requests.get(url=url_query).text
        soup = BeautifulSoup(webdata, 'lxml')
        names = soup.select('dbname')
        nums = soup.select('count')
        result = {}
        results = []

        for name, num in zip(names, nums):
            join_name=name_dic[name.get_text()]
            result[join_name] = int(num.get_text())
            temp_results = json.dumps(result)
            join_result = json.loads(temp_results)
            results.append(join_result)
            result.clear()

        return results


if __name__ == '__main__':
    term = SearchTerm(input("Input the term you would like to search:"))
    print(term.search_query())
