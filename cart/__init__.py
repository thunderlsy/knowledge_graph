#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")

from cart.views import *
