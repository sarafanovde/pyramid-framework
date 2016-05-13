from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import pyramid.httpexceptions as exc
import os

from pyramid.wsgi import wsgiapp


@wsgiapp
def index(environ, start_response):
    status = '200 OK'
    response_headers = [("Content-Type", "text/html")]
    result = []
    fd = open('./index.html','r')
    result = fd.read()
    start_response(status, response_headers)	
    return result

@wsgiapp
def aboutme(environ, start_response):
    status = '200 OK'
    response_headers = [("Content-Type", "text/html")]
    result = []	
    fd = open('./about/aboutme.html','r')
    result = fd.read()
    start_response(status, response_headers)	
    return result


MIDDLEWARE_TOP = "<div class='top'>Middleware TOP</div>"
MIDDLEWARE_BOTTOM =  "<div class='botton'>Middleware BOTTOM</div>"

class MiddleWare(object):
 	def __init__(self, app):
 		self.app = app

 	def __call__(self, environ, start_response):
 		response = self.app(environ, start_response)
 		print (response)
 		if response.find('<body>') >-1:
 				header,body = response.split('<body>')
 				bodycontent,htmlend = body.split('</body>')
 				bodycontent = '<body>'+ MIDDLEWARE_TOP + bodycontent + MIDDLEWARE_BOTTOM+'</body>'
 				return [header.encode() + bodycontent.encode() + htmlend.encode()]
 		else:
 			        return [MIDDLEWARE_TOP.encode() + response.encode()]



if __name__ == '__main__':
    configurator  = Configurator()
    configurator .add_route('root', '/')
    configurator .add_view(index, route_name='root')
    configurator .add_route('index_html', '/index.html')
    configurator .add_view(index, route_name='index_html')
    configurator .add_route('aboutme_html', '/about/aboutme.html')
    configurator .add_view(aboutme, route_name='aboutme_html')
    app = configurator .make_wsgi_app()
    App = MiddleWare(app)
    server = make_server('localhost', 8000, App)
    server.serve_forever()
