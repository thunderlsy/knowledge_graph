#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import jsonify, current_app
from search import search_bp
from flask_restful import Resource, Api

search_api = Api(search_bp)


class ThreeLevelSearch(Resource):

    def get(self, node_name):

        # 三级查询
        gql = "match (start_node)-[first_relationship]->(second_node) where start_node.name = '{}' WITH start_node,first_relationship,second_node match (second_node)-[second_relationship]->(third_node) return start_node,first_relationship,second_node,second_relationship,third_node".format(
            node_name)

        sub_graph = current_app.graph.run(gql).data()

        if not sub_graph:
            json_dict = {
                "error_code": 1,
                "data": "数据库查无此数据",
            }
            return json_dict

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
        # return json_dict


search_api.add_resource(ThreeLevelSearch, '/<node_name>', endpoint="Three_Level_Search")
