#!/usr/bin/env python
# _*_coding:utf-8_*_
import hashlib
import time
import tornado
import tornado.auth
import tornado.web

from handlers.base import BaseHandler
from models.models import Company, User


# 公司管理
class CompanyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        companys = self.session.query(Company).filter(Company.id == self.get_secure_cookie('company_id')).all()
        self.render("fra_com_list.html", auth_user=self.current_user, companys=companys)


# 公司新增
class CompanyAddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        err = ''
        self.render("fra_com_add.html", auth_user=self.current_user, err=err)

    @tornado.web.authenticated
    def post(self):
        name = self.get_argument('name')
        code = self.get_argument('code')
        address = self.get_argument('address')
        parent = self.get_argument('parent')
        company = self.session.query(Company).filter(Company.code == code).first()
        if company:
            err = '公司编码已存在'
            self.render("fra_com_add.html", auth_user=self.current_user, err=err)
        else:
            data = time.strftime("%Y-%m-%d")
            company = Company(
                    name=name,
                    code=code,
                    address=address,
                    parent=parent,
                    data=data,
            )
            self.session.add(company)
            self.session.commit()
            self.redirect('/fra/com')


# 公司修改
class CompanyUpdateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        code = self.get_argument('code')
        if code:
            err = ''
            company = self.session.query(Company).filter(Company.code == code).first()
            self.render("fra_com_detail.html", auth_user=self.current_user, company=company, err=err)
        else:
            err = '公司编码不存在'
            self.render("fra_com_detail.html", auth_user=self.current_user, err=err)

    @tornado.web.authenticated
    def post(self):
        name = self.get_argument('name')
        code = self.get_argument('code')
        address = self.get_argument('address')
        parent = self.get_argument('parent')
        company = self.session.query(Company).filter(Company.code == code).first()
        if company:
            data = time.strftime("%Y-%m-%d")
            company = Company(
                    id=company.id,
                    name=name,
                    code=code,
                    address=address,
                    parent=parent,
                    data=data,
            )
            self.session.merge(company)
            self.session.commit()
            self.redirect('/fra/com')
        else:
            err = '公司编码不存在'
            self.render("fra_com_add.html", auth_user=self.current_user, err=err)


# 公司删除
class CompanyDeteleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        code = self.get_argument('code')
        if code:
            company = self.session.query(Company).filter(Company.code == code).first()
            self.session.delete(company)
            self.session.commit()
            self.redirect('/fra/com')
        else:
            err = '公司编码不存在'
            self.render("fra_com_detail.html", auth_user=self.current_user, err=err)


# 人员管理
class UserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        users = self.session.query(User).filter(User.company_id == self.get_secure_cookie('company_id')).all()
        self.render("fra_user_list.html", auth_user=self.current_user, users=users)


# 人员新增管理
class UserAddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        err = ''
        companys = self.session.query(Company).filter().all()
        self.render("fra_user_add.html", auth_user=self.current_user, companys=companys, err=err)

    @tornado.web.authenticated
    def post(self):
        username = self.get_argument('username')
        # sha256加密
        password = hashlib.sha256(self.get_argument('password')).hexdigest()
        email = self.get_argument('email')
        tell_phone = self.get_argument('tell_phone')
        company_id = self.get_argument('company_id')
        user = self.session.query(User).filter(User.username == username).first()
        if user:
            err = '用户已经存在'
            self.render("fra_user_add.html", auth_user=self.current_user, err=err)
        else:
            data = time.strftime("%Y-%m-%d")
            user = User(
                    username=username,
                    password=password,
                    email=email,
                    data=data,
                    tell_phone=tell_phone,
                    company_id=company_id,
            )
            self.session.add(user)
            self.session.commit()
            self.redirect('/fra/user')


# 人员修改管理
class UserUpdateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_id = self.get_argument('id')
        if user_id:
            user = self.session.query(User).filter(User.id == user_id).first()
            if user:
                err = ''
                self.render("fra_user_detail.html", auth_user=self.current_user, user=user, err=err)
            else:
                err = '人员不存在'
                users = self.session.query(User).filter().all()
                self.render("fra_user_list.html", auth_user=self.current_user, users=users, err=err)
        else:
            err = '人员不存在'
            users = self.session.query(User).filter().all()
            self.render("fra_user_list.html", auth_user=self.current_user, users=users, err=err)

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument('id')
        username = self.get_argument('username')
        password = hashlib.sha256(self.get_argument('password')).hexdigest()
        email = self.get_argument('email')
        tell_phone = self.get_argument('tell_phone')
        user = self.session.query(User).filter(User.id == id).first()
        if user:
            if self.get_argument('password') == '':
                user = User(
                    id=id,
                    username=username,
                    email=email,
                    tell_phone=tell_phone,
                )
                self.session.merge(user)
                self.session.commit()
                self.redirect('/fra/user')
            else:
                user = User(
                    id=id,
                    username=username,
                    password=password,
                    email=email,
                    tell_phone=tell_phone,
                )
                self.session.merge(user)
                self.session.commit()
                self.redirect('/fra/user')

        else:
            err = '用户不存在'
            users = self.session.query(User).filter().all()
            self.render("fra_user_list.html", auth_user=self.current_user, users=users, err=err)


# 人员删除管理
class UserDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_id = self.get_argument('id')
        if user_id:
            user = self.session.query(User).filter(User.id == user_id).first()
            self.session.delete(user)
            self.session.commit()
            self.redirect('/fra/user')
        else:
            err = '删除的人员不存在'
            self.render("fra_user_list.html", auth_user=self.current_user, err=err)
