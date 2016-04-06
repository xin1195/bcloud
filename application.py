#!/usr/bin/env python
# _*_coding:utf-8_*_
import logging
import os.path
import tornado.web
from url import urls

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    # filename='logs/bcloud' + str(time.strftime("%Y%m%d%H%M%S")) + '.log',
                    filename='logs/bcloud.log',
                    filemode='w')

settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        login_url="/login",
        xsrf_cookies=True,
        debug=True,
)

application = tornado.web.Application(
        handlers=urls,
        **settings
)


