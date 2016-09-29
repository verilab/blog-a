import os
import re
import shutil
import handler
import util

from datetime import datetime

from config import config as C

_deploy_dir = '_deploy'

_post_page_count = 0
_post_file_names = []
_tags = set()
_categories = set()


def init():
    """
    Clear old files and iterate posts and collect basic info
    """
    global _post_page_count
    global _post_file_names
    global _tags
    global _categories

    # remove old static files
    if os.path.exists(_deploy_dir):
        for file in os.listdir(_deploy_dir):
            if file.startswith('.'):
                continue
            path = os.path.join(_deploy_dir, file)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    else:
        os.mkdir(_deploy_dir)

    file_list = util.get_posts_list()

    # get post count
    if C.entry_count_one_page == 0:
        _post_page_count = 1
    else:
        total = len(file_list)
        _post_page_count = total // C.entry_count_one_page \
                           + (1 if total % C.entry_count_one_page != 0 else 0)

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
    """
    Generate index page
    """
    with open(os.path.join(_deploy_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(handler.index())


def generate_post_pages():
    """
    Generate "/page/<int>" pages
    """
    for i in range(1, _post_page_count + 1):
        post_page_dir = os.path.join(_deploy_dir, 'page', str(i))
        os.makedirs(post_page_dir)
        with open(os.path.join(post_page_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(handler.page(i))


def generate_tag_pages():
    """
    Generate "/tag/<string>" pages
    """
    for t in _tags:
        tag_page_dir = os.path.join(_deploy_dir, 'tag', t)
        os.makedirs(tag_page_dir)
        with open(os.path.join(tag_page_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(handler.tag(t))


def generate_category_pages():
    """
    Generate "/category/<string>" pages
    """
    for c in _categories:
        category_page_dir = os.path.join(_deploy_dir, 'category', c)
        os.makedirs(category_page_dir)
        with open(os.path.join(category_page_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(handler.category(c))


def generate_posts():
    """
    Generate post pages
    """
    for file in _post_file_names:
        y, m, d, name = file.split('-', 3)
        post_dir = os.path.join(_deploy_dir, 'post', y, m, d, name)
        os.makedirs(post_dir)
        with open(os.path.join(post_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(handler.post(y, m, d, name))


def generate_custom_pages(rel_dir_path='.'):
    """
    Generate custom pages
    """
    dir_path = os.path.join('pages', rel_dir_path)
    os.makedirs(os.path.join(_deploy_dir, rel_dir_path), exist_ok=True)
    for file in os.listdir(dir_path):
        if file.startswith('.'):
            # is hidden file
            continue

        if os.path.isdir(os.path.join(dir_path, file)):
            generate_custom_pages(os.path.join(rel_dir_path, file))
            continue

        rel_file_path = os.path.join(rel_dir_path, file)
        filename, ext = os.path.splitext(rel_file_path)
        if ext == '.md' or ext == '.markdown':
            # is markdown file, need render
            rel_file_path = '.'.join((filename, 'html'))
            with open(os.path.join(_deploy_dir, rel_file_path), 'w', encoding='utf-8') as f:
                f.write(
                    handler.custom_page('/'.join(os.path.split(rel_file_path)).replace('./', '')))
        else:
            # is common static file, just copy
            shutil.copy(os.path.join('pages', rel_file_path),
                        os.path.join(_deploy_dir, rel_file_path))


def generate_404():
    """
    Generate 404 page
    """
    with open(os.path.join(_deploy_dir, '404.html'), 'w', encoding='utf-8') as f:
        f.write(handler.page_not_found()[0])


def generate_static():
    """
    Generate CSS and JavaScript files
    """
    util.copytree('static', os.path.join(_deploy_dir, 'static'))


def search_file(s, d):
    """
    Search for file recursively
    :param s: key word
    :param d: directory to search in
    :return: list of absolute file paths
    """
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
    """
    Fix relative paths in links in HTML files
    """
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
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                lines.append(line.replace('href="/', 'href="' + dir)
                             .replace('src="/', 'src="' + dir))

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)


def generate_feed():
    """
    Generate feed.xml
    """
    with open(os.path.join(_deploy_dir, 'feed.xml'), 'wb') as f:
        f.write(handler.feed())


def generate_static_site():
    """
    Generate whole static site
    """
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
    print('Generating custom pages...', end='')
    generate_custom_pages()
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


def setup_github_pages():
    """
    Setup git repository for GitHub Pages
    """
    print('Enter the url of your repository')
    print("(For example, 'git@github.com:your_username/your_username.github.io.git)")
    print("           or 'https://github.com/your_username/your_username.github.io')")
    repo_url = input('Repository url: ')
    while not re.match(
            r'(?:https://github\.com/|git@github\.com:)([\w-]+)/\1\.github\.(io|com)\.git',
            repo_url):
        print('The repository url you entered is invalid, please check your input.')
        repo_url = input('Repository url: ')

    if not os.path.exists(_deploy_dir):
        os.mkdir(_deploy_dir)

    os.chdir(_deploy_dir)

    os.system('git init')

    print('Enter your email and name')
    email = input('Email: ')
    name = input('Name: ')
    os.system('git config user.email "%s"' % email)
    os.system('git config user.name "%s"' % name)
    os.system('git remote add origin %s' % repo_url)

    os.chdir('../')
    print('Setup succeeded.')


def clean():
    """
    Remove the "_deploy" directory
    """
    print('Cleaning...', end='')
    shutil.rmtree(_deploy_dir)
    print('OK')


def deploy():
    """
    Push all changes in "_deploy" to remote repository
    """
    os.chdir(_deploy_dir)

    os.system('git add .')

    if os.system('git diff --quiet --exit-code') == 0 \
            and os.system('git diff --quiet --cached --exit-code') == 0:
        print('There is no changes to be deployed.')
        return

    os.system('git commit -m "Updated on %s"' % datetime.now().strftime('%y-%m-%d %H:%M:%S'))
    if os.system('git push origin master') != 0:
        print('Deploy failed.')
        return

    os.chdir('../')
    print('Deploy succeeded.')
