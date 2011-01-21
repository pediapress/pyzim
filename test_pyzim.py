import pyzim

pyzim.init_log()

src = pyzim.ArticleSource()

def kw(title, data=None, redirect_aid=None):
    aid = title.replace(' ', '_')
    return {
        'namespace': 'A',
        'title': title,
        'aid': aid,
        'url': title,
        'redirect_aid': redirect_aid,
        'mimetype': 'text/html',
        'data': data,
    }

src.add_article(**kw('Test', data='<p>Some <strong>HTML</strong></p>'))
src.add_article(**kw('Redirect', redirect_aid='Redirect_target'))
src.add_article(**kw('Redirect target', data='<p>HTML data of redirect target</p>'))

src.create('test.zim')
