import houdini
import os
from urllib.parse import urljoin

import misaka
import yaml
from flask import render_template, request
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name

import config as C


class HighlighterRenderer(misaka.HtmlRenderer):
    def blockcode(self, text, lang):
        if not lang:
            return '\n<pre><code>{}</code></pre>\n'.format(houdini.escape_html(text.strip()))

        lexer = get_lexer_by_name(lang)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)


renderer = HighlighterRenderer()
render_md = misaka.Markdown(renderer,
                            extensions=('fenced-code', 'tables', 'strikethrough', 'underline', 'highlight', 'quote'))


def make_external_url(url):
    return urljoin(request.url_root, url)


def read_md_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as stream:
        content = stream.read().split('\n\n', 1)
    return content


def parse_posts_page(page_id):
    entries = []
    info = {
        'title': C.title,
        'has_newer': False,
        'newer_url': '',
        'has_older': False,
        'older_url': '',
        'entries': []
    }
    f_list = sorted(os.listdir('posts'), reverse=True)
    count = C.max_count
    target_f_list = f_list
    if count > 0:
        start = (page_id - 1) * count
        end = min(page_id * count, len(f_list))
        target_f_list = f_list[start:end]
        if start > 0:
            info['has_newer'] = True
            info['newer_url'] = '/'.join(('/page', str(page_id - 1))) if page_id - 1 != 1 else '/'
        if end < len(f_list):
            info['has_older'] = True
            info['older_url'] = '/'.join(('/page', str(page_id + 1)))
    elif page_id != 1:
        target_f_list = []
    for f in target_f_list:
        file_path = os.path.join('posts', f)
        yml, _ = read_md_file(file_path)
        entry = yaml.load(yml)
        y, m, d, name = os.path.splitext(f)[0].split('-', 3)
        entry['date'] = '-'.join((y, m, d))
        entry['url'] = '/'.join(('/post', y, m, d, name))
        entries.append(entry)
    info['entries'] = entries

    return info


def index():
    return page(1)


def page(page_id):
    info = parse_posts_page(page_id)
    if info['entries'] or page_id == 1:
        return render_template('index.html', info=info)
    else:
        return page_not_found()


def post(year, month, day, post_name):
    print(request.url, request.url_root)
    file_name = '-'.join((year, month, day, post_name)) + '.md'
    file_path = os.path.join('posts', file_name)
    if not os.path.exists(file_path):
        return page_not_found()
    yml, md = read_md_file(file_path)
    article = yaml.load(yml)
    article['body'] = render_md(md)
    article['nav_title'] = ' - '.join((article['title'], C.title))
    article['id_key'] = '-'.join((year, month, day, post_name))
    article['url'] = '/'.join((C.site_url, 'post', year, month, day, post_name))
    return render_template('post.html', article=article)


def page_not_found():
    return render_template('404.html'), 404


def link():
    return render_template('link.html')