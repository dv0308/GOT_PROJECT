from flask import Flask,jsonify,make_response
from py2neo import Graph
from py2neo.matching import *

app = Flask(__name__)
graph = Graph("bolt://localhost:11005", auth=("neo4j", "hello123@#"))

# orm
@app.route('/v1/characters', methods=["GET"])
def get_all_characters():
    nodes = NodeMatcher(graph)
    characters = list(nodes.match("Character").all())
    return make_response(jsonify(characters), 200)

@app.route("/v1/characters/<id>", methods=["GET"])
def get_character_by_id(id):
    nodes = NodeMatcher(graph)
    character = nodes[int(id)]
    return make_response(jsonify(character))

#Raw Cypher
@app.route("/v1/characters/<name>/betrayed_by", methods=["GET"])
def get_betrayls(name: str):
    character = graph.run(
        "MATCH (c:Character) WHERE c.name= $name return c", name=name) .evaluate()
    if not character:
        return make_response(
            jsonify(error=f"could not find character with {name=}"), 400)

    cypher_query = "MATCH (trator)-[betrayed]->(victim:Character{ name:$name }) RETURN trator,betrayed,victim"
    query_result = graph.run(cypher_query, name=name)
    betrayels = [betrayel for betrayel in query_result]

    return make_response(jsonify(betrayels))



if __name__ == '__main__':
    app.run()