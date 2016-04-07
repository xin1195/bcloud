#!/usr/bin/env python
# _*_coding:utf-8_*_
import tornado
import tornado.gen
import tornado.web
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_CONNECT_STRING = 'mysql://root:bestom123456@112.74.16.96/bcloudTest?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo=True)
# engine = create_engine(DB_CONNECT_STRING)
DB_Session = sessionmaker(bind=engine)


# 基类
class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.session = DB_Session()

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie("username")

    def on_finish(self):
        self.session.close()
