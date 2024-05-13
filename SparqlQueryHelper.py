import os
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class SparqlQueryHelper:
    def __init__(self):
        self.sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        self.graph = Graph()
        self.graph.parse(resource_path("./resources/ontology.ttl"))

    def buildQuery(self, regex_filter="", actor_filter="", director_filter="",
                   genre_filter="", country_filter="", year_filter="", modes=None):

        if modes is None:
            modes = [0, 0, 0, 0]

        sparql_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>

        SELECT DISTINCT ?title ?abstract (GROUP_CONCAT(DISTINCT ?actor; SEPARATOR=", ") AS ?actors)
                        (GROUP_CONCAT(DISTINCT ?director; SEPARATOR=", ") AS ?directors)
                        (GROUP_CONCAT(DISTINCT ?genre; SEPARATOR=", ") AS ?genres)
                        (GROUP_CONCAT(DISTINCT ?country; SEPARATOR=", ") AS ?countries)
                        ?year
        WHERE {
          ?film rdf:type dbo:Film;
               dbo:abstract ?abstract;
               rdfs:label ?title.

          FILTER(LANGMATCHES(LANG(?title), "en"))
          FILTER(LANGMATCHES(LANG(?abstract), "en"))\n\t\t  """

        sparql_query = self.addFilter(sparql_query, "title", regex_filter, modes[0])
        sparql_query = self.addOptional(sparql_query, "dbo:starring", "actor", actor_filter, modes[1])
        sparql_query = self.addOptional(sparql_query, "dbo:director", "director", director_filter, modes[2])
        sparql_query = self.addOptional(sparql_query, "dbo:genre", "genre", genre_filter, modes[3])
        sparql_query = self.addOptional(sparql_query, "dbo:country", "country", country_filter)
        sparql_query = self.addOptional(sparql_query, "dbo:releaseDate", "year", year_filter)
        sparql_query += """
        }
        GROUP BY ?title ?year ?abstract
        LIMIT 100
        """
        print(sparql_query)
        return sparql_query

    @staticmethod
    def addFilter(query, variable, user_input, mode):
        if user_input:
            if variable != "year":
                query += f'\n\t\t  FILTER ({"" if mode == 0 else "!"}REGEX(?{variable}, ".*{user_input}.*", "i"))\n\t\t'
                if variable == "title":
                    query += "\n\t\t  "
            else:
                query += f'\n\t\t  FILTER (?year = {user_input})'
        return query

    @staticmethod
    def addOptional(query, filmProperty, variable, user_input, mode=0):
        optionalBody = f"""
            ?film {filmProperty} ?{variable}Resource.
            ?{variable}Resource rdfs:label ?{variable}.
            FILTER(LANGMATCHES(LANG(?{variable}), "en")) 
        """
        if variable == "year":
            optionalBody = f"""
                ?film dbo:releaseDate ?date.
                BIND(IF(BOUND(?date), YEAR(?date), "") AS ?year).
            """
        optionalBody = SparqlQueryHelper.addFilter(optionalBody, variable, user_input, mode)
        if user_input:
            query += optionalBody
        else:
            query += "OPTIONAL {\n" + optionalBody + "\n\t\t  }\n\t\t  "
        return query

    def executeQuery(self, query):
        allResults = []
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        for result in results["results"]["bindings"]:
            allResults.append(result)
        return allResults

    def executeUniversityQuery(self, query):
        results = self.graph.query(f"""
        PREFIX uni: <http://www.semanticweb.org/neema/ontologies/2024/4/university/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xml: <http://www.w3.org/XML/1998/namespace>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        {query}
        """)
        return results


if __name__ == "__main__":
    sparqlQueryHelper = SparqlQueryHelper()

    title = input("Enter Regex filter for film titles (leave blank for no filter): ")
    actor = input("Enter Regex filter for actors (leave blank for no filter): ")
    director = input("Enter Regex filter for directors (leave blank for no filter): ")
    genre = input("Enter Regex filter for genres (leave blank for no filter): ")
    country = input("Enter Regex filter for countries (leave blank for no filter): ")
    year = input("Enter year filter for film release (leave blank for no filter): ")

    searchQuery = sparqlQueryHelper.buildQuery(title, actor, director, genre, country, year)
    sparqlQueryHelper.executeQuery(searchQuery)
