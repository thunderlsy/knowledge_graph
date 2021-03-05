#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import jsonify
from search import search_bp
from py2neo import Graph


graph = Graph('http://localhost:7474', username='neo4j', password='neo4j')


@search_bp.route('/<node_name>', methods=["GET"])
def cart_info(node_name):
    # sub_graph = graph.run(gql).to_subgraph()
    # gql = "match (start_node)-[relationship]-(end_node) where start_node.name = '{}' return start_node,relationship,end_node".format(node_name)
    gql = "match (start_node)-[first_relationship]->(second_node) where start_node.name = '{}' WITH start_node,first_relationship,second_node match (second_node)-[second_relationship]->(third_node) return start_node,first_relationship,second_node,second_relationship,third_node".format(
        node_name)

    sub_graph = graph.run(gql).data()

    if not sub_graph:
        json_dict = {
            "error_code": 1,
            "data": "数据库查无此数据",
        }
        return jsonify(json_dict)

    relationship_end = []

    for i in sub_graph:

        if i['second_node']['id'] != i['third_node']['id']:
            relationship_end.append({"source_name": i['second_node']['name'], "source_id": i['second_node']['id'],
                                     "relationship": type(i['second_relationship']).__name__,
                                     "target_name": i['third_node']['name'], "target_id": i['third_node']['id']})

    json_dict = {
        "error_code": 0,
        "start_node": {"start_name": node_name, "start_id": sub_graph[0]['start_node']['id']},
        "relationship_information": relationship_end,
    }

    return jsonify(json_dict)

