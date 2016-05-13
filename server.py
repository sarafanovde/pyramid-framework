from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import pyramid.httpexceptions as exc
import os

from pyramid.wsgi import wsgiapp


@wsgiapp
def index_html(environ, start_response):
    status = '200 OK'
    response_headers = [("Content-Type", "text/html")]
    result = []
    file = open('./index.html','rb')
    for x in file:
    	result.append(x)
    start_response(status, response_headers)	
    return result
@wsgiapp
def aboutme_html(environ, start_response):
    status = '200 OK'
    response_headers = [("Content-Type", "text/html")]
    result = []	
    file = open('./about/aboutme.html','rb')	
    for x in file:
    	result.append(x)
    start_response(status, response_headers)
    return result


MIDDLEWARE_TOP = "<div class='top'>Middleware TOP</div>"
MIDDLEWARE_BOTTOM =  "<div class='botton'>Middleware BOTTOM</div>"

class MyMiddleWare(object):
 	def __init__(self, app):
 		self.app = app

 	def __call__(self, environ, start_response):
 		#Вставляем TOP and BOTTOM
	 	openBody = -1
 		closeBody = -1
 		response = self.app(environ, start_response)
 		for x in response:
 			if "<body>" in x.decode():
	 			openBody = response.index(x)
 			if "</body>" in x.decode():
 				closeBody = response.index(x)
 		result = response[:openBody] + [MIDDLEWARE_TOP.encode()] + response[openBody:closeBody+1] + [MIDDLEWARE_BOTTOM.encode()] + response[closeBody+1:]
 		return result



if __name__ == '__main__':
    config = Configurator()
    config.add_route('root', '/')
    config.add_view(index_html, route_name='root')
    config.add_route('index_html', '/index.html')
    config.add_view(index_html, route_name='index_html')
    config.add_route('aboutme_html', '/about/aboutme.html')
    config.add_view(aboutme_html, route_name='aboutme_html')
    app = config.make_wsgi_app()
    myApp = MyMiddleWare(app)
    server = make_server('0.0.0.0', 8000, myApp)
    server.serve_forever()
