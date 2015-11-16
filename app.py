import json
import datetime

import tornado.ioloop
import tornado.web
from tornado.options import define, options

tornado.options.define("port", default="8000")
tornado.options.define("debug", default=True)

class TemplatePageHandler(tornado.web.RequestHandler):
    def get(self, url):
        self.render('html/'+url+'.html')

class CommandHandler(tornado.web.RequestHandler):
    def get(self):
        print self.get_argument('type')
        print self.get_argument('state')

        #Robot GPIO controls go here.
        
application = tornado.web.Application([
        (r"/", tornado.web.RedirectHandler, {'url': '/home'}),
        (r"/command/", CommandHandler),
        # (r"/static/(.*?)", tornado.web.StaticFileHandler, {"path": "static"}),
        (r"/(.*?)", TemplatePageHandler),
    ],
    debug=options.debug,
)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

