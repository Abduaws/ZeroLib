import rdflib

g = rdflib.Graph()

g.parse("./resources/ontology.ttl")

results = g.query("""
PREFIX uni: <http://www.semanticweb.org/neema/ontologies/2024/4/university/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xml: <http://www.w3.org/XML/1998/namespace>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>


  

SELECT ?elective ?student ?studentName ?studentAge ?studentPhone ?studentID
WHERE {
    ?elective rdf:type uni:Elective .
    ?elective uni:registeredBy ?student.
    OPTIONAL {?student uni:hasLabel ?studentName}
    OPTIONAL {?student uni:hasAge ?studentAge}
    OPTIONAL {?student uni:hasPhonenumber ?studentPhone}
    OPTIONAL {?student uni:studentID ?studentID}
}

""")

for result in results:
    result.asdict()
    print(result)