import os
import shutil
import handler
import util

from config import config as C

_deploy_dir = '_deploy'

_post_page_count = 0
_post_file_names = []
_tags = set()
_categories = set()


def init():
    global _post_page_count
    global _post_file_names
    global _tags
    global _categories

    # remove old static files
    if os.path.exists(_deploy_dir):
        shutil.rmtree(_deploy_dir)
    os.mkdir(_deploy_dir)

    file_list = util.get_posts_list()

    # get post count
    if C.entry_count_one_page == 0:
        _post_page_count = 1
    else:
        _post_page_count = len(file_list) // C.entry_count_one_page + 1

    for file in file_list:
        # get post file names
        _post_file_names.append(os.path.splitext(file)[0])

        # get tags and categories
        file_path = os.path.join('posts', file)
        d = util.render_yaml(util.read_md_file_head(file_path))
        if 'categories' in d:
            _categories |= set(util.to_list(d['categories']))
        if 'tags' in d:
            _tags |= set(util.to_list(d['tags']))


def generate_index():
    with open(os.path.join(_deploy_dir, 'index.html'), 'w') as f:
        f.write(handler.index())


def generate_post_pages():
    for i in range(1, _post_page_count + 1):
        post_page_dir = os.path.join(_deploy_dir, 'page', str(i))
        os.makedirs(post_page_dir)
        with open(os.path.join(post_page_dir, 'index.html'), 'w') as f:
            f.write(handler.page(i))


def generate_tag_pages():
    for t in _tags:
        tag_page_dir = os.path.join(_deploy_dir, 'tag', t)
        os.makedirs(tag_page_dir)
        with open(os.path.join(tag_page_dir, 'index.html'), 'w') as f:
            f.write(handler.tag(t))


def generate_category_pages():
    for c in _categories:
        category_page_dir = os.path.join(_deploy_dir, 'category', c)
        os.makedirs(category_page_dir)
        with open(os.path.join(category_page_dir, 'index.html'), 'w') as f:
            f.write(handler.category(c))


def generate_posts():
    for file in _post_file_names:
        y, m, d, name = file.split('-', 3)
        post_dir = os.path.join(_deploy_dir, 'post', y, m, d, name)
        os.makedirs(post_dir)
        with open(os.path.join(post_dir, 'index.html'), 'w') as f:
            f.write(handler.post(y, m, d, name))


def generate_404():
    with open(os.path.join(_deploy_dir, '404.html'), 'w') as f:
        f.write(handler.page_not_found()[0])


def generate_static():
    shutil.copytree('static', os.path.join(_deploy_dir, 'static'))


def search_file(s, d):
    result = []
    for p in os.listdir(d):
        if os.path.isdir(os.path.join(d, p)):
            result += search_file(s, os.path.join(d, p))
        else:
            name = os.path.split(p)[1]
            if s in name:
                result.append(os.path.join(os.path.abspath(d), p))
    return result


def fix_links():
    for file_path in search_file('.html', _deploy_dir):
        dir = ''

        temp_path = file_path
        deploy_abspath = os.path.abspath(_deploy_dir)
        if os.path.dirname(file_path) != deploy_abspath:
            temp_path = os.path.split(temp_path)[0]
            while temp_path != deploy_abspath:
                temp_path = os.path.split(temp_path)[0]
                dir = os.path.join('..', dir)

        if dir == '':
            dir = './'

        lines = []
        with open(file_path, 'r') as f:
            for line in f:
                lines.append(line.replace('href="/feed', 'href="/feed.xml')
                             .replace('href="/', 'href="' + dir)
                             .replace('src="/', 'src="' + dir))

        with open(file_path, 'w') as f:
            f.writelines(lines)


def generate_feed():
    with open(os.path.join(_deploy_dir, 'feed.xml'), 'wb') as f:
        f.write(handler.feed())


def generate_static_site():
    print('Initiating...', end='')
    init()
    print('OK')
    print('Generating index...', end='')
    generate_index()
    print('OK')
    print('Generating post pages...', end='')
    generate_post_pages()
    print('OK')
    print('Generating tag pages...', end='')
    generate_tag_pages()
    print('OK')
    print('Generating category pages...', end='')
    generate_category_pages()
    print('OK')
    print('Generating posts...', end='')
    generate_posts()
    print('OK')
    print('Generating 404...', end='')
    generate_404()
    print('OK')
    print('Generating static files...', end='')
    generate_static()
    print('OK')
    print('Fixing links...', end='')
    fix_links()
    print('OK')
    print('Generating feed...', end='')
    generate_feed()
    print('OK')
