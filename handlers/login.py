#!/usr/bin/env python
# _*_coding:utf-8_*_
import hashlib
import tornado
import tornado.gen
import logging
from sqlalchemy import and_
import time
from handlers.base import BaseHandler
from models.models import User


class LoginHandler(BaseHandler):
    def get(self):
        self.render('sys_login.html', login_err='')

    def post(self):
        username = self.get_argument('username')
        password = hashlib.sha256(self.get_argument('password').encode('utf-8')).hexdigest()
        user = self.session.query(User).filter(and_(User.username == username, User.password == password)).first()
        if user:
            self.set_secure_cookie('user_id', str(user.id))
            self.set_secure_cookie('username', username)
            self.set_secure_cookie('company_id', str(user.company_id))
            logging.info(str(username) + ' : login success')
            self.redirect('/')
        else:
            logging.info(str(username) + ' : login fail')
            self.render('sys_login.html', login_err='用户名或密码错误！')


class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie('username', None)
        self.redirect('/login')
