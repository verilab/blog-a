from attrdict import AttrDict

config = AttrDict(
    # site info
    title='RiCE Blog',
    subtitle='',
    root_url='http://blog.r-c.im',
    author='Richard Chien',
    email='richardchienthebest@gmail.com',

    # discuss field
    duoshuo_enable=False,
    duoshuo_short_name='richardchien',
    disqus_enable=True,
    disqus_short_name='richardchien',

    # configuration
    entry_count_one_page=10,
    feed_count=10,
    language='zh_CN',
    timezone='UTC+08:00',  # UTC±[hh]:[mm]
    host='0.0.0.0',
    port=8080,
)
