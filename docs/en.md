# BlogA

![License](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)
[![Build Status](https://travis-ci.org/BlogTANG/blog-a.svg?branch=master)](https://travis-ci.org/BlogTANG/blog-a)

This is a simple blog app based on Flask, requiring Python 3.x (you may need to use `python3` instead of `python` in all commands below). Demo: [https://blogtang.github.io/blog-a-demo/](https://blogtang.github.io/blog-a-demo/).

## Get Started

### Install Python modules

```py
pip install -r requirements.txt
```

### Configuration

Configure the blog site in `config.py`.

### Add posts

Posts should be written in Markdown and placed in `posts` directory. Names of post files are supposed to be in format `yyyy-MM-dd-post-name.md` or `yyyy-MM-dd-post-name.markdown`, for example, `2016-03-02-my-first-post.md`.

Extra properties of a post could be placed at the beginning of the markdown file, using the YAML language. The properties which can be identified by the default template are listed below:

```yaml
title: My Post Title (derived from post file name by default, for example, default title of "2016-03-02-my-first-post.md" is "My First Post")
layout: post (default value is "post" and the app will look for "layout-name.html" in "templates" directory)
url: (default value is "root_url/year/month/day/title")
categories: [category1, category2] (default value is none)
tags: [tag1, tag2, tag3] (default value is none)
date: YYYY-MM-DD HH:MM:SS (derived from post file name by default)
updated: YYYY-MM-DD HH:MM:SS (default value is none)
author: Richard Chien (default value is the author in config.py)
email: richardchienthebest@gmail.com (default value is the email in config.py)
```

`\n\n` is used to separate YAML and Markdown parts, like:

```
title: My Post Title
tags: [tag1, tag2]
date: 2016-03-02 20:48

## Title
This is my first post.
```

If need to use "Read More" button and article preview on homepage, you can add a `<!-- more -->` flag at a proper position in the Markdown file. If one of this flag is found, content before the flag will be cut as the preview of the article, else the full content of the article will be previewed. You can turn on or off this function in `config.py` by setting the `support_read_more`. (This function is on the premise of your template supporting the "Read More" function)

### Add custom pages

Add Markdown or HTML files in `pages` directory (or in its subdirectory), for example `readme.md` or `readme/index.md` or `readme/index.html`, then you can access the custom page through `/readme.html` or `/readme/` separately.

If Markdown is being used, the file should be just like those as posts, for example:

```
title: About
layout: page (default value is "page" and the app will look for "layout-name.html" in "templates" directory)
author: Richard Chien (default value is the author in config.py)
email: richardchienthebest@gmail.com (default value is the email in config.py)

This is an about page.
```

If HTML is being used, then the raw content of the HTML file will be directly returned.

### Set favicon

It is recommended to use [RealFaviconGenerator](https://realfavicongenerator.net/) to automatically generate favicon online and replace the `/static/favicons` directory with the generated one.

Alternatively, you can edit `/templates/head.html` to set favicon by yourself.

### Set theme

Set `theme` property (`default` as default) in `config.py`, and then run the following command to apply it:

```py
python app.py apply-theme
```

Note that the `theme` set here must be in the `themes` directory. There is a default theme `default` there initially. You can download or clone third-party themes (or from [BlogT](https://github.com/BlogTANG/blog-t)) there and set one of them to `theme` property to change your theme. Once you change the `theme` property, the command above should be runned to apply the change.

### Run web app

You can run dynamic web app use the command below:

```py
python app.py
```

### Generate static site

You can use `generate` subcommand to generate static site as well:

```py
python app.py generate
```

The generated files are in `_deploy` directory.

### Deploy to GitHub Pages

Deploying to GitHub Pages is supported.

Create an empty repository named `username.github.io` (change `username` to your GitHub username) on GitHub, and then run:

```py
python app.py setup-github-pages
```

Follow the instructions and set it up. This command is only needed for the first time.

Each time you added a new post, run the command below to generate static pages.

```py
python app.py generate
```

Then deploy the changes to GitHub Pages:

```py
python app.py deploy
```

## Custom Theme

You can write your own them to meet different needs. To write a theme, you should know about HTML, CSS, JavaScript and Jinja2 template engine.

First create a directory in `themes` with name as the name of the theme. Then create a `templates` directory in the theme directory, and write template files in the `templates` directory. If there a need to use static files, you can create a `static` directory in the theme directory and put static files in it. The theme `default` can be an example for you.

When running `apply-theme` command, contents in `templates` and `static` will be soft linked to the `templates` and `static` directories in root of the blog, and previously existing files that won't cause conflicts will be preserved. Thus, you can use public static files in the `static` directories in root of the blog, favicon for instance.

Jinja2 engine is used to render templates (see template syntax in [Template Designer Documentation](http://jinja.pocoo.org/docs/dev/templates/)). Key files and relations between these files and relative URLs are listed below.

```
/                                    -> index.html
/page/2                              -> index.html
/post/2016/03/03/some-title          -> post.html
/tag/some-tag                        -> tag.html
/category/some-category              -> category.html
/search?q={query-text}[&c=20&p=2]    -> search.html
```

The files above should be seen in `templates` directory, otherwise the app may not work properly.

Two variables `site` and `page` are sent to the template files while rendering them. `site` stores all configurations in `config.py`; `page` stores information about the current page, and here is the details:

```
# properties in "page" sent to index.html
has_newer: there are newer posts besides the current page or not
newer_url: link of newer posts, for example, value of this property is "/page/2" when the current page is "/page/3"
has_older: there are older posts besides the current page or not
older_url: link of older posts
entries: list of entries, each of which contains all properties marked at the beginning of the correspond post file, a "body" property that stores HTML strings rendered from the preview of Markdown body and a "read_more" property indicates that if there should be a "Read More" button

# properties in "page" sent to post.html
# Besides all properties marked at the beginning of the correspond post file and the "body", it contains the following two:
id_key: the unique key of the post
absolute_url: the absolute url of the post

# properties in "page" sent to tag.html and category.html
archive_type: archive type ("tag" or "category")
archive_name: tag or category name
entries: same as the "page" sent to index.html

# properties in "page" sent to search.html
query: query text
has_next: has next page
next_url: link of next page
has_prev: has previous page
prev_url: link of previous page
entries: list of entries that should be displayed on the current page, each of the entries contains all properties marked at the beginning of the correspond post or custom page file
```

## API Mode

You can switch to API mode by setting `mode` in `config.py` to `api`. In this mode, the previous URLs in "web-app" mode will return the corresponding JSON data, and two new interfaces, `/categories` and `/tags`, can be used to get category list and tag list separately.

You can also set `mode` to `mixed` to turn on mixed mode, in which, it will return JSON if `application/json` is added to `Accept` property in HTTP request header or url parameter `format=json` is set, or HTML if not.

See [API Description](api) for detailed API description.

JSONP is now supported.

You can use [BlogNG](https://github.com/BlogTANG/blog-ng) to take the most of this API mode and get excellent experience of the single page web app.

## Webhook Payload

When this feature is enabled, you can use `http://example.com/_webhook` (replace `http://example.com` with your own root URL) as the Payload URL on GitHub or other site that supports webhooks, and use a custom script to handle data of the POST request.

To enable this, set `webhook_enable` to True in `config.py`, then modify `handle(data)` function in `custom/webhook_handler.py` (manually create it if not exists) to handle the data. The `data` parameter here can be a JSON or a form, which is determined by `request.json or request.form`.
