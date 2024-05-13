from rdflib import Graph, URIRef
from rdflib.namespace import RDF

uni_onto = Graph()
uni_onto.parse('data/university_ontology.ttl')

# print all professor names
Professor = "http://www.semanticweb.org/neema/ontologies/2024/4/university/Professor"
for professor in uni_onto.subjects(RDF.type,URIRef(Professor)):
    print(professor)
