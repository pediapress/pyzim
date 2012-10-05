__version_info__ = (0, 3, 0)
version = __version__ = "0.3.0"

from _pyzim import init_log, ArticleSource, Article, zimfile


class IterArticleSource(ArticleSource):
    """Be more Pythonic by implementing get_next_article() using __iter__().

    (Currently, Cython does not support the yield stmt.)
    """

    def get_next_article(self):
        if self.it is None:
            self.it = iter(self)
        try:
            return self.it.next()
        except StopIteration:
            self.it = None
            return None

    def __iter__(self):
        "Implement this"

        yield None
