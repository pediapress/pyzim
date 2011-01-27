cimport _pyzim

cimport cpython.ref as cpy_ref


def init_log():
    log_init()


class Article(object):
    def __init__(self, title, namespace='A', url=None, aid=None, redirect_aid=None, mimetype='text/html'):
        assert title, 'title is requried'
        self.title = title
        self.aid = aid or title
        self.url = url or title
        self.namespace = namespace
        self.mimetype = mimetype
        self.redirect_aid = redirect_aid or ''


cdef PyArticle* cy_get_next_article(PyObject* ptr):
    cdef ArticleSource src = <ArticleSource>(ptr)
    art = src.get_next_article()
    if art is None:
        return NULL
    cdef PyArticle* pyart = new PyArticle(ord(art.namespace[0]), string(art.url), string(art.title), string(art.aid), string(art.redirect_aid), string(art.mimetype))
    return pyart


cdef string cy_get_data(PyObject* ptr, string aid):
    cdef ArticleSource src = <ArticleSource>(ptr)
    data = src.get_data(aid.c_str())
    return string(data, len(data))


cdef class ArticleSource:
    cdef PyArticleSource* thisptr

    def __cinit__(self):
        self.thisptr = new PyArticleSource(<cpy_ref.PyObject*>self, cy_get_next_article, cy_get_data)
        self.it = None

    def get_next_article(self):
        return None

    def get_data(self, aid):
        return 'ArticleSource.get_data() needs to be implemented!'

    def __dealloc__(self):
        del self.thisptr

    def create(self, fname):
        create(string(fname), self.thisptr)
