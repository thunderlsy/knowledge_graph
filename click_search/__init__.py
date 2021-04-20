#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint

click_search_bp = Blueprint("click_search", __name__, url_prefix="/click_search")

from click_search.views import *
