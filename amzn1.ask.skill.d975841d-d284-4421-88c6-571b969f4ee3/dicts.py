########################################################################################

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
########################################################################################

disease_dict = {
    'cancer': "162",
    'melanoma': "1909",
    'HIV': "526",
    'corona': "0080600",
    'flu': "8469",
    'alzheimer\'s disease': '10652',
    'anxiety': '2030',
    'rabies':'11260',
    'asthma':'2841',
    'stroke':'6713',
    'ebola hemorrhagic fever':'4325',
    'tuberculosis':'399',
    'diabetes mellitus':'9351',
    'diarrhea':'13250',
    'leukemia':'1240',
    'osteoarthritis':'8398',
    'hypertension':'10763',
    'myocardial infarction':'5844',
    'anemia':'2355',
    'measles':'8622',
    # 'glaucoma': '1686'
}

