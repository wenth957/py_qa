from py2neo import Graph
import os


neo4j_url = "http://localhost:7474"
neo4j_auth = ("neo4j", "baby1234")


class Neo4jQuery:

    def __init__(self, url=neo4j_url, author=neo4j_auth):
        self.graph = Graph(url, auth=author)

    def run(self, cql):
        result = []
        matches = self.graph.run(cql)
        for data in matches:
            result.append(data.items()[0][1])
        return result





