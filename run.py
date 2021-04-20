from flask import Flask, jsonify, render_template
from flask_cors import CORS
from cart import cart_bp
from input_search import input_search_bp
from click_search import click_search_bp
from py2neo import Graph


def create_flask_app(config):
    """
    创建Flask应用
    :param config: 配置对象
    :return: Flask应用
    """
    the_app = Flask(__name__, template_folder='./template', static_folder='./template/KnowledgeGraph/static')
    CORS(the_app)
    the_app.config.from_object(config)

    # 从环境变量指向的配置文件中读取的配置信息会覆盖掉从配置对象中加载的同名参数
    the_app.config.from_envvar("PROJECT_SETTING", silent=True)
    return the_app


class DefaultConfig(object):
    """默认配置"""
    SECRET_KEY = 'chris!@#$%^&*()'
    # 防止前端中文显示为ASCII
    JSON_AS_ASCII = False


class DevelopmentConfig(DefaultConfig):
    DEBUG = True


class ProductionConfig(DefaultConfig):
    DEBUG = False


# app = create_flask_app(ProductionConfig)
app = create_flask_app(DevelopmentConfig)

# 数据库连接信息保存在current_app中
app.graph = Graph('http://localhost:7474', username='neo4j', password='neo4j')
app.register_blueprint(input_search_bp)
app.register_blueprint(click_search_bp)
app.register_blueprint(cart_bp)


@app.route("/")
def index():
    # print(app.config['SECRET_KEY'])
    # url_dict = {rule.rule: rule.endpoint for rule in app.url_map.iter_rules()}
    # print(url_dict)
    #
    # return jsonify(url_dict)
    return render_template('KnowledgeGraph/index.html')


@app.route("/distinguish")
def distinguish():
    return render_template('KnowledgeGraph/distinguish.html')


app.run('0.0.0.0', 5000)
