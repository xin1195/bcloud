#!/usr/bin/env python
# _*_coding:utf-8_*_
import time
from sqlalchemy import and_
from tornado_json import schema
from tornado_json.requesthandlers import APIHandler
import logging
from handlers.base import BaseHandler
from models.models import User, Device, Company


# 用户接口 用于设备登录
class ApiUserHandler(APIHandler, BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @schema.validate()
    def post(self):
        try:
            username = self.get_argument('username_guai')
            password = self.get_argument('password_guai')
            user = self.session.query(User).filter(and_(User.username == username, User.password == password)).first()
            if user:
                logging.info(str(username) + 'login success')
                return 'true'
            else:
                logging.info(str(username) + 'login false')
                return 'false'
        except:
            logging.info(str(username) + 'login database_error')
            return 'database_error'


# 设备注册接口 用于设备注册
class ApiDeviceRegister(APIHandler, BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @schema.validate()
    def post(self):
        try:
            device = self.session.query(Device).filter(Device.device_id == self.get_argument('device_id')).first()
            if device:
                return 'device_already_exists'
            else:
                data = time.strftime("%Y-%m-%d")
                company = self.session.query(Company).filter(Company.code == self.get_argument('company')).first()
                device_data = Device(device_id=self.get_argument('device_id'),
                                     device_id_s=self.get_argument('device_id_s'),
                                     device_name=self.get_argument('device_name'),
                                     ip=self.get_argument('ip'),
                                     port=self.get_argument('port'),
                                     data=data,
                                     model=self.get_argument('model'),
                                     board_model=self.get_argument('board_model'),
                                     screen_size=self.get_argument('screen_size'),
                                     screen_resolution=self.get_argument('screen_resolution'),
                                     screen_number='3',
                                     cpu_model=self.get_argument('cpu_model'),
                                     cpu_num=self.get_argument('cpu_num'),
                                     ram_model=self.get_argument('ram_model'),
                                     ram_size=self.get_argument('ram_size'),
                                     mac_address=self.get_argument('mac_address'),
                                     voltage=self.get_argument('voltage'),
                                     power_consumption=self.get_argument('power_consumption'),
                                     device_position=self.get_argument('device_position'),
                                     company_id=company.id
                                     )
                self.session.add(device_data)
                self.session.commit()
                return 'device_register_ok'
        except:
            return 'database_error'


# 设备分屏数量接口
class ApiScreenNumber(APIHandler, BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @schema.validate()
    def post(self):
        try:
            device_id = self.get_argument('device_id')
            device = self.session.query(Device).filter(Device.device_id == device_id).first()
            list_data = []
            dict_data = dict()
            if device:
                dict_data['screen_number'] = device.screen_number
                list_data.append(dict_data)
                logging.info("device_id: success" + device_id)
                return list_data
            else:
                dict_data['screen_number'] = '3'
                list_data.append(dict_data)
                logging.info("device_id: success no device" + device_id)
                return list_data
        except:
            logging.info("device_id: database_error" + device_id)
            return 'database_error'
