from rdflib import Graph, RDF, OWL, BNode,Namespace
import rdflib.extras
from rdflib.extras.infixowl import Class, EnumeratedClass, AllClasses
from owlrl import DeductiveClosure
import  owlrl
import rdflib
import rdflib.extras.infixowl

# Create an empty RDF graph

g = Graph()
# Define some namespaces
uni = Namespace("http://www.semanticweb.org/neema/ontologies/2024/4/university/")
g.bind("uni",uni,override=False)

# Create a new class called UndergraduateOrPostgraduate = disjointUnion(Undergraduate, Postgraduate)
Undergraduate = Class(uni.Undergraduate,graph=g)
PostgraduateTA = Class(uni.Postgrad_TA,graph=g)

UndergraduateOrPostgraduateTA = Undergraduate | PostgraduateTA
UndergraduateOrPostgraduateTA.identifier = uni.UnderGraduateOrPostgraduateTA

g.serialize("data/rule_5.ttl")

uni_onto = Graph().parse("data/university_ontology_final.ttl")

# add g triples on our university ontology
uni_onto += g
DeductiveClosure(owlrl.OWLRL_Semantics).expand(uni_onto)
for student in uni_onto.subjects(RDF.type,uni.UnderGraduateOrPostgraduateTA):
    print(student)



