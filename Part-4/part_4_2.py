from rdflib import Graph, URIRef


uni_onto = Graph()
uni_onto.parse('data/university_ontology.ttl')

query = open("data/query_2.txt").read()

query_result = uni_onto.query(query)
for row in query_result:
    print(row.professor)
