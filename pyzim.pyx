from libcpp.vector cimport vector
cdef extern from "<string>" namespace "std":
    cdef cppclass string:
        string()
        string(char *)
        char * c_str()

cdef extern from "pyas.h":
    cdef cppclass PyArticle:
        PyArticle(string, string, string)

    cdef cppclass PyArticleSource:
        PyArticleSource()
        void push_back(PyArticle*)

    cdef void create(string &fname, PyArticleSource *src)

cdef extern from "cxxtools/log.h":
    cdef void log_init()

def init_log():
    log_init()

cdef PyArticle* make_article(url, title, aid):
    return new PyArticle(string(url), string(title), string(aid))


cdef class ArticleSource:
    cdef PyArticleSource *thisptr
    def __cinit__(self, articles):
        self.thisptr = new PyArticleSource()
        for x in articles:
            self.thisptr.push_back(make_article(x.url, x.title, x.aid))

    def __dealloc__(self):
        del self.thisptr

    def create(self, fname):
        create(string(fname), self.thisptr)
