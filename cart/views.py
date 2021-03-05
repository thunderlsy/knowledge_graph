#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cart import cart_bp


@cart_bp.route('/info', methods=["GET"])
def cart_info():
    return "cart_info"
