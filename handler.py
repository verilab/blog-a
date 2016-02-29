from feedgen.feed import FeedGenerator
from flask import render_template, request

from util import *

import config as C


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
    article['nav_title'] = ' - '.join((article['title'], C.site_title))
    article['id_key'] = '-'.join((year, month, day, post_name))
    article['absolute_url'] = 'http://' + '/'.join((C.site_url, 'post', year, month, day, post_name))
    return render_template('post.html', article=article)


def page_not_found():
    return render_template('404.html'), 404


def link():
    return render_template('link.html')


def feed():
    f_list = sorted(os.listdir('posts'), reverse=True)

    fg = FeedGenerator()
    fg.id(str(len(f_list)))
    fg.title("RC's Blog")
    fg.author(dict(name='Richard Chien', email='richardchienthebest@gmail.com'))
    fg.link(href=C.site_url, rel='alternate')
    fg.subtitle("Feed of RC's Blog")
    fg.link(href=C.site_url + '/feed', rel='self')
    fg.language('zh')

    entries = parse_posts_page(1, count=min(10, len(f_list)))['entries']
    for entry in entries:
        fe = fg.add_entry()
        fe.id(entry['url'])
        fe.title(entry['title'])
        fe.link(href=C.site_url + entry['url'], rel='alternate')
        fe.author(dict(name='Richard Chien', email='richardchienthebest@gmail.com'))
        fe.content(entry['body'])

    atom_feed = fg.atom_str(pretty=True)
    return atom_feed
