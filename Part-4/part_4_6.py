from rdflib import Graph, RDF, Namespace
from rdflib.extras.infixowl import Class
from owlrl import DeductiveClosure
import owlrl



### RULE - 1 ###
g1 = Graph()
# Define some namespaces
uni = Namespace(
    "http://www.semanticweb.org/neema/ontologies/2024/4/university/")
g1.bind("uni", uni, override=False)

# Create a new class called ITOrHouseKeeping = disjointUnion(Undergraduate, Postgraduate)
IT = Class(uni.IT, graph=g1)
House_Keeping = Class(uni.House_keeping, graph=g1)

UndergraduateOrPostgraduateTA = IT | House_Keeping
UndergraduateOrPostgraduateTA.identifier = uni.ITOrHouseKeeping

uni_onto = Graph().parse("data/university_ontology_final.ttl")

# add g triples on our university ontology
uni_onto += g1
DeductiveClosure(owlrl.OWLRL_Semantics).expand(uni_onto)
print("Rule-1")
for staff in uni_onto.subjects(RDF.type, uni.ITOrHouseKeeping):
    print(staff)

print()

### RULE - 2 ###
g2 = Graph()
g2.bind("uni", uni, override=False)
Undergraduate = Class(uni.Undergraduate, graph=g2)
Professor = Class(uni.Professor, graph=g2)

UndergraduateOrProfessor = Undergraduate | Professor
UndergraduateOrProfessor.identifier = uni.UndergraduateOrProfessor


uni_onto = Graph().parse("data/university_ontology_final.ttl")
uni_onto += g2

DeductiveClosure(owlrl.OWLRL_Semantics).expand(uni_onto)
print("Rule-2")
for person in uni_onto.subjects(RDF.type, uni.UndergraduateOrProfessor):
    print(person)

print()

### RULE - 3 ###
g3 = Graph()
g3.bind("uni", uni, override=False)
Student = Class(uni.Student, graph=g3)
Teaching = Class(uni.Teaching, graph=g3)

StudentOrTeaching = Student | Teaching
StudentOrTeaching.identifier = uni.StudentOrTeaching


uni_onto = Graph().parse("data/university_ontology_final.ttl")
uni_onto += g3

DeductiveClosure(owlrl.OWLRL_Semantics).expand(uni_onto)
print("Rule-3")
for person in uni_onto.subjects(RDF.type, uni.StudentOrTeaching):
    print(person)

print()
