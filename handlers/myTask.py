#!/usr/bin/env python
# _*_coding:utf-8_*_
import time

import tornado
import tornado.gen

from api.apiWebSocket import ApiDeviceSocketHandler
from handlers.base import BaseHandler
from handlers.basefunction import BaseFunctionHandler
from models.models import MyTask, MyTaskContent


# 任务列表
class MyTaskHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        my_tasks = self.session.query(MyTask).filter(MyTask.company_id == self.get_secure_cookie('company_id')).order_by(MyTask.id.desc()).all()
        self.render("task_list.html", auth_user=self.current_user, my_tasks=my_tasks)


# 任务详细
class MyTaskDetailHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        my_task_id = self.get_argument("my_task_id")
        my_task = self.session.query(MyTask).filter(MyTask.id == my_task_id).first()
        my_task_contents = my_task.my_task_content
        self.render("task_detail.html", auth_user=self.current_user, my_task_contents=my_task_contents)


# 任务列表--删除
class MyTaskDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        my_task_id = self.get_argument("my_task_id")
        my_task = self.session.query(MyTask).filter(MyTask.id == my_task_id).first()
        self.session.delete(my_task)
        self.session.commit()
        self.redirect('/myTask')


# 推送--定时开关机数据
class SendTimeSwitchHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        device_time_switch_id = self.get_argument("device_time_switch_id")
        device_time_switch, week_list = BaseFunctionHandler.get_device_time_switch(self, device_time_switch_id)
        my_task = MyTask(
            name='定时开关机任务',
            type='time_switch',
            time=time.strftime("%Y-%m-%d %H:%M:%S"),
            user_id=self.get_secure_cookie('user_id'),
            company_id=self.get_secure_cookie('company_id'),
        )
        self.session.add(my_task)
        self.session.commit()
        for device_group in device_time_switch.device_group:
            devices = device_group.device
            for device in devices:
                my_task_content = MyTaskContent(
                    device_id=device.device_id,
                    from_user=self.get_secure_cookie('username'),
                    new_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                    send_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                    send_data=str(week_list),
                    my_task_id=my_task.id
                )
                self.session.add(my_task_content)
        self.session.commit()
        ApiDeviceSocketHandler.send_to_many_device(devices, week_list)
        self.redirect('/myTask')


# 推送--资源组数据
class SendPlaylistHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        res_group_id = self.get_argument('res_group_id')
        res_group, playlist = BaseFunctionHandler.get_res_group_by_res_group_id(res_group_id)
        my_task = MyTask(
            name='播放列表任务',
            type='playlist',
            time=time.strftime("%Y-%m-%d %H:%M:%S"),
            user_id=self.get_secure_cookie('user_id'),
            company_id=self.get_secure_cookie('company_id'),
        )
        self.session.add(my_task)
        self.session.commit()
        device_groups = res_group.deviceGroup
        for device_group in device_groups:
            devices = device_group.device
        for device in devices:
            my_task_content = MyTaskContent(
                    device_id=device.device_id,
                    from_user=self.get_secure_cookie('username'),
                    new_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                    send_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                    send_data=str(playlist),
                    my_task_id=my_task.id
            )
            self.session.add(my_task_content)
        self.session.commit()
        ApiDeviceSocketHandler.send_to_many_device(devices, playlist)
        self.redirect('/myTask')


# 推送--设备重启命令
class SendDeviceRestartHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        device_id = self.get_argument('device_id')
        my_task = MyTask(
            name='广告机重启',
            type='deviceRestart',
            time=time.strftime("%Y-%m-%d %H:%M:%S"),
            user_id=self.get_secure_cookie('user_id'),
            company_id=self.get_secure_cookie('company_id'),
        )
        self.session.add(my_task)
        self.session.commit()
        data = [{'cmd': 'deviceRestart'}, {'data': 'restart'}]
        my_task_content = MyTaskContent(
                    device_id=device_id,
                    from_user=self.get_secure_cookie('username'),
                    new_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                    send_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                    send_data=str(data),
                    my_task_id=my_task.id
            )
        self.session.add(my_task_content)
        self.session.commit()
        ApiDeviceSocketHandler.send_to_one_device(device_id, data)
        self.redirect('/myTask')


