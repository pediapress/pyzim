from libcpp.vector cimport vector
cdef extern from "<string>" namespace "std":
    cdef cppclass string:
        string()
        string(char*)
        char* c_str()

cdef extern from "pyas.h":
    cdef cppclass PyArticle:
        PyArticle(char namespace, string url, string title, string aid, string redirectAid, string mimetype)
        void setData(string)

    cdef cppclass PyArticleSource:
        PyArticleSource()
        void addArticle(PyArticle*)

    cdef void create(string& fname, PyArticleSource* src)

cdef extern from "cxxtools/log.h":
    cdef void log_init()

def init_log():
    log_init()


cdef class ArticleSource:
    cdef PyArticleSource* thisptr

    def __cinit__(self):
        self.thisptr = new PyArticleSource()

    def add_article(self, namespace, url, title, aid, redirect_aid=None, data=None, mimetype='text/html'):
        redirect_aid = redirect_aid or ''
        cdef PyArticle* article = new PyArticle(ord(namespace[0]), string(url), string(title), string(aid), string(redirect_aid), string(mimetype))
        if data is not None:
            article.setData(string(data))
        self.thisptr.addArticle(article)

    def __dealloc__(self):
        del self.thisptr

    def create(self, fname):
        create(string(fname), self.thisptr)
