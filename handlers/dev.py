#!/usr/bin/env python
# _*_coding:utf-8_*_
import tornado
import tornado.auth
import tornado.web
import time

from api.apiWebSocket import ApiDeviceSocketHandler
from handlers.base import BaseHandler
from models.models import Device, DeviceGroup, DeviceTimeSwitch, DeviceWeek, DeviceDay, ResGroup, MyTask, MyTaskContent, DeviceScreenNumber


# 设备管理
class DeviceManageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        devices = self.session.query(Device).filter(Device.company_id == self.get_secure_cookie('company_id')).all()
        self.render("dev_manage.html", auth_user=self.current_user, devices=devices)


# 设备管理--通过device_id获取设备详细信息
class DeviceManageDetailHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        device_id = self.get_argument("device_id")
        err = ''
        device = self.session.query(Device).filter(Device.device_id == device_id).first()
        device_groups = self.session.query(DeviceGroup).filter(DeviceGroup.company_id == self.get_secure_cookie('company_id')).all()
        device_screen_numbers = self.session.query(DeviceScreenNumber).filter().all()
        self.render("dev_manage_detail.html", auth_user=self.current_user, device=device, device_groups=device_groups, device_screen_numbers=device_screen_numbers, err=err)

    @tornado.web.authenticated
    def post(self):
        device_id = self.get_argument('device_id')
        device_name = self.get_argument("device_name")
        ip = self.get_argument("ip")
        device_position = self.get_argument("device_position")
        port = self.get_argument("port")
        device_use = self.get_argument("device_use")
        device_audio = self.get_argument("device_audio")
        screen_number = self.get_argument("screen_number")
        ad_environment = self.get_argument("ad_environment")
        device_group_id = self.get_argument('deviceGroup_id')
        try:
            device = Device(
                    device_id=device_id,
                    device_name=device_name,
                    ip=ip,
                    device_position=device_position,
                    port=port,
                    device_audio=device_audio,
                    screen_number=screen_number,
                    device_use=device_use,
                    ad_environment=ad_environment,
                    deviceGroup_id=device_group_id,
            )
            self.session.merge(device)
            self.session.commit()
            # 新建任务
            my_task = MyTask(
                name='设备信息任务',
                type='device',
                time=time.strftime("%Y-%m-%d %H:%M:%S"),
                user_id=self.get_secure_cookie('user_id'),
                company_id=self.get_secure_cookie('company_id'),
            )
            self.session.add(my_task)
            self.session.commit()
            # 新建任务内容
            data_list = list()
            data_dict = dict()
            data_dict['cmd'] = 'device'
            data_list.append(data_dict)
            data_dict = dict()
            data_dict['device_audio'] = device_audio
            data_dict['screen_number'] = screen_number
            data_list.append(data_dict)
            my_task_content = MyTaskContent(
                device_id=device.device_id,
                from_user=self.get_secure_cookie('username'),
                new_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                send_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                send_data=str(data_list),
                my_task_id=my_task.id
            )
            self.session.add(my_task_content)
            self.session.commit()
            ApiDeviceSocketHandler.send_to_one_device(device_id, data_list)
            self.redirect('/dev/group?device_group_id='+device_group_id)
        except:
            err = '修改失败'
            device = self.session.query(Device).filter(Device.device_id == device_id).first()
            self.render("dev_manage_detail.html", auth_user=self.current_user, device=device, err=err)


# 设备组管理
class DeviceGroupHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        company_id = self.get_secure_cookie('company_id')
        device_group_id = self.get_argument('device_group_id')
        device_groups = self.session.query(DeviceGroup).filter(DeviceGroup.company_id == company_id).all()
        if device_group_id == '':
            device_group = self.session.query(DeviceGroup).filter(DeviceGroup.company_id == company_id).first()
            if device_group:
                device_group_id = device_group.id
                devices = self.session.query(Device).filter(Device.deviceGroup_id == device_group_id).all()
            else:
                devices = ''
        else:
            devices = self.session.query(Device).filter(Device.deviceGroup_id == device_group_id).all()
        self.render("dev_group.html", auth_user=self.current_user, device_groups=device_groups, devices=devices)


# 设备组管理--新增
class DeviceGroupAddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        msg = ''
        action = '/dev/group/add'
        device_group = DeviceGroup()
        res_groups = self.session.query(ResGroup).filter(ResGroup.company_id == self.get_secure_cookie('company_id')).all()
        device_time_switches = self.session.query(DeviceTimeSwitch).filter(DeviceTimeSwitch.company_id == self.get_secure_cookie('company_id')).all()
        self.render("dev_group_add.html", auth_user=self.current_user, action=action, device_group=device_group, res_groups=res_groups, device_time_switches=device_time_switches,  msg=msg)

    @tornado.web.authenticated
    def post(self):
        name = self.get_argument('name')
        res_group_id = self.get_argument('res_group_id')
        device_time_switch_id = self.get_argument('device_time_switch_id')
        try:
            device_group = DeviceGroup(
                name=name,
                resGroup_id=res_group_id,
                device_time_switch_id=device_time_switch_id,
                company_id=self.get_secure_cookie('company_id'),
            )
            self.session.add(device_group)
            self.session.commit()
            self.redirect('/dev/group?device_group_id=')
        except:
            msg = '设备组新增失败'
            action = '/dev/group/add'
            device_group = DeviceGroup()
            self.render("dev_group_add.html", auth_user=self.current_user, action=action, device_group=device_group, msg=msg)


# 设备组管理--修改名称
class DeviceGroupUpdateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        msg = ''
        action = '/dev/group/update'
        device_group_id = self.get_argument('device_group_id')
        device_group = self.session.query(DeviceGroup).filter(DeviceGroup.id == device_group_id).first()
        res_groups = self.session.query(ResGroup).filter(ResGroup.company_id == self.get_secure_cookie('company_id')).all()
        device_time_switches = self.session.query(DeviceTimeSwitch).filter(DeviceTimeSwitch.company_id == self.get_secure_cookie('company_id')).all()
        self.render("dev_group_add.html", auth_user=self.current_user, action=action, device_group=device_group, res_groups=res_groups, device_time_switches=device_time_switches, msg=msg)

    @tornado.web.authenticated
    def post(self):
        device_group_id = self.get_argument('device_group_id')
        res_group_id = self.get_argument('res_group_id')
        device_time_switch_id = self.get_argument('device_time_switch_id')
        name = self.get_argument('name')
        device_group = DeviceGroup(
            id=device_group_id,
            name=name,
            resGroup_id=res_group_id,
            device_time_switch_id=device_time_switch_id,
        )
        self.session.merge(device_group)
        self.session.commit()
        self.redirect('/dev/group?device_group_id='+device_group_id)


# 设备组管理--删除
class DeviceGroupDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        device_group_id = self.get_argument('device_group_id')
        device_group = self.session.query(DeviceGroup).filter(DeviceGroup.id == device_group_id).first()
        self.session.delete(device_group)
        self.session.commit()
        self.redirect('/dev/group?device_group_id=')


# 定时开关机
class DeviceTimeSwitchHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        device_time_switch_id = self.get_argument('device_time_switch_id')
        device_time_switches = self.session.query(DeviceTimeSwitch).filter(DeviceTimeSwitch.company_id == self.get_secure_cookie('company_id')).all()
        if device_time_switch_id == '':
            device_time_switch = self.session.query(DeviceTimeSwitch).filter(DeviceTimeSwitch.company_id == self.get_secure_cookie('company_id')).first()
        else:
            device_time_switch = self.session.query(DeviceTimeSwitch).filter(DeviceTimeSwitch.id == device_time_switch_id).first()
        if device_time_switch:
            device_weeks = device_time_switch.device_week
        else:
            device_weeks = ''
        self.render("dev_timeSwitch.html", auth_user=self.current_user, device_time_switches=device_time_switches, device_weeks=device_weeks)


# 定时开关机--新增
class DeviceTimeSwitchAddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        action = '/dev/timeSwitch/add'
        device_time_switch = DeviceTimeSwitch()
        self.render("dev_timeSwitch_add.html", auth_user=self.current_user, action=action, device_time_switch=device_time_switch)

    @tornado.web.authenticated
    def post(self):
        name = self.get_argument('name')
        company_id = self.get_secure_cookie('company_id')
        weeks = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        device_time_switch = DeviceTimeSwitch(
            name=name,
            company_id=company_id,
        )
        self.session.add(device_time_switch)
        self.session.commit()
        for week in weeks:
            device_week = DeviceWeek(
                name=week,
                company_id=company_id,
                device_timeSwitch_id=device_time_switch.id
            )
            self.session.add(device_week)
        self.session.commit()
        self.redirect('/dev/timeSwitch?device_time_switch_id=')


# 定时开关机--修改
class DeviceTimeSwitchUpdateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        action = '/dev/timeSwitch/update'
        device_time_switch_id = self.get_argument('device_time_switch_id')
        device_time_switch = self.session.query(DeviceTimeSwitch).filter(DeviceTimeSwitch.id == device_time_switch_id).first()
        self.render("dev_timeSwitch_add.html", auth_user=self.current_user, action=action, device_time_switch=device_time_switch)

    @tornado.web.authenticated
    def post(self):
        device_time_switch_id = self.get_argument('device_time_switch_id')
        name = self.get_argument('name')
        device_time_switch = DeviceTimeSwitch(
            id=device_time_switch_id,
            name=name,
        )
        self.session.merge(device_time_switch)
        self.session.commit()
        self.redirect('/dev/timeSwitch?device_time_switch_id='+device_time_switch_id)


# 定时开关机--删除
class DeviceTimeSwitchDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        device_time_switch_id = self.get_argument('device_time_switch_id')
        device_time_switch = self.session.query(DeviceTimeSwitch).filter(DeviceTimeSwitch.id == device_time_switch_id).first()
        self.session.delete(device_time_switch)
        self.session.commit()
        self.redirect('/dev/timeSwitch?device_time_switch_id=')


# 定时控制--新增
class DeviceDayAddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        action = '/dev/day/add'
        device_week_id = self.get_argument('device_week_id')
        device_week = self.session.query(DeviceWeek).filter(DeviceWeek.id == device_week_id).first()
        device_time_switch_id = str(device_week.device_timeSwitch_id)
        device_day = DeviceDay()
        time_list = ['0', '0']
        self.render("dev_day_add.html", auth_user=self.current_user, action=action, device_day=device_day, device_time_switch_id=device_time_switch_id, device_week_id=device_week_id, time_list=time_list)

    @tornado.web.authenticated
    def post(self):
        device_time_switch_id = self.get_argument('device_time_switch_id')
        name = self.get_argument('name')
        hour = self.get_argument('hour')
        screen = self.get_argument('screen')
        second = self.get_argument('second')
        time = hour + ':' + second + ':00'
        company_id = self.get_secure_cookie('company_id')
        device_week_id = self.get_argument('device_week_id')
        device_day = DeviceDay(
            name=name,
            time=time,
            screen=screen,
            device_week_id=device_week_id,
            company_id=company_id,
        )
        self.session.add(device_day)
        self.session.commit()
        self.redirect('/dev/timeSwitch?device_time_switch_id='+device_time_switch_id)


# 定时控制--修改
class DeviceDayUpdateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        action = '/dev/day/update'
        device_day_id = self.get_argument('device_day_id')
        device_week_id = self.get_argument('device_week_id')
        device_week = self.session.query(DeviceWeek).filter(DeviceWeek.id == device_week_id).first()
        device_time_switch_id = str(device_week.device_timeSwitch_id)
        device_day = self.session.query(DeviceDay).filter(DeviceDay.id == device_day_id).first()
        time_list = str(device_day.time).split(':')
        self.render("dev_day_add.html", auth_user=self.current_user, action=action, device_day=device_day, device_time_switch_id=device_time_switch_id, device_week_id=device_week_id, time_list=time_list)

    @tornado.web.authenticated
    def post(self):
        device_time_switch_id = self.get_argument('device_time_switch_id')
        id = self.get_argument('id')
        name = self.get_argument('name')
        hour = self.get_argument('hour')
        screen = self.get_argument('screen')
        second = self.get_argument('second')
        time = hour + ':' + second + ':00'
        device_day = DeviceDay(
            id=id,
            name=name,
            time=time,
            screen=screen,
        )
        self.session.merge(device_day)
        self.session.commit()
        self.redirect('/dev/timeSwitch?device_time_switch_id='+device_time_switch_id)


# 定时控制--删除
class DeviceDayDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        device_day_id = self.get_argument('device_day_id')
        device_week_id = self.get_argument('device_week_id')
        device_week = self.session.query(DeviceWeek).filter(DeviceWeek.id == device_week_id).first()
        device_time_switch_id = str(device_week.device_timeSwitch_id)
        device_day = self.session.query(DeviceDay).filter(DeviceDay.id == device_day_id).first()
        self.session.delete(device_day)
        self.session.commit()
        self.redirect('/dev/timeSwitch?device_time_switch_id='+device_time_switch_id)


