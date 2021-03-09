#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint
# from flask_restful import Resource, Api
from py2neo import Graph

graph = Graph('http://localhost:7474', username='neo4j', password='neo4j')
search_bp = Blueprint("search", __name__, url_prefix="/search")
# search_api = Api(search_bp)

from search.views import *
