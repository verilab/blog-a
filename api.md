# API Description

## Posts

- `GET /`, the same as `GET /page/1`.

- `GET /page/<int:page_id>`, get posts on a specific page.

Out:

```json
{
  "ok": true,
  "page": {
    "entries": [
      {
        "author": "Your Name",
        "body": "<p>content</p>",
        "categories": [
          "Category1"
        ],
        "date": "Wed, 15 Jun 2016 16:00:00 GMT",
        "email": "example@example.com",
        "layout": "post",
        "read_more": false,
        "tags": [
          "Tag1",
          "Tag2",
          "Tag3"
        ],
        "title": "Post Title",
        "url": "/post/2016/06/16/test-post"
      }
    ],
    "has_newer": false,
    "has_older": false,
    "newer_url": "",
    "older_url": ""
  },
  "site": {
    "author": "Your Name",
    "disqus_enable": false,
    "disqus_short_name": "",
    "duoshuo_enable": false,
    "duoshuo_short_name": "",
    "email": "example@example.com",
    "entry_count_one_page": 0,
    "feed_count": 10,
    "host": "0.0.0.0",
    "language": "zh_CN",
    "mode": "api",
    "port": 8080,
    "root_url": "http://example.com",
    "subtitle": "Yet another Blog A",
    "support_read_more": false,
    "timezone": "UTC+08:00",
    "title": "Blog A"
  }
}
```

- `GET /post/<string:year>/<string:month>/<string:day>/<post_name>`, get a post.

Out:

```json
{
  "ok": true,
  "page": {
    "absolute_url": "http://example.com/post/2014/02/03/test-post",
    "author": "Your Name",
    "body": "<p>content</p>",
    "categories": [
      "Category1"
    ],
    "date": "Mon, 03 Feb 2014 16:00:00 GMT",
    "email": "example@example.com",
    "id_key": "2014-02-03-test-post",
    "layout": "post",
    "read_more": false,
    "tags": [
      "Tag1"
    ],
    "title": "Post Title",
    "updated": "Tue, 04 Feb 2014 16:00:00 GMT",
    "url": "/post/2014/02/03/test-post"
  },
  "site": {
    "author": "Your Name",
    "disqus_enable": false,
    "disqus_short_name": "",
    "duoshuo_enable": false,
    "duoshuo_short_name": "",
    "email": "example@example.com",
    "entry_count_one_page": 0,
    "feed_count": 10,
    "host": "0.0.0.0",
    "language": "zh_CN",
    "mode": "api",
    "port": 8080,
    "root_url": "http://example.com",
    "subtitle": "Yet another Blog A",
    "support_read_more": false,
    "timezone": "UTC+08:00",
    "title": "Blog A"
  }
}
```

## Categories and Tags

- `GET /categories`, get category list.

Out:

```json
{
  "ok": true,
  "data": [
    "Category1",
    "Category2"
  ]
}
```

- `GET /category/<string:c>`, get all posts of a specific category, output is similar to `GET /page/<int:page_id>`.

- `GET /tags`, get tag list.

Out:

```json
{
  "ok": true,
  "data": [
    "Tag1",
    "Tag2"
  ]
}
```

- `GET /tag/<string:t>`, get all posts of a specific tag, output is similar to `GET /page/<int:page_id>`.

## Custom Pages

- `GET /<path:custom_page_path>`, get custom page.

Out:

```json
{
  "ok": true,
  "page": {
    "absolute_url": "http://example.com/about",
    "author": "Your Name",
    "body": "<p>This is an about page.</p>\n",
    "email": "example@example.com",
    "id_key": "about",
    "layout": "page",
    "title": "About"
  },
  "site": {
    "author": "Your Name",
    "disqus_enable": false,
    "disqus_short_name": "",
    "duoshuo_enable": false,
    "duoshuo_short_name": "",
    "email": "example@example.com",
    "entry_count_one_page": 0,
    "feed_count": 10,
    "host": "0.0.0.0",
    "language": "zh_CN",
    "mode": "api",
    "port": 8080,
    "root_url": "http://example.com",
    "subtitle": "Yet another Blog A",
    "support_read_more": false,
    "timezone": "UTC+08:00",
    "title": "Blog A"
  }
}
```

## 404

Out:

```json
{
  "ok": false
}
```
