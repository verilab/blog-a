import os

from feedgen.feed import FeedGenerator
from flask import render_template, send_file, redirect, jsonify, request

from config import config as C
from util import parse_posts, make_abs_url, parse_posts_page, extension_of_markdown_file, \
    parse_custom_page, get_categories, get_tags, search_content

_mode_api = 'api'
_mode_web_app = 'web-app'
_mode_mixed = 'mixed'

# make it web app mode as default
C.mode = C.get('mode', _mode_web_app)
if C.mode != _mode_api and C.mode != _mode_web_app and C.mode != _mode_mixed:
    raise SyntaxError('Can not recognize mode "%s"' % C.mode)


def should_return_json():
    return C.mode == _mode_api \
           or (C.mode == _mode_mixed
               and ('application/json' in request.headers.get('Accept', '')
                    or request.args.get('format') == 'json'))


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
        if should_return_json():
            return jsonify(dict(ok=True, site=C, page=pg))
        else:
            return render_template('index.html', site=C, page=pg)
    else:
        return page_not_found()


def post(year, month, day, name):
    """
    Render post
    """
    file_name = '-'.join((year, month, day, name))

    ext = extension_of_markdown_file(os.path.join('posts', file_name))
    if ext is None:
        return page_not_found()

    file_name_with_ext = '.'.join((file_name, ext))

    article = parse_posts(f_list=(file_name_with_ext,))[0]
    article['id_key'] = file_name
    article['absolute_url'] = make_abs_url(C.root_url, '/'.join(('post', year, month, day, name)))

    if should_return_json():
        return jsonify(dict(ok=True, site=C, page=article))
    else:
        return render_template(article['layout'] + '.html', site=C, page=article)


def page_not_found():
    """
    Render 404 page
    """
    if should_return_json():
        return jsonify(dict(ok=False))
    else:
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
        'archive_type': 'tag',
        'archive_name': t,
        'entries': parse_posts(tag=t, cut_by_read_more=C.get('support_read_more', False))
    }
    if pg['entries']:
        if should_return_json():
            return jsonify(dict(ok=True, site=C, page=pg))
        else:
            return render_template('tag.html', site=C, page=pg)
    else:
        return page_not_found()


def tags():
    if should_return_json():
        return jsonify(dict(ok=True, data=get_tags()))
    else:
        return page_not_found()


def category(c):
    """
    Render category page
    """
    pg = {
        'archive_type': 'category',
        'archive_name': c,
        'entries': parse_posts(category=c, cut_by_read_more=C.get('support_read_more', False))
    }
    if pg['entries']:
        if should_return_json():
            return jsonify(dict(ok=True, site=C, page=pg))
        else:
            return render_template('category.html', site=C, page=pg)
    else:
        return page_not_found()


def categories():
    if should_return_json():
        return jsonify(dict(ok=True, data=get_categories()))
    else:
        return page_not_found()


def custom_page(rel_path):
    """
    Render custom page
    """
    if '..' in rel_path or './' in rel_path \
            or '/.' in rel_path or rel_path.startswith('.') \
            or '//' in rel_path:
        # the path is not safe
        return page_not_found()

    file_path = os.path.join('pages', rel_path)

    if os.path.exists(file_path) and os.path.isfile(file_path):
        # the exact file exists, so return it
        return send_file(file_path)

    # try different type of file

    # try directory
    if os.path.isdir(file_path):
        # is a directory
        if not file_path.endswith('/'):
            return redirect(rel_path + '/', code=302)
        return custom_page(os.path.join(rel_path, 'index.html'))

    # # try html
    # if os.path.exists(file_path + '.html'):
    #     # html file exists
    #     return send_file(file_path + '.html')

    # try markdown
    # remove "html" extension if accessing this page through "xxx.html"
    file_path = os.path.splitext(file_path)[0]
    md_ext = extension_of_markdown_file(file_path)
    if md_ext is not None:
        # markdown file exists
        content = parse_custom_page('.'.join((file_path, md_ext)))
        content['id_key'] = rel_path
        content['absolute_url'] = make_abs_url(C.root_url, rel_path)
        if should_return_json():
            return jsonify(dict(ok=True, site=C, page=content))
        else:
            return render_template(content['layout'] + '.html', site=C, page=content)

    return page_not_found()


def search():
    """
    Search for something
    """
    query_text = request.args.get('q')
    count_per_page = int(request.args.get('c', C.get('entry_count_one_page_when_search', 20)))
    current_page = int(request.args.get('p', 1))
    if not query_text or query_text == '':
        # invalid query
        return page_not_found()

    print(query_text)
    pg = search_content(query_text, count_per_page, current_page)

    if pg['entries'] or current_page == 1:
        if should_return_json():
            return jsonify(dict(ok=True, site=C, page=pg))
        else:
            return render_template('search.html', site=C, page=pg)
    else:
        return page_not_found()
