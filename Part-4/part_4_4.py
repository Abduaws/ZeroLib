from rdflib import Graph, URIRef, RDF
from owlrl import DeductiveClosure
import  owlrl, sys
from colorama import Fore, Style

uni_onto = Graph()
uni_onto.parse("data/university_ontology_final.ttl")

# Applying reasoning
DeductiveClosure(owlrl.OWLRL_Semantics).expand(uni_onto)

studentName = input("Please enter the student name: ")

base_uri = "http://www.semanticweb.org/neema/ontologies/2024/4/university/"


studentURI = base_uri[:62] + studentName
studentClassURI = base_uri[:62] + "Student"
if (URIRef(studentURI), RDF.type, URIRef(studentClassURI)) in uni_onto:
    for s,p,o in uni_onto.triples((URIRef(studentURI), None, None)):
        if p[62:] in ["hasName","hasPhonenumber","studentID","hasAge"]:
            print(p[62:],":",o)
else:
    print(Fore.RED + "Student not found!" + Fore.RESET)
    # print(Style.RESET_ALL)


