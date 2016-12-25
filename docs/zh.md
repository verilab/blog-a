# BlogA

![License](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)
[![Build Status](https://travis-ci.org/BlogTANG/blog-a.svg?branch=master)](https://travis-ci.org/BlogTANG/blog-a)

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

注意这里选择的主题必须在 `themes` 目录下存在，默认有 `default` 主题，[BlogT](https://github.com/BlogTANG/blog-t) 项目中提供了一些其它主题，你也可以下载或 clone 第三方主题到这里然后将目录名设置到 `theme`。每次更改 `theme` 属性都需要重新执行上面的命令来应用更改。

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

具体 API 说明见 [API Description](api)。

该模式支持通过 JSONP 来进行跨站请求。

你可以使用 [BlogNG](https://github.com/BlogTANG/blog-ng) 前端来配合 API 模式使用，将会有较好的单页应用体验。

## Webhook 回调

Webhook 回调功能开启时，可以在 GitHub 等支持 Webhook 的网站，添加 `http://example.com/_webhook`（注意这里 `http://example.com` 换成你自己的地址）作为 Payload URL，从而在事件发生时接收 POST 请求并进行自定义的处理。

要开启 Webhook 回调功能，在 `config.py` 中，将 `webhook_enable` 设置为 True（默认为 False），然后修改 BlogA 目录下 `custom/webhook_handler.py` 中的 `handle(data)` 函数（文件或函数没有则手动创建）来自定义处理脚本。注意这里传入的 `data` 参数类型可能是 JSON 或表单，如果请求头标记了 `application/json` 则尝试读取 JSON，否则尝试读取表单，具体请依照你设置 Webhook 的网站的说明。
