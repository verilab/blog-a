import os

from feedgen.feed import FeedGenerator
from flask import render_template
from util import parse_posts, make_abs_url, parse_posts_page

from config import config as C


def index():
    """
    Render index page
    """
    return page(1)


def page(page_id):
    """
    Render posts page ('/page/<int:page_id>')
    """
    pg = parse_posts_page(page_id)
    if pg['entries'] or page_id == 1:
        return render_template('index.html', site=C, page=pg)
    else:
        return page_not_found()


def post(year, month, day, name):
    """
    Render post
    """
    file_name = '-'.join((year, month, day, name))

    file_name_with_ext = file_name
    if os.path.exists(file_name + '.md') is not None:
        file_name_with_ext += '.md'
    elif os.path.exists(file_name + '.markdown') is not None:
        file_name_with_ext += '.markdown'
    else:
        return page_not_found()

    article = parse_posts(f_list=(file_name_with_ext,))[0]
    article['id_key'] = file_name
    article['absolute_url'] = make_abs_url(C.root_url, '/'.join(('post', year, month, day, name)))

    return render_template('post.html', site=C, page=article)


def page_not_found():
    """
    Render 404 page
    """
    return render_template('404.html', site=C), 404


def feed():
    """
    Generate atom feed
    """
    entries = parse_posts(0, C.feed_count)
    fg = FeedGenerator()
    fg.id(str(len(entries)))
    fg.title(C.title)
    fg.subtitle(C.subtitle)
    fg.language(C.language)
    fg.author(dict(name=C.author, email=C.email))
    fg.link(href=C.root_url, rel='alternate')
    fg.link(href=make_abs_url(C.root_url, 'feed'), rel='self')
    for entry in entries:
        fe = fg.add_entry()
        fe.id(entry.get('url'))
        fe.title(entry.get('title'))
        fe.published(entry.get('date'))
        fe.updated(entry.get('updated') or entry.get('date'))
        fe.link(href=make_abs_url(C.root_url, entry.get('url')), rel='alternate')
        fe.author(dict(name=entry.get('author'), email=entry.get('email')))
        fe.content(entry.get('body'))

    atom_feed = fg.atom_str(pretty=True)
    return atom_feed


def tag(t):
    """
    Render tag page
    """
    pg = {
        'tag': t,
        'entries': parse_posts(tag=t)
    }
    if pg['entries']:
        return render_template('tag.html', site=C, page=pg)
    else:
        return page_not_found()


def category(c):
    """
    Render category page
    """
    pg = {
        'category': c,
        'entries': parse_posts(category=c)
    }
    if pg['entries']:
        return render_template('category.html', site=C, page=pg)
    else:
        return page_not_found()
