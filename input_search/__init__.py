#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint

search_bp = Blueprint("input_search", __name__, url_prefix="/input_search")

from input_search.views import *
