#!/usr/bin/env python
# _*_coding:utf-8_*_

# 基本方法
import logging
import time

import tornado

from handlers.base import DB_Session
from models.models import ResGroup, Device, Company, DeviceTimeSwitch


class BaseFunctionHandler(tornado.web.RequestHandler):

    # 注册数据信息
    @staticmethod
    def device_res(self, data_dict):
        try:
            db_session = DB_Session()
            device = db_session.query(Device).filter(Device.device_id == data_dict['device_id']).first()
            if device:
                logging.info('device is has')
                return 'device is has'
            else:
                data = time.strftime("%Y-%m-%d")
                company = db_session.query(Company).filter(Company.code == data_dict['company']).first()
                device_data = Device(device_id=data_dict['device_id'],
                                     device_id_s=data_dict['device_id_s'],
                                     device_name=data_dict['device_name'],
                                     ip=data_dict['ip'],
                                     port=data_dict['port'],
                                     data=data,
                                     model=data_dict['model'],
                                     board_model=data_dict['board_model'],
                                     screen_size=data_dict['screen_size'],
                                     screen_resolution=data_dict['screen_resolution'],
                                     screen_number='3',
                                     cpu_model=data_dict['cpu_model'],
                                     cpu_num=data_dict['cpu_num'],
                                     ram_model=data_dict['ram_model'],
                                     ram_size=data_dict['ram_size'],
                                     mac_address=data_dict['mac_address'],
                                     voltage=data_dict['voltage'],
                                     power_consumption=data_dict['power_consumption'],
                                     device_position=data_dict['device_position'],
                                     company_id=company.id
                                     )
                db_session.add(device_data)
                db_session.commit()
                logging.info("设备注册成功:" + str(device_data))
                return 'device_register_success'
        except:
            return 'device_register_fail'
        finally:
            db_session.close()

    # 获取定时开关机
    @staticmethod
    def get_device_time_switch(self, device_time_switch_id):
        try:
            db_session = DB_Session()
            device_time_switch = db_session.query(DeviceTimeSwitch).filter(DeviceTimeSwitch.id == device_time_switch_id).first()
            week_list = list()
            dict_data = dict()
            dict_data['cmd'] = 'timeSwitch'
            week_list.append(dict_data)
            for device_week in device_time_switch.device_week:
                week_dict = dict()
                device_days = device_week.device_day
                day_list = list()
                for device_day in device_days:
                    day_dict = dict()
                    day_dict['name'] = device_day.name
                    day_dict['time'] = str(device_day.time)
                    day_dict['screen'] = device_day.screen
                    day_list.append(day_dict)
                week_dict['week_name'] = device_week.name
                week_dict['day_date'] = day_list
                week_list.append(week_dict)
            return device_time_switch, week_list
        except:
            return 'database_error'
        # finally:
        #     db_session.close()

    # 获取定时开关机
    @staticmethod
    def get_time_switch(device_id):
        try:
            db_session = DB_Session()
            device = db_session.query(Device).filter(Device.device_id == device_id).first()
            device_weeks = device.deviceGroup.device_timeSwitch.device_week
            week_list = list()
            dict_data = dict()
            dict_data['cmd'] = 'timeSwitch'
            week_list.append(dict_data)
            for device_week in device_weeks:
                week_dict = dict()
                device_days = device_week.device_day
                day_list = list()
                for device_day in device_days:
                    day_dict = dict()
                    day_dict['name'] = device_day.name
                    day_dict['time'] = str(device_day.time)
                    day_dict['screen'] = device_day.screen
                    day_list.append(day_dict)
                week_dict['week_name'] = device_week.name
                week_dict['day_date'] = day_list
                week_list.append(week_dict)
            return week_list
        except:
            return 'database_error'
        finally:
            db_session.close()

    # 获取资源组数据
    @staticmethod
    def get_res_group_by_device_id(device_id):
        try:
            db_session = DB_Session()
            device = db_session.query(Device).filter(Device.device_id == device_id).first()
            res_group_id = device.deviceGroup.resGroup_id
            res_group, playlist = BaseFunctionHandler.get_res_group_by_res_group_id(res_group_id)
            return playlist
        except:
            playlist = [{
                'cmd': 'playlist'
            },{
                'content': '广东尚景捷讯数码科技有限公司（简称尚景捷讯）是一家致力于电商平台服务和O2O综合网络商城运营为一体的高科技企业。公司以打造一站式服务平台为战略目标，以提供高质量产品、为客户创造价值为核心理念，具有“天地人”三位一体的商业销售模式，独特的经营理念和制度化的管理。在经营的过程中坚持创新的购物体验理念，保证客户利益最大化。公司团队注重自身技能的提升与综合素质的培养，始终坚持诚信经营、客户至上的原则和专注、联盟、创新、严谨的核心价值体系，提供最贴近客户需要的资源与服务。',
                'path': '',
                'type': 'text',
                'name': '尚景捷迅'
            },{
                'content': '',
                'path': '/media/public/image/SJ1.jpg',
                'type': 'image',
                'name': '尚景新起点'
            },{
                'content': '',
                'path': '/media/public/video/SJ1.mp4',
                'type': 'video',
                'name': '尚景新起点'
            },{
                'content': 'http://www.sjjxsm.com',
                'path': 'http://www.sjjxsm.com',
                'type': 'url',
                'name': '尚景商城'
            }]
            return playlist
        finally:
            db_session.close()

    # 获取资源组数据
    @staticmethod
    def get_res_group_by_res_group_id(res_group_id):
        try:
            db_session = DB_Session()
            res_group = db_session.query(ResGroup).filter(ResGroup.id == res_group_id).first()
            playlist = list()
            dict_data = dict()
            dict_data['cmd'] = 'playlist'
            playlist.append(dict_data)
            res_texts = res_group.resText
            res_webs = res_group.resWeb
            res_images = res_group.resImage
            res_videos = res_group.resVideo
            if res_texts:
                for res_text in res_texts:
                    dict_data = dict()
                    dict_data['type'] = 'text'
                    dict_data['name'] = res_text.name
                    dict_data['path'] = ''
                    dict_data['content'] = res_text.content
                    playlist.append(dict_data)
            if res_images:
                for res_image in res_images:
                    dict_data = dict()
                    dict_data['type'] = 'image'
                    dict_data['name'] = res_image.name
                    dict_data['path'] = res_image.path
                    dict_data['content'] = ''
                    playlist.append(dict_data)
            if res_videos:
                for res_video in res_videos:
                    dict_data = dict()
                    dict_data['type'] = 'video'
                    dict_data['name'] = res_video.name
                    dict_data['path'] = res_video.path
                    dict_data['content'] = ''
                    playlist.append(dict_data)
            if res_webs:
                for res_web in res_webs:
                    dict_data = dict()
                    dict_data['type'] = 'url'
                    dict_data['name'] = res_web.name
                    dict_data['path'] = res_web.content
                    dict_data['content'] = res_web.content
                    playlist.append(dict_data)
            return res_group, playlist
        except:
            return 'database_error'
        # finally:
        #     db_session.close()
