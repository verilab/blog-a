import os
import re
import misaka
import houdini
import yaml

import config as C

from datetime import datetime
from urllib.parse import urljoin
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name


class HighlighterRenderer(misaka.HtmlRenderer):
    def blockcode(self, text, lang):
        if not lang:
            return '\n<pre><code>{}</code></pre>\n'.format(houdini.escape_html(text.strip()))

        lexer = get_lexer_by_name(lang)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)


renderer = HighlighterRenderer()


def make_abs_url(root_url, rel_url):
    """
    Make an absolute URL from a relative URL

    :param root_url: root URL
    :param rel_url: relative URL
    :return: absolute URL
    """
    return urljoin(root_url, rel_url)


def read_md_file(file_path, split=True):
    """
    Read full content of a markdown file

    :param file_path: path of file
    :param split: split head and body ot not
    :return: a tuple with 2 elements - yaml head and markdown body, or a string of whole file if split is True
    """
    with open(file_path, 'r', encoding='utf-8') as stream:
        content = stream.read().split('\n\n', 1) if split else stream.read()
    return content


def read_md_file_head(file_path):
    """
    Read the yaml head of a markdown file

    :param file_path: path of file
    :return: the yaml head
    """
    with open(file_path, 'r', encoding='utf-8') as stream:
        last_line = None
        line = None
        head = ''
        while not (line == last_line and line == '\n'):
            line = stream.readline()
            head += line
            last_line = line
    return head


def read_md_file_body(file_path):
    """
    Read the markdown body of a markdown file

    :param file_path: path of file
    :return: the markdown body
    """
    return read_md_file(file_path, split=True)[1]


def render_yaml(yaml_str):
    """
    Render a yaml string

    :param yaml_str: yaml string to render
    :return: a dict
    """
    return yaml.load(yaml_str)


def render_md(md_str):
    """
    Render a markdown string

    :param md_str: markdown string to render
    :return: html text
    """
    return misaka.Markdown(
        renderer,
        extensions=('fenced-code',
                    'tables',
                    'strikethrough',
                    'underline',
                    'highlight',
                    'quote')
    )(md_str)


def get_posts_list():
    """
    Get list of all post files, whose name match the format "yyyy-m(m)-d(d)-text.m(ark)d(own)"

    :return: list of all post files
    """
    file_list = []
    reg = re.compile(r'(\d{4}|\d{2})-((1[0-2])|(0?[1-9]))-(([12][0-9])|(3[01])|(0?[1-9]))-[\w-]+\.(md|markdown)')
    for file in sorted(os.listdir('posts'), reverse=True):
        if reg.match(file):
            file_list.append(file)
    return file_list


def parse_posts(start=0, count=0):
    """
    Parse posts in the "posts" directory

    :param start: the first post id
    :param count: number of posts to parse (0 for all)
    :return: list of parsed post (a list of dict)
    """
    # count can't be less than 0
    if count < 0:
        raise ValueError('The number of posts to parse cannot be less than 0.')

    # filter the file list
    file_list = get_posts_list()
    if count > 0:
        end = start + min(count, len(file_list))  # using min() in case of over bound
        print(len(file_list))
        file_list = file_list[start:end]

    entries = []
    for file in file_list:
        y, m, d, file_name = os.path.splitext(file)[0].split('-', 3)

        # set default post info
        entry = {
            'layout': 'post',
            'published': True,
            'categories': [],
            'tags': [],
            'date': datetime(int(y), int(m), int(d)),
            'title': ' '.join(map(lambda w: w.capitalize(), file_name.split('-'))),
            'url': '/'.join(('/post', y, m, d, file_name))
        }

        file_path = os.path.join('posts', file)
        yml, md = read_md_file(file_path)

        # get more detailed post info from yaml head
        post_info = render_yaml(yml)
        for k, v in post_info.items():
            entry[k] = v

        # render markdown body to html
        entry['body'] = render_md(md)

        if entry['published']:
            entries.append(entry)

    return entries


def parse_posts_page(page_id):
    """
    Parse posts on the page with page_id

    :param page_id: id of page to parse
    :return: a info dict to be sent to templates
    """
    info = {
        'site_title': C.site_title,
        'has_newer': False,
        'newer_url': '',
        'has_older': False,
        'older_url': '',
        'entries': []
    }

    count = C.entry_count_one_page
    file_list = sorted(os.listdir('posts'), reverse=True)
    if count > 0 or (count == 0 and page_id == 1):
        start = (page_id - 1) * count
        end = min(page_id * count, len(file_list))

        if start > 0:
            info['has_newer'] = True
            info['newer_url'] = '/'.join(('/page', str(page_id - 1))) if page_id - 1 != 1 else '/'
        if end < len(file_list):
            info['has_older'] = True
            info['older_url'] = '/'.join(('/page', str(page_id + 1)))

        info['entries'] = parse_posts(start, count)

    return info
