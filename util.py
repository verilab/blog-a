import os
import re
import shutil
import misaka
import houdini
import yaml

from datetime import datetime, timezone, timedelta, date
from urllib.parse import urljoin
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from config import config as C


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
                    'footnotes',
                    'autolink',
                    'strikethrough',
                    'underline',
                    'highlight',
                    'quote',
                    'superscript')
    )(md_str)


# regex to match the post file with correct format
post_file_regex = re.compile(
    r'(\d{4}|\d{2})-((1[0-2])|(0?[1-9]))-(([12][0-9])|(3[01])|(0?[1-9]))-[\w-]+\.(md|MD|markdown|mdown)'
)

# regex to match the "<!--more-->" (aka "Read More") flag in md file
more_flag_regex = re.compile(
    r'<!--\s*more\s*-->'
)


def get_posts_list():
    """
    Get list of all post files, whose name match the format "yyyy-m(m)-d(d)-text.m(ark)d(own)"

    :return: list of all post files
    """
    file_list = []
    for file in sorted(os.listdir('posts'), reverse=True):
        if post_file_regex.match(file):
            file_list.append(file)
    return file_list


def default_post_info(file):
    """
    Get default post info from post file name

    :param file: post file name with extension
    :return: default post info (a dict)
    """
    y, m, d, file_name = os.path.splitext(file)[0].split('-', 3)
    # set default post info
    entry = {
        'layout': 'post',
        'author': C.author,
        'email': C.email,
        # default date, title, url from file name
        'date': datetime(int(y), int(m), int(d)),
        'title': ' '.join(map(lambda w: w.capitalize(), file_name.split('-'))),
        'url': '/'.join(('/post', y, m, d, file_name))
    }
    return entry


def parse_posts(start=0, count=0, f_list=None, tag=None, category=None, cut_by_read_more=False):
    """
    Parse posts in the "posts" directory

    :param start: the first post id
    :param count: number of posts to parse (0 for all)
    :param f_list: specific file list
    :param tag: specific tag
    :param category: specific category
    :param cut_by_read_more: should cut md file by "Read More" flag
    :return: list of parsed post (a list of dict)
    """
    if not f_list:
        # count can't be less than 0
        if count < 0:
            raise ValueError('The number of posts to parse cannot be less than 0.')

        # filter the file list
        file_list = get_posts_list()
        if count > 0:
            end = start + min(count, len(file_list))  # using min() in case of over bound
            file_list = file_list[start:end]
    else:
        # parse specific file list
        file_list = f_list

    # filter tag and category
    new_file_list = []
    if tag is not None or category is not None:
        for file in file_list:
            file_path = os.path.join('posts', file)
            yml_dict = render_yaml(read_md_file_head(file_path))

            if yml_dict:
                # make sure that the tags and categories are lists
                if 'categories' in yml_dict:
                    yml_dict['categories'] = to_list(yml_dict['categories'])
                if 'tags' in yml_dict:
                    yml_dict['tags'] = to_list(yml_dict['tags'])

                if ('tags' in yml_dict and tag in yml_dict['tags']) or \
                        ('categories' in yml_dict and category in yml_dict['categories']):
                    new_file_list.append(file)

        file_list = new_file_list

    entries = []
    for file in file_list:
        entry = default_post_info(file)

        file_path = os.path.join('posts', file)
        yml, md = read_md_file(file_path)

        # get more detailed post info from yaml head
        post_info = render_yaml(yml)
        if post_info:
            for k, v in post_info.items():
                entry[k] = v

        # fix datetime wrongly being a date object or has no tzinfo
        if 'date' in entry:
            entry['date'] = fix_datetime(entry['date'])
        if 'updated' in entry:
            entry['updated'] = fix_datetime(entry['updated'])

        # fix categories and tags
        if 'categories' in entry:
            entry['categories'] = to_list(entry['categories'])
        if 'tags' in entry:
            entry['tags'] = to_list(entry['tags'])

        # render markdown body to html
        entry['read_more'] = cut_by_read_more  # default set to cut_by_read_more
        if cut_by_read_more:
            # find the "Read More" flag position and cut it
            indices = [x.start(0) for x in more_flag_regex.finditer(md)]
            if indices:
                md = md[:indices[0]]
            else:
                # didn't cut
                entry['read_more'] = False
        entry['body'] = render_md(md)

        entries.append(entry)

    return entries


def parse_posts_page(page_id):
    """
    Parse posts on the page with page_id

    :param page_id: id of page to parse
    :return: a info dict to be sent to templates
    """
    pg = {
        'has_newer': False,
        'newer_url': '',
        'has_older': False,
        'older_url': '',
        'entries': []
    }

    count = C.entry_count_one_page
    file_list = get_posts_list()

    if count == 0 and page_id != 1:
        # should show all posts but not on page 1, then show nothing
        return pg

    # show specific number of posts or all (only on page 1)
    start = (page_id - 1) * count
    end = min(page_id * count, len(file_list))

    # determine there are newer or older posts
    if start > 0:
        pg['has_newer'] = True
        pg['newer_url'] = '/'.join(('/page', str(page_id - 1))) if page_id - 1 != 1 else '/'
    if end < len(file_list) and end != 0:
        pg['has_older'] = True
        pg['older_url'] = '/'.join(('/page', str(page_id + 1)))

    pg['entries'] = parse_posts(start, count, cut_by_read_more=C.get('support_read_more', False))

    return pg


def default_custom_page_info(file):
    """
    Get default custom page info from markdown filename

    :param file: page markdown file name with extension
    :return: default page info (a dict)
    """
    filename = os.path.splitext(file)[0]

    # set default post info
    entry = {
        'layout': 'page',
        'author': C.author,
        'email': C.email,
        # default title, url from file name
        'title': ' '.join(map(lambda w: w.capitalize(), filename.split('-')))
    }
    return entry


def parse_custom_page(file_path):
    """
    Parse custom page in markdown

    :param file_path: markdown file path
    :return: parsed custom page (a dict)
    """
    page = default_custom_page_info(os.path.basename(file_path))

    yml, md = read_md_file(file_path)

    # get more detailed page info from yaml head
    page_info = render_yaml(yml)
    if page_info:
        for k, v in page_info.items():
            page[k] = v

    # render markdown body to html
    page['body'] = render_md(md)

    return page


def timezone_from_str(tz_str):
    """
    Convert a timezone string to a timezone object

    :param tz_str: string with format 'UTC±[hh]:[mm]'
    :return: a timezone object
    """
    m = re.match(r'UTC([+|-]\d{1,2}):(\d{2})', tz_str)
    delta_h = int(m.group(1))
    delta_m = int(m.group(2)) if delta_h >= 0 else -int(m.group(2))
    return timezone(timedelta(hours=delta_h, minutes=delta_m))


def fix_datetime(dt):
    """
    Fix a datetime (supposed to be)

    :param dt: datetime to fix
    :return: correct datetime object
    """
    if isinstance(dt, date):
        dt = datetime(dt.year, dt.month, dt.day)
    if dt is not None and dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone_from_str(C.timezone))
    return dt


def to_list(item):
    """
    Make a list contains item if item is not a list

    :param item: item to convert
    :return: a list
    """
    if item is not None and not isinstance(item, list):
        return [item]
    return item


def extension_of_markdown_file(file_path_without_ext):
    """
    Find markdown file with the specific file path

    :param file_path_without_ext: file path without extension
    :return: file extension
    """
    if os.path.exists(file_path_without_ext + '.md') is not False:
        return 'md'
    elif os.path.exists(file_path_without_ext + '.MD') is not False:
        return 'MD'
    elif os.path.exists(file_path_without_ext + '.mdown') is not False:
        return 'mdown'
    elif os.path.exists(file_path_without_ext + '.markdown') is not False:
        return 'markdown'
    else:
        return None


def get_labels_of_posts(label_type):
    """
    Get labels (tags or categories) of all posts

    :param label_type: 'tags' or 'categories'
    :return: list of labels with post count
    """
    file_list = get_posts_list()
    count_dict = {}
    for file in file_list:
        file_path = os.path.join('posts', file)
        yml_dict = render_yaml(read_md_file_head(file_path))
        if yml_dict:
            labels = to_list(yml_dict[label_type])
            for label in labels:
                count_dict[label] = count_dict.get(label, 0) + 1
    result = []
    for key in count_dict.keys():
        result.append(dict(name=key, count=count_dict[key]))
    return result


def get_categories():
    """
    Get all categories

    :return: list of categories with post count
    """
    return get_labels_of_posts('categories')


def get_tags():
    """
    Get all tags

    :return: list of tags with post count
    """
    return get_labels_of_posts('tags')


def copytree(src, dst, symlinks=False, ignore=None):
    """
    Correctly copy an entire directory

    :param src: source dir
    :param dst: destination dir
    :param symlinks: copy content of symlinks
    :param ignore: ignore
    """
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def search_content(query_text, count_per_page, current_page):
    """
    Search for posts and pages which contain query_text

    :param query_text: text to query
    :return: list of entries
    """
    pg = {
        'query': query_text,
        'entries': [],
        'has_next': False,
        'next_url': '',
        'has_prev': False,
        'prev_url': ''
    }
    entries = []

    def append_if_needed(entry, yml, md, type):
        is_result = False

        # get more detailed info from yaml head
        info = render_yaml(yml)
        if info:
            for k, v in info.items():
                entry[k] = v

        if query_text.lower() in entry['title'].lower():
            # title contains query text
            is_result = True
        elif query_text.lower() in md.lower():
            # markdown body contains query text
            is_result = True

        if is_result:
            # fix datetime wrongly being a date object or has no tzinfo
            if 'date' in entry:
                entry['date'] = fix_datetime(entry['date'])
            if 'updated' in entry:
                entry['updated'] = fix_datetime(entry['updated'])

            # fix categories and tags
            if 'categories' in entry:
                entry['categories'] = to_list(entry['categories'])
            if 'tags' in entry:
                entry['tags'] = to_list(entry['tags'])

            entry['type'] = type
            entries.append(entry)

    # search for posts

    post_files = get_posts_list()

    for file in post_files:
        entry = default_post_info(file)
        yml, md = read_md_file(os.path.join('posts', file))
        append_if_needed(entry, yml, md, 'post')

    # search for custom pages

    def list_dir(dir):
        results = []
        for f in os.listdir(dir):
            full_rel_path = os.path.join(dir, f)
            if os.path.isdir(full_rel_path):
                results += list_dir(full_rel_path)
            elif f.endswith('.md') or f.endswith('.MD') or f.endswith('.markdown') or f.endswith('.mdown'):
                results.append(full_rel_path)
        return results

    custom_page_file_paths = list_dir('pages')
    for file_path in custom_page_file_paths:
        entry = default_custom_page_info(os.path.basename(file_path))
        split_path = os.path.splitext(file_path)[0].split(os.sep)[1:]
        if split_path[len(split_path) - 1] == 'index':
            split_path[len(split_path) - 1] = ''
        entry['url'] = '/' + '/'.join(split_path)
        yml, md = read_md_file(file_path)
        append_if_needed(entry, yml, md, 'page')

    total_count = len(entries)
    start = count_per_page * (current_page - 1)
    end = min(count_per_page * current_page, total_count)
    if start < 0 or start >= total_count or end > total_count or end <= 0:
        pg['entries'] = None
    else:
        pg['entries'] = entries[start:end]

    if start > 0:
        pg['has_prev'] = True
        pg['prev_url'] = '/search?q=%s&c=%s&p=%s' % (query_text, count_per_page, current_page - 1)
    if end < total_count:
        pg['has_next'] = True
        pg['next_url'] = '/search?q=%s&c=%s&p=%s' % (query_text, count_per_page, current_page + 1)
    return pg
