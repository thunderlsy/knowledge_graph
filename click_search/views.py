#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import jsonify, current_app, session, g
from click_search import click_search_bp
from flask_restful import Resource, Api
import time
from pymongo import MongoClient

# client = MongoClient(host='127.0.0.1', port=27017)
# collection = client['test']["deduplication_contents"]

search_api = Api(click_search_bp)


def timing_one(func):
    def inner(*args, **kwargs):
        begin = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("函数执行花费%f,(1号计时器)" % (end - begin))
        return result

    return inner


def timing_two(func):
    def inner(*args, **kwargs):
        begin = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("函数执行花费%f,(2号计时器)" % (end - begin))
        return result

    return inner


class ThreeLevelSearch(Resource):
    method_decorators = {
        "get": [timing_one]
    }

    def get(self, node_id):

        json_dict = {
            "error_code": 666,
            "data": "数据库查无此数据",
        }

        # 三级查询
        gql = "match (start_node)-[first_relationship]->(second_node) where start_node.id = '{}' WITH start_node,first_relationship,second_node match (second_node)-[second_relationship]->(third_node) return start_node,first_relationship,second_node,second_relationship,third_node".format(
            node_id)

        # 返回查询语句放入current_app
        # last_gql = current_app.last_search
        # print(last_gql)

        sub_graph = current_app.graph.run(gql).data()

        if not sub_graph:
            sub_graph = two_level_search(node_id)

            # if not sub_graph:
            #     content_gql = ""

            return sub_graph if sub_graph else json_dict

        # if not sub_graph:
        #     return json_dict

        Sou_Tar_List = []
        temp_second_id_list = []
        for i in sub_graph:

            if i['second_node']['id'] != i['third_node']['id']:
                # 添加二级与三级节点的关系
                Sou_Tar_List.append({"source_name": i['second_node']['name'], "source_id": i['second_node']['id'],
                                     "relationship": type(i['second_relationship']).__name__,
                                     "target_name": i['third_node']['name'], "target_id": i['third_node']['id']})

                # 添加一级与二级节点的关系
                if i['second_node']['id'] not in temp_second_id_list:
                    Sou_Tar_List.append({"source_name": i['start_node']['name'], "source_id": i['start_node']['id'],
                                         "relationship": type(i['first_relationship']).__name__,
                                         "target_name": i['second_node']['name'], "target_id": i['second_node']['id']})
                    temp_second_id_list.append(i['second_node']['id'])
        json_dict = {
            "error_code": 0,
            "start_node": {"start_name": sub_graph[0]['start_node']['name'],
                           "start_id": sub_graph[0]['start_node']['id']},
            "relationship_information": Sou_Tar_List,
        }

        return jsonify(json_dict)
        # return json_dict


def two_level_search(node_id):
    # 二级查询
    gql = "match (source_node)-[r]->(target_node) where source_node.id = '{}' return source_node,r,target_node".format(
        node_id)

    sub_graph = current_app.graph.run(gql).data()

    if not sub_graph:

        content_gql = "match (source_node:Entity) where source_node.id = '{}' return source_node".format(node_id)

        content_graph = current_app.graph.run(content_gql).data()
        if content_graph[0]['source_node']['is_content'] == 'true':
            # t = collection.find_one({"_id": node_id})['html_str']
            content_html = current_app.mongo.find_one({"_id": node_id})['html_str']
            json_dict = {
                "error_code": 1,
                "content_html": content_html,
            }
            return json_dict
        print(content_gql, content_graph)

        return

    Sou_Tar_List = []

    for i in sub_graph:
        Sou_Tar_List.append({"source_name": i['source_node']['name'],
                             "source_id": i['source_node']['id'],
                             "relationship": type(i['r']).__name__,
                             "target_name": i['target_node']['name'],
                             "target_id": i['target_node']['id']})
    json_dict = {
        "error_code": 0,
        "start_node": {"start_name": sub_graph[0]['source_node']['name'],
                       "start_id": sub_graph[0]['source_node']['id']},
        "relationship_information": Sou_Tar_List,
    }
    return jsonify(json_dict)


search_api.add_resource(ThreeLevelSearch, '/<node_id>', endpoint="Three_Level_Search")
