title: README

[![License](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](LICENSE)
[![Build Status](https://travis-ci.org/BlogTANG/blog-a.svg?branch=master)](https://travis-ci.org/BlogTANG/blog-a)

[中文](#zh) [English](#en)

<a name="zh"></a>

基于 Flask 的简易 Python 博客框架，要求 Python 版本 3.x（下面所有命令中的 `python` 可能需要换成 `python3`），Demo：[http://blog-a.demo.r-c.im](http://blog-a.demo.r-c.im)。

## 基本用法

### 安装 Python 模块

```py
pip install -r requirements.txt
```

### 网站配置

在 `config.py` 文件中修改网站配置信息。

### 添加 Post

使用 Markdown 书写 Post，放在 `posts` 目录，Post 文件名为 `yyyy-MM-dd-post-name.md` 或 `yyyy-MM-dd-post-name.markdown`，如 `2016-03-02-my-first-post.md`。

Markdown 文件开头使用 YAML 标记文章信息，可被识别的信息如下：

```yaml
title: My Post Title (默认从文件名获取, 如: "2016-03-02-my-first-post.md" 的默认 title 为 "My First Post")
layout: post (默认为 "post", 程序会在 "templates" 目录下查找相应名称的 HTML 模板文件)
url: (默认为 "root_url/year/month/day/title")
categories: [category1, category2] (默认为空)
tags: [tag1, tag2, tag3] (默认为空)
date: YYYY-MM-DD HH:MM:SS (默认从文件名获取)
updated: YYYY-MM-DD HH:MM:SS (默认为空)
author: Richard Chien (默认为 config.py 文件中设置的 author)
email: richardchienthebest@gmail.com (默认为 config.py 文件中设置的 email)
```

YAML 标记部分和正文 Markdown 部分用 `\n\n` 分隔，如：

```
title: My Post Title
tags: [tag1, tag2]
date: 2016-03-02 20:48

## Title
This is my first post.
```

如果需要在首页的文章列表采用「阅读更多」按钮，也就是截取文章开头一部分作为预览，可以在 Post 文件中 Markdown 正文的适当位置添加 `<!-- more -->` 标记，如果使用了这个标记，程序会将开头到第一个此标记之间的内容作为首页相应条目的预览，如果没有做这个标记，则默认显示全文，此功能可以在 `config.py` 中通过设置 `support_read_more` 属性来开关。（这个功能的前提是你所使用的主题模板支持「阅读更多」功能）

### 添加 Custom Page

在 `pages` 目录添加 Markdown 文件或 HTML 文件（可以在子目录中），比如 `readme.md` 或 `readme/index.md` 或 `readme/index.html`，第一种可以通过 `/readme.html` 来访问，后两种，即内容在子目录下，则可以通过 `/readme/` 或 `/readme/index.html` 来访问。

如果使用 Markdown 文件，则格式类似于书写 Post 时的格式，例如：

```
title: About
layout: page (默认为 "page", 程序会在 "templates" 目录下查找相应名称的 HTML 模板文件)
author: Richard Chien (默认为 config.py 文件中设置的 author)
email: richardchienthebest@gmail.com (默认为 config.py 文件中设置的 email)

This is an about page.
```

如果使用 HTML 文件，则直接返回 HTML 的内容。

### 设置 Favicon

建议使用 [RealFaviconGenerator](https://realfavicongenerator.net/) 在线生成 Favicon，并覆盖 `static` 目录下的 `favicons` 目录。

当然你也可以自行修改 `/templates/head.html` 文件中设置 Favicon 的部分。

### 设置主题

在 `config.py` 中设置 `theme` 属性（默认是 `default`）来指定要使用的主题，然后执行下面命令来应用当前选择的主题：

```py
python app.py apply-theme
```

注意这里选择的主题必须在 `themes` 目录下存在，默认有 `default` 主题，你也可以下载或 clone 第三方主题到这里然后将目录名设置到 `theme`。每次更改 `theme` 属性都需要重新执行上面的命令来应用更改。

### 运行 Web App

可以直接运行动态 Web App：

```py
python app.py
```

### 生成静态网站

也可通过 `generate` 子命令生成纯静态网站：

```py
python app.py generate
```

生成的静态文件在 `_deploy` 目录中。

### 部署到 GitHub Pages

支持自动部署到 GitHub Pages。

首先在 GitHub 创建一个名为 `username.github.io` 空仓库（`username` 换成你的 GitHub 用户名），然后运行：

```py
python app.py setup-github-pages
```

根据提示完成配置，此命令只需在第一次使用时运行。

每次添加了 Post 之后，运行下面命令来生成静态页面：

```py
python app.py generate
```

并运行：

```py
python app.py deploy
```

将网站的变动部署到 GitHub Pages。

## 自定义主题

你可以自己编写主题来适应不同的需求，编写自定义主题需要你对 HTML、CSS、JavaScript、Jinja2 模板有所了解。

首先在 `themes` 目录下创建一个子目录，目录名也就是主题名，然后在里面创建 `templates` 目录，在这个目录里面编写 HTML 模板文件，如果需要引入静态文件，在主题目录下再创建一个 `static` 目录（具体目录结构参考默认的 `default` 主题），把静态文件放在里面。

在执行 `apply-theme` 命令时，`templates` 和 `static` 目录里的内容都会被软链接到博客根目录的 `templates` 和 `static` 目录中，并且不会清除根目录的 `templates` 和 `static` 中原有的且不冲突的内容，因此你可以在模板中引入公共的静态文件，比如 Favicon。

模板使用 Jinja2 引擎，语法参考 [Template Designer Documentation](http://jinja.pocoo.org/docs/dev/templates/)。运行时程序要求确保 `templates` 目录下有名为 `index.html`、`post.html`、`tag.html`、`category.html`、`404.html` 的几个文件（如果需要支持搜索功能，还需要有 `search.html`），这些模板文件与 URL 的对应关系如下：

```
/                                    -> index.html
/page/2                              -> index.html
/post/2016/03/03/some-title          -> post.html
/tag/some-tag                        -> tag.html
/category/some-category              -> category.html
/search?q={query-text}[&c=20&p=2]    -> search.html
```

渲染 HTML 时传入的变量为 `site` 和 `page`。`site` 中保存网站信息，即 `config.py` 中的配置；`page` 中保存页面相关的信息，具体内容如下：

```
# 传入 index.html 的 page 的属性
has_newer: 有更新的 Post
newer_url: 更新的 Post 列表, 如在 "/page/3" 时, 此属性值为 "/page/2"
has_older: 有更早的 Post
older_url: 更早的 Post 列表
entries: 当前页面需要显示的所有 Post 条目列表，其中每一个列表项的属性即为 Post 文件开头的 YAML 标记的信息, 以及 "body", 保存已解析成 HTML 的 Markdown 正文预览内容, 和 "read_more", 表示当前是否需要显示 "阅读更多" 按钮

# 传入 post.html 的 page 的属性
# 除了 Post 文件开头的 YAML 标记的信息以及 "body" (这里的 "body" 是全文而不是预览) 外, 还包括下面两个:
id_key: 代表该 Post 的唯一值, 用于 Disqus 之类评论框
absolute_url: 链接到该 Post 的绝对路径, 用于 Disqus 之类评论框

# 传入 tag.html 和 category.html 的 page 的属性
archive_type: 归档类型 ("tag" 或 "category")
archive_name: Tag 或 Category 名
entries: 与传入 index.html 的 page 中的 entries 相同

# 传入 search.html 的 page 的属性
query: 查询的文本内容
has_next: 有下一页
next_url: 下一页的地址
has_prev: 有上一页
prev_url: 上一页的地址
entries: 当前搜索结果页面需要显示的所有条目列表，其中每一个列表项的属性即为 Post 或 Custom Page 文件开头的 YAML 标记的信息
```

## API 模式

可以在 `config.py` 中将 `mode` 修改为 `api` 来切换到 API 模式，该模式下，正常访问的 URL 会返回相应的 JSON 数据，并且新增加 `/categories` 和 `/tags` 两个接口来获取所有 Category 和 Tag 列表。

也可以将 `mode` 改为 `mixed` 来开启混合模式，该模式下，在 HTTP 请求头的 Accept 属性中添加 `application/json`，或者在 URL 中添加参数 `format=json`，将会返回 JSON 数据，否则返回正常的 HTML 数据。

具体 API 说明见 [`api.md`](api.md)。

该模式支持通过 JSONP 来进行跨站请求。

## TODO

- [x] 支持 Custom Page
- [x] 支持除 post 以外的 layout
- [x] 安装第三方模板
- [x] 搜索

---------

<a name="en"></a>

This is a simple blog app based on Flask, requiring Python 3.x (you may need to use `python3` instead of `python` in all commands below). Demo: [http://blog-a.demo.r-c.im](http://blog-a.demo.r-c.im).

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

Note that the `theme` set here must be in the `themes` directory. There is a default theme `default` there initially. You can download or clone third-party themes there and set one of them to `theme` property to change your theme. Once you change the `theme` property, the command above should be runned to apply the change.

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

See [`api.md`](api.md) for detailed API description.

JSONP is now supported.

## TODO

- [x] Support custom page
- [x] Support layout other than "post"
- [x] Install third-party templates
- [x] Search
