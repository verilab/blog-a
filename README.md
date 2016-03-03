# Blog A

基于 Flask 的简易 Python 博客框架，要求 Python 版本 3.x。

## 基本用法

在 `config.py` 文件中修改网站配置信息。

使用 Markdown 书写 Post，放在 `posts` 目录，Post 文件名为 `yyyy-MM-dd-post-name.md` 或 `yyyy-MM-dd-post-name.markdown`，如 `2016-03-02-my-first-post.md`。

Markdown 文件开头使用 YAML 标记文章信息，可被识别的信息如下：

```yaml
title: My Post Title (默认从文件名获取, 如: 2016-03-02-my-first-post.md 的默认 title 为 "My First Post")
layout: post (默认为 "post", 暂不支持其他 layout)
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

运行 Web App：

```py
python3 app.py
```

## 自定义主题

模板使用 Jinja2 引擎，语法参考 [Template Designer Documentation](http://jinja.pocoo.org/docs/dev/templates/)，模板文件放在 `templates` 目录，运行时程序要求确保 `templates` 目录下有名为 `index.html`、`post.html`、`tag.html`、`category.html`、`404.html` 的几个文件，这些模板文件与 URL 的对应关系如下：

```
/ -> index.html
/page/2                     -> index.html
/post/2016/03/03/some-title -> post.html
/tag/some-tag               -> tag.html
/category/some-category     -> category.html
```

渲染 HTML 时传入的变量为 `site` 和 `page`。`site` 中保存网站信息，即 `config.py` 中 site info 部分的配置；`page` 中保存页面相关的信息，具体内容如下：

```
# 传入 index.html 的 page 的属性
has_newer: 有更新的 Post
newer_url: 更新的 Post 列表, 如在 "/page/3" 时, 此属性值为 "/page/2"
has_older: 有更早的 Post
older_url: 更早的 Post 列表
entries: 当前页面需要显示的所有 Post 条目列表，其中每一个列表项的属性即为 Post 文件开头的 YAML 标记的信息, 以及 "body", 保存已解析成 HTML 的 Markdown 正文内容

# 传入 post.html 的 page 的属性
# 除了 Post 文件开头的 YAML 标记的信息以及 "body" 外, 还包括下面两个:
id_key: 代表该 Post 的唯一值, 用于 Disqus 之类评论框
absolute_url: 链接到该 Post 的绝对路径, 用于 Disqus 之类评论框

# 传入 tag.html 的 page 的属性
tag: Tag 名称
entries: 与传入 index.html 的 page 中的 entries 相同

# 传入 category.html 的 page 的属性
category: Category 名称
entries: 与传入 index.html 的 page 中的 entries 相同
```

## TODO

- 支持除 post 以外的 layout
- 生成静态 HTML 文件
