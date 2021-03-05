from flask import Flask, jsonify
from flask_cors import CORS
from py2neo import Graph, Node, Relationship, walk
from cart import cart_bp
from search import search_bp

# graph = Graph('http://localhost:7474', username='neo4j', password='neo4j')


def create_flask_app(config):
    """
    创建Flask应用
    :param config: 配置对象
    :return: Flask应用
    """
    the_app = Flask(__name__)
    CORS(the_app)
    the_app.config.from_object(config)

    # 从环境变量指向的配置文件中读取的配置信息会覆盖掉从配置对象中加载的同名参数
    the_app.config.from_envvar("PROJECT_SETTING", silent=True)
    return the_app


class DefaultConfig(object):
    """默认配置"""
    SECRET_KEY = 'chris!@#$%^&*()'
    JSON_AS_ASCII = False


class DevelopmentConfig(DefaultConfig):
    DEBUG = True


class ProductionConfig(DefaultConfig):
    DEBUG = False


# app = create_flask_app(ProductionConfig)
app = create_flask_app(DevelopmentConfig)
app.register_blueprint(cart_bp)
app.register_blueprint(search_bp)


@app.route("/")
def index():
    print(app.config['SECRET_KEY'])
    url_dict = {rule.rule: rule.endpoint for rule in app.url_map.iter_rules()}

    return jsonify(url_dict)


# @app.route("/search/<node_name>", methods=['GET'])
# def search(node_name):
#     # sub_graph = graph.run(gql).to_subgraph()
#     # gql = "match (start_node)-[relationship]-(end_node) where start_node.name = '{}' return start_node,relationship,end_node".format(node_name)
#     gql = "match (start_node)-[first_relationship]->(second_node) where start_node.name = '{}' WITH start_node,first_relationship,second_node match (second_node)-[second_relationship]->(third_node) return start_node,first_relationship,second_node,second_relationship,third_node".format(
#         node_name)
#
#     sub_graph = graph.run(gql).data()
#
#     if not sub_graph:
#         json_dict = {
#             "error_code": 1,
#             "data": "数据库查无此数据",
#         }
#         return jsonify(json_dict)
#
#     relationship_end = []
#
#     for i in sub_graph:
#
#         if i['second_node']['id'] != i['third_node']['id']:
#             relationship_end.append({"source_name": i['second_node']['name'], "source_id": i['second_node']['id'],
#                                      "relationship": type(i['second_relationship']).__name__,
#                                      "target_name": i['third_node']['name'], "target_id": i['third_node']['id']})
#
#     json_dict = {
#         "error_code": 0,
#         "start_node": {"start_name": node_name, "start_id": sub_graph[0]['start_node']['id']},
#         "relationship_information": relationship_end,
#     }
#
#     return jsonify(json_dict)


app.run('0.0.0.0', 5000)
