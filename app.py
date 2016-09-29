#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import handler
import generator
import theme

from functools import wraps
from flask import Flask, request, current_app

from config import config as C

app = Flask(__name__)


def support_jsonp(f):
    """
    Wraps JSONified output for JSONP
    https://gist.github.com/richardchien/7b7c2727feb3e8993845a3ce61bad808
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + f(*args, **kwargs).data.decode('utf-8') + ')'
            return current_app.response_class(content, mimetype='application/json')
        else:
            return f(*args, **kwargs)

    return decorated_function


@app.route('/')
@support_jsonp
def index():
    return handler.index()


@app.route('/page/<int:page_id>', strict_slashes=False)
@support_jsonp
def page(page_id):
    return handler.page(page_id)


@app.route('/post/<string:year>/<string:month>/<string:day>/<post_name>', strict_slashes=False)
@support_jsonp
def post(year, month, day, post_name):
    return handler.post(year, month, day, post_name)


@app.route('/feed', strict_slashes=False)
@app.route('/feed.xml')
@app.route('/atom.xml')
def feed():
    return handler.feed()


@app.route('/category/<string:c>', strict_slashes=False)
@support_jsonp
def category(c):
    return handler.category(c)


@app.route('/categories', strict_slashes=True)
@support_jsonp
def categories():
    return handler.categories()


@app.route('/tag/<string:t>', strict_slashes=False)
@support_jsonp
def tag(t):
    return handler.tag(t)


@app.route('/tags', strict_slashes=True)
@support_jsonp
def tags():
    return handler.tags()


@app.route('/search', strict_slashes=True)
@support_jsonp
def search():
    return handler.search()


if C.get('webhook_enable', False):
    @app.route('/_webhook', strict_slashes=True, methods=['POST'])
    def webhook():
        try:
            from custom import webhook_handler as h
            if h.handle:
                h.handle(request.json or request.form)
        except ImportError:
            print('There is no webhook handler.')
        return '', 204


@app.route('/<path:custom_page_path>', strict_slashes=True)
@support_jsonp
def custom_page(custom_page_path):
    return handler.custom_page(custom_page_path)


@app.errorhandler(404)
@support_jsonp
def page_not_found(e):
    return handler.page_not_found()


@app.after_request
def allow_access(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            print('Unknown arguments.')
        elif sys.argv[1] == 'generate':
            with app.app_context() and app.test_request_context(''):
                generator.generate_static_site()
        elif sys.argv[1] == 'setup-github-pages':
            generator.setup_github_pages()
        elif sys.argv[1] == 'deploy':
            generator.deploy()
        elif sys.argv[1] == 'clean':
            generator.clean()
        elif sys.argv[1] == 'apply-theme':
            theme.apply_theme(C.theme)
        else:
            print('Unknown arguments.')
    else:
        app.run(debug=False, host=C.host, port=C.port)
