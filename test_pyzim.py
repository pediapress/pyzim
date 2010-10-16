import pyzim
pyzim.init_log()

class article(object):
    url = ""
    aid = ""
    title = ""

    def __init__(self, **kw):
        self.__dict__.update(kw)

articles = [article(url="bla", title="bla", aid="blubb")]
asource = pyzim.ArticleSource(articles)
asource.create("bla.zim")

