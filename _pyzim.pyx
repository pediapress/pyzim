
from cpython.ref cimport PyObject

cimport cpython.ref as cpy_ref
from libcpp cimport bool
from libcpp.string cimport string as stdstring

cdef extern from "<string>" namespace "std":
    cdef cppclass string:
        string()
        string(char*)
        string(char*, size_t n)
        char* c_str()

cdef extern from "cxxtools/log.h":
    cdef void log_init()

cdef extern from "pyas.h":
    cdef cppclass PyArticle:
        PyArticle(char namespace, string url, string title, string aid, string redirectAid, string mimetype)

    ctypedef PyArticle* (*GetNextArticle)(PyObject* pyObj)
    ctypedef string (*GetData)(PyObject* pyObj, string aid)

    cdef cppclass PyArticleSource:
        PyArticleSource(PyObject*, GetNextArticle, GetData)

    cdef void create(string& fname, PyArticleSource* src)


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


cdef extern from "zim/file.h":
   cdef cppclass _zimfile "zim::File":
       _zimfile(char *) except +
       bool verify() except +
       stdstring getChecksum() except +

cdef class zimfile(object):
    cdef _zimfile *_ptr
    def __cinit__(self, fn):
        self._ptr = new _zimfile(fn)

    def __dealloc__(self):
        del self._ptr

    def verify(self):
        return self._ptr.verify()

    @property
    def checksum(self):
        return self._ptr.getChecksum()
