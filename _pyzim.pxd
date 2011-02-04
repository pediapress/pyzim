from cpython.ref cimport PyObject

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
