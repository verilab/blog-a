from attrdict import AttrDict

config = AttrDict(
    # site info
    title='Blog A',
    subtitle='Yet another Blog A',
    root_url='http://example.com',
    author='Your Name',
    email='example@example.com',

    # discuss field
    duoshuo_enable=False,
    duoshuo_short_name='',
    disqus_enable=False,
    disqus_short_name='',

    # configuration
    support_read_more=False,
    entry_count_one_page=0,
    feed_count=10,
    language='zh_CN',
    timezone='UTC+08:00',  # UTC±[hh]:[mm]
    host='0.0.0.0',
    port=8080,
)
