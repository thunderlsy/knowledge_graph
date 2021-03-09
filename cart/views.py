#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cart import cart_bp
from flask_restful import Resource, Api


@cart_bp.route('/info', methods=["GET"])
def cart_info():
    return "cart_info"


# 2.2 定义类视图
class UserResource1(Resource):

    def get(self):
        return "get user"

    def post(self):
        return "post user"


# 可以添加多个类视图
class UserResource2(Resource):

    def get(self):
        return "get user"

    def post(self):
        return "post user"


cart_api = Api(cart_bp)
cart_api.add_resource(UserResource1, '/info1', endpoint="cart_route1")
cart_api.add_resource(UserResource2, '/info2', endpoint="cart_route2")
