#!/usr/bin/python
# _*_coding:utf-8_*_
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import define, options
from application import application
define("port", default=8008, help="run on the given port", type=int)


def main():
    # debug|info|warning|error|none 日志级别
    tornado.options.options.logging = "info"
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
