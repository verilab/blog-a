#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask

import config as C
import handler

app = Flask(__name__)


@app.route('/')
def index():
    return page(1)


@app.route('/page/<int:page_id>')
def page(page_id):
    return handler.page(page_id)


@app.route('/post/<string:year>/<string:month>/<string:day>/<post_name>')
def post(year, month, day, post_name):
    return handler.post(year, month, day, post_name)


@app.errorhandler(404)
def page_not_found(e):
    return handler.page_not_found()


if __name__ == '__main__':
    app.run(debug=True, host=C.host, port=C.port)
