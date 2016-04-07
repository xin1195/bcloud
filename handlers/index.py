#!/usr/bin/env python
# _*_coding:utf-8_*_
import tornado
import tornado.auth
import tornado.web

from handlers.base import BaseHandler
from models.models import DeviceGroup


class IndexHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        device_groups = self.session.query(DeviceGroup).filter(DeviceGroup.company_id == self.get_secure_cookie('company_id')).all()
        self.render("sys_index.html", auth_user=self.current_user, device_groups=device_groups)

