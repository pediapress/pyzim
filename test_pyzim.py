import pyzim

pyzim.init_log()

src = pyzim.ArticleSource()

lorem = '''<div><a href="A/Redirect">Link!!!11</a> <img src="I/Test.jpg" width="200" height="100" /> Lorem ipsum dolor sit <strong>amet</strong>, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.</div>\n'''

#lorem = ' '.join([chr(x) for x in range(ord('A'), ord('Z')+1)])
#lorem = lorem*10 + 'X'

def kw(title, data=None, redirect_aid=None):
    aid = title.replace(' ', '_')
    return {
        'namespace': 'A',
        'title': title,
        'aid': aid,
        'url': title,
        'redirect_aid': redirect_aid,
        'mimetype': 'text/html',
        'data': data,
    }

src.add_article(**kw('Test', data=lorem)) #<p>Some <strong>HTML</strong></p>'))
#src.add_article(**kw('Redirect', redirect_aid='Redirect_target'))
#src.add_article(**kw('Redirect target', data='REDIRECT TARGET' + lorem))
src.add_article(namespace='I', title='Test.jpg', data=open('Test.jpg').read(), mimetype='image/jpeg', aid='Test.jpg', url='Test.jpg')

src.create('test.zim')
