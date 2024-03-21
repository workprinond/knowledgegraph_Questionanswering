from SPARQLWrapper import SPARQLWrapper, JSON
from string import Template
import pandas as pds

sparql = SPARQLWrapper("http://rdf.disgenet.org/sparql/")


def getCapitalOf():
    # template = Template("""
    # PREFIX dbo: <http://dbpedia.org/ontology/>
    # PREFIX dbr: <http://dbpedia.org/resource/>
    # SELECT ?country ?capital
    #  WHERE {
    #      ?country a dbo:Country.
    #      <http://dbpedia.org/resource/$country> dbo:capital ?capital.
    #     FILTER NOT EXISTS { ?country dbo:dissolutionYear ?yearEnd }
    # }
    # Limit 1
    # """)
    # country = list(map(lambda x: x.capitalize()+'_',country_raw.split('_')))
    # s = template.substitute(country=''.join(country)[0:-1])

    prefixes = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX void: <http://rdfs.org/ns/void#>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX so: <http://purl.obolibrary.org/obo/SO_>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX up: <http://purl.uniprot.org/core/>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dctypes: <http://purl.org/dc/dcmitype/>
PREFIX wi: <http://http://purl.org/ontology/wi/core#>
PREFIX eco: <http://http://purl.obolibrary.org/obo/eco.owl#>
PREFIX prov: <http://http://http://www.w3.org/ns/prov#>
PREFIX pav: <http://http://http://purl.org/pav/>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX dto: <http://diseasetargetontology.org/dto/>
    """

    template = Template(
        """
$prefix


SELECT DISTINCT ?umls ?umlsTerm ?doid ?doTerm 
WHERE { 
	?gda sio:SIO_000628 ?umls .
	?umls dcterms:title ?umlsTerm ;
		skos:exactMatch ?doid .
	?doid rdfs:label ?doTerm ;
		rdfs:subClassOf+ <http://purl.obolibrary.org/obo/DOID_2394> .
	FILTER regex(?umls, "umls/id")
}
LIMIT 5
        """
    )

    s = template.substitute(prefix=''.join(prefixes))

    # return s
    sparql.setQuery(s)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    vars = results['head']['vars']
    bindings = results['results']['bindings']


    df = pds.DataFrame(list(map(lambda x: helper(x, vars), bindings)))
    styler = df.style.highlight_max(axis='index')
    breakpoint()
    return df

    # if len(results['results']['bindings']) == 0:
    #     return 'No Capital for ' + country_raw + ', please check the spelling'
    # return results['results']['bindings'][0]['capital']['value'].split('/')[-1]



def helper(entry, vars):
    res = {}
    for key in vars:
        res[key] = entry[key]['value']
    return res

# n = 'United_states'
print(getCapitalOf())
