#! /usr/bin/env python

from hashlib import sha1
import mimetypes
import os
import shutil
import sys
import tempfile

from lxml import etree

from remix.collection import WebPage, coll_from_zip
import pyzim



def src2aid(src):
    return sha1(src).hexdigest()



class ZIPArticleSource(pyzim.IterArticleSource):
    def __init__(self, zipfn):
        self.tmpdir = tempfile.mkdtemp()
        self.coll = coll_from_zip(self.tmpdir, zipfn)
        self.aid2article = {}

    def __del__(self):
        if os.path.exists(self.tmpdir):
            shutil.rmtree(self.tmpdir)

    def __iter__(self):
        for lvl, webpage in self.coll.outline.walk(cls=WebPage):
            title = webpage.title
            aid = title # webpage.id FIXME
            url = aid # FIXME
            article = pyzim.Article(title, aid=aid, url=url, mimetype='text/html', namespace='A')
            article.webpage = webpage
            self.aid2article[aid] = article
            yield article

            for src, fn in webpage.images.items():
                aid = src2aid(src)
                title = aid # TODO
                url = aid
                mimetype = mimetypes.guess_type(fn)[0]
                img = pyzim.Article(title, aid=aid, url=url, mimetype=mimetype, namespace='I')
                img.filename = fn
                self.aid2article[aid] = img
                yield img

    def get_data(self, aid):
        article = self.aid2article[aid]
        if article.namespace == 'A':
            webpage = self.aid2article[aid].webpage
            root = webpage.tree
            self.rewrite_links(root)
            self.rewrite_img_srcs(root)
            return etree.tostring(root)
        elif article.namespace == 'I':
            fn = self.aid2article[aid].filename
            data = open(fn, 'rb').read()
            print fn, len(data)
            return data

    def rewrite_links(self, root):
        for a in root.xpath('//a[@title]'):
            title = a.attrib['title']
            aid = title # FIXME
            if aid in self.aid2article:
                a.set('href', '/A/{0}'.format(title))

    def rewrite_img_srcs(self, root):
        for img in root.xpath('//img'):
            aid = src2aid(img.attrib['src'])
            if aid in self.aid2article:
                img.attrib['src'] = '/I/{0}'.format(aid)


def zip2zim(zipfn, zimfn):
    src = ZIPArticleSource(zipfn)
    src.create(zimfn)


def main():
    if len(sys.argv) != 3:
        sys.exit('Usage: {0} ZIPFILE ZIMFILE'.format(sys.argv[0]))
    zipfn, zimfn = sys.argv[1:3]
    zip2zim(zipfn, zimfn)

if __name__ == '__main__':
    main()
