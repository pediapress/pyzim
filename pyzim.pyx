from libcpp.vector cimport vector
cdef extern from "<string>" namespace "std":
    cdef cppclass string:
        string()
        string(char *)
        char * c_str()

cdef extern from "pyas.h":
    cdef cppclass PyArticle:
        string url
        string title
        string aid

    ctypedef PyArticle * PyArticlePtr
    cdef cppclass PyArticleSource:
        vector[PyArticlePtr] articles

    cdef void create(string &fname, PyArticleSource *src)

cdef extern from "cxxtools/log.h":
    cdef void log_init()

def init_log():
    log_init()

cdef PyArticle * make_article(url, title, aid):
    cdef PyArticle *a = new PyArticle()
    a.url = string(url)
    a.title = string(title)
    a.aid = string(aid)
    return a


cdef class ArticleSource:
    cdef PyArticleSource *thisptr
    def __cinit__(self, articles):
        self.thisptr = new PyArticleSource()
        for x in articles:
            self.thisptr.articles.push_back(make_article(x.url, x.title, x.aid))

    def __dealloc__(self):
        del self.thisptr

    def create(self, fname):
        create(string("bla"), self.thisptr)



def doit():
    cdef PyArticle *a = new PyArticle()
    a.url = string("bla")

    cdef PyArticleSource *src = new PyArticleSource()
    create(string("bla.zim"), src)
