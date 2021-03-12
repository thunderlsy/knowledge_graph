#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cart import cart_bp
from flask_restful import Resource, Api
from flask_restful.representations import json

cart_api = Api(cart_bp)


# 通用装饰器
def logging1(func):
    print("logging_1装饰器外部")

    def inner(*args, **kwargs):
        print("logging_1装饰器内部")
        return func(*args, **kwargs)

    return inner


# 通用装饰器
def logging2(func):
    print("logging_2装饰器外部")

    def inner(*args, **kwargs):
        print("logging_2装饰器内部")
        return func(*args, **kwargs)

    return inner


@cart_bp.route('/info', methods=["GET"])
def cart_info():
    return "cart_info"
    # return jsonify("cart_info")


# 2.2 定义类视图
class UserResource1(Resource):

    def get(self):
        return "get user"

    def post(self):
        return "post user"


# 可以添加多个类视图
class UserResource2(Resource):
    method_decorators = {
        'get': [logging1, logging2],
        'post': [logging2]
    }

    def get(self):
        return "get user"

    def post(self):
        return "post user"


cart_api.add_resource(UserResource1, '/info1', endpoint="cart_route1")
cart_api.add_resource(UserResource2, '/info2', endpoint="cart_route2")
