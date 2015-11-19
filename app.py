import json
import datetime

import tornado.ioloop
import tornado.web
from tornado.options import define, options

tornado.options.define("port", default="8000")
tornado.options.define("debug", default=True)

try:
    import RPi.GPIO as GPIO
    has_gpio = True

    GPIO.setmode(GPIO.BOARD)
     
    Motor1A = 16
    Motor1B = 18
    Motor1E = 22

    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1E,GPIO.OUT)
 
except ImportError:
    has_gpio = False
 

def turn_motor_on():
    print "Turning motor on"
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
 
def turn_motor_off(): 
    print "Stopping motor"
    GPIO.output(Motor1E,GPIO.LOW)
 

def exit_func():
    print "bye bye!"
    if has_gpio:
        GPIO.cleanup()


import atexit
atexit.register(exit_func)


class TemplatePageHandler(tornado.web.RequestHandler):
    def get(self, url):
        self.render('html/'+url+'.html')

class CommandHandler(tornado.web.RequestHandler):
    def get(self):
        type_ = self.get_argument('type')
        state = self.get_argument('state')

        #Robot GPIO controls go here.
        if type_ == 'lmotor' and has_gpio:
            if state == 'start':
                turn_motor_on()
            else:
                turn_motor_off()


        
application = tornado.web.Application([
        (r"/", tornado.web.RedirectHandler, {'url': '/two-button'}),
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

