import json
import datetime
# import motor
# import markdown

import tornado.ioloop
import tornado.web
from tornado.options import define, options

# from handlers import EventHandler, QueryHandler
# import util

#Define core options. These can (and should!) be overridden by a config file.
tornado.options.define("port", default="8000")
tornado.options.define("debug", default=True)
# tornado.options.define("mongo_host", default="localhost")
# tornado.options.define("mongo_port", default="27017")
# tornado.options.define("log_config_file", default="config/logging-locks-DEV.json")

# mongo_client = motor.MotorClient('mongodb://'+options.mongo_host+':'+options.mongo_port)

class TemplatePageHandler(tornado.web.RequestHandler):
    def get(self, url):
        self.render('html/'+url+'.html')


class CommandHandler(tornado.web.RequestHandler):
    def get(self):
        print self.get_argument('type')
        print self.get_argument('state')
        
        # self.render('html/'+url+'.html')

#!!! This is a hacky, temporary way to avoid compiling to HTML a zillion times while I write the app.
# class MarkdownTemplatePageHandler(tornado.web.RequestHandler):
#     def get(self, url):
#         self.render('html/markdown.html', url=url)

application = tornado.web.Application([
        (r"/", tornado.web.RedirectHandler, {'url': '/home'}),
        (r"/command/", CommandHandler),
        # (r"/query/", QueryHandler),
        # (r"/home", tornado.web.StaticFileHandler),
        (r"/static/(.*?)", tornado.web.StaticFileHandler, {"path": "static"}),
        (r"/(.*?)", TemplatePageHandler),
    ],
    debug=options.debug,
    # db=mongo_client["db"],
    # logging_locks=util.LoggingLocks(json.load(file(options.log_config_file))),
)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

