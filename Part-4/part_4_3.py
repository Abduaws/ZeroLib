from rdflib import Graph, URIRef
from owlrl import DeductiveClosure
import  owlrl


print("Before inference")

# print all teaching staff before inference
uni_onto = Graph()
uni_onto.parse('data/university_ontology_final.rdf')
teaches = "http://www.semanticweb.org/neema/ontologies/2024/4/university/teaches"
for teacher in uni_onto.subject_objects(predicate=URIRef(teaches)):
    print(teacher)

# Applying reasoning
DeductiveClosure(owlrl.OWLRL_Semantics).expand(uni_onto)

# print all teaching staff after inference
print("After inference")
teaches = "http://www.semanticweb.org/neema/ontologies/2024/4/university/teaches"
for teacher in uni_onto.subject_objects(predicate=URIRef(teaches)):
    print(teacher)
