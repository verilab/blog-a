from attrdict import AttrDict

config = AttrDict(
    # site info
    title='My Blog',
    subtitle='Yet another BlogA blog.',
    root_url='http://example.com',
    author='Your Name',
    email='example@example.com',

    # discuss field
    duoshuo_enable=False,
    duoshuo_short_name='',
    disqus_enable=False,
    disqus_short_name='',

    # configuration
    theme='default',  # run 'python app.py apply-theme' after changing this
    support_read_more=True,
    entry_count_one_page=5,
    feed_count=10,
    language='zh_CN',
    timezone='UTC+08:00',  # UTC±[hh]:[mm]
    host='0.0.0.0',
    port=8080,
    mode='mixed',  # 'web-app' or 'api' or 'mixed'
)
