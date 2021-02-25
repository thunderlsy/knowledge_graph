from flask import Flask, jsonify
from py2neo import Graph, Node, Relationship, walk

graph = Graph('http://localhost:7474', username='neo4j', password='neo4j')


def create_flask_app(config):
    """
    创建Flask应用
    :param config: 配置对象
    :return: Flask应用
    """
    the_app = Flask(__name__)
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


@app.route("/")
def index():
    print(app.config['SECRET_KEY'])
    return "hello world"


@app.route("/search/<node_name>", methods=['GET'])
def search(node_name):
    # sub_graph = graph.run(gql).to_subgraph()
    # gql = "match (start_node)-[relationship]-(end_node) where start_node.name = '{}' return start_node,relationship,end_node".format(node_name)
    gql = "match (start_node)-[first_relationship]->(second_node) where start_node.name = '{}' WITH start_node,first_relationship,second_node match (second_node)-[second_relationship]->(third_node) return start_node,first_relationship,second_node,second_relationship,third_node".format(node_name)

    sub_graph = graph.run(gql).data()

    relationship_end = []

    for i in sub_graph:
        print(type(i.get('relationship')).__name__)
        print(i.get('end_node').get('name'))
        start_id_list = [i.get('end_node').get('name'), i.get('end_node').get('id')]
        relationship_end.append({type(i.get('relationship')).__name__: start_id_list})

    json_dict = {
        "start_node": [node_name, sub_graph[0].get('start_node').get('id')],
        "relationship_end": relationship_end,
        # "sub_graph": sub_graph
    }

    return jsonify(json_dict), 200
