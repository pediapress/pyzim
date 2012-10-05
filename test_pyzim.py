#! /usr/bin/env py.test

import pyzim

lorem = u'''<div><a href="A/Redirect">Link!!!11</a> <img src="/I/Test.jpg" width="200" height="100" /> Lorem ipsum dolor sit <strong>amet</strong>, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.</div>\n'''

#lorem = ' '.join([chr(x) for x in range(ord('A'), ord('Z')+1)])
#lorem = lorem*10 + 'X'


#pyzim.init_log()


class TestArticleSource(pyzim.IterArticleSource):
    def __init__(self, num_articles):
        self.num_articles = num_articles

    def __iter__(self):
        yield pyzim.Article('Test.jpg', url='Test.jpg', namespace='I', mimetype='image/jpeg')
        for i in range(self.num_articles):
            yield pyzim.Article('Test {0}'.format(i))

    def get_data(self, aid):
        if aid == 'Test.jpg':
            print 'returning image'
            return open('Test.jpg', 'rb').read()
        return u'<h1>{0}</h1>\n{1}'.format(aid, lorem)


def test_create():
    src = TestArticleSource(100)
    src.create('test.zim')
    zf = pyzim.zimfile("test.zim")
    print "checksum:", zf.checksum
    zf.verify()

