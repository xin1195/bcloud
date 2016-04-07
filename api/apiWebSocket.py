#!/usr/bin/env python
# _*_coding:utf-8_*_
import json
import tornado
import tornado.websocket
from handlers.basefunction import BaseFunctionHandler
import logging


# UserSocket接口，用于浏览器通信
class ApiUserSocketHandler(tornado.websocket.WebSocketHandler):
    # 用户集 字典类型 key为username ，value 为 对应的对象
    user_client_map = {}

    @staticmethod
    def send_to_all_user(self, message):
        for i in ApiUserSocketHandler.user_client_map:
            ApiUserSocketHandler.user_client_map[i].write_message(json.dumps(message))

    @staticmethod
    def send_to_one_user(user_client, message):
        user_client.write_message(json.dumps(message))

    @staticmethod
    def send_to_many_user(user_clients, message):
        for user_client in user_clients:
            user_client.write_message(json.dumps(message))

    def open(self):
        pass

    def on_close(self):
        pass

    def on_message(self, message):
        pass

    def on_pong(self, data):
        logging.info("on_pong: " + data)


# DeviceSocket接口，用于与设备通信
class ApiDeviceSocketHandler(tornado.websocket.WebSocketHandler):
    # 用户集 字典类型 key为username ，value 为 对应的对象
    device_client_map = {}

    @staticmethod
    def send_to_all_device(self, message):
        for i in ApiDeviceSocketHandler.device_client_map:
            ApiDeviceSocketHandler.device_client_map[i].write_message(json.dumps(message))
            logging.info('send_to_all_device' + str(message))

    @staticmethod
    def send_to_one_device(device_id, message):
        if ApiDeviceSocketHandler.device_client_map.has_key(device_id):
            ApiDeviceSocketHandler.device_client_map[device_id].write_message(json.dumps(message))
            logging.info('send_to_one_device 推送成功' + str(device_id))
        else:
            logging.info('send_to_many_device 推送失败 不在线' + str(device_id))

    @staticmethod
    def send_to_many_device(device_clients, message):
        for device_client in device_clients:
            device_id = device_client.device_id
            if ApiDeviceSocketHandler.device_client_map.has_key(device_id):
                ApiDeviceSocketHandler.device_client_map[device_id].write_message(json.dumps(message))
                logging.info('send_to_many_device 推送成功' + str(device_id))
            else:
                logging.info('send_to_many_device 推送失败 不在线' + str(device_id))

    # send_success
    @staticmethod
    def send_success(self):
        self.write_message(json.dumps([{
            'cmd': 'connect_success',
        }, {
            'form_user': 'system',
            'data': 'open:connect_success',
        }]))

    # websocke第一次连接是调用
    def open(self):
        device_id = str(self.get_argument("device_id"))
        # 发送成功
        ApiDeviceSocketHandler.send_success(self)
        logging.info("device_id: " + device_id + " : connect_success")
        # 添加设备到设备字典中
        ApiDeviceSocketHandler.device_client_map[device_id] = self
        logging.info("device_client_map: " + str(ApiDeviceSocketHandler.device_client_map))
        # 推送资源组数据
        playlist = BaseFunctionHandler.get_res_group_by_device_id(device_id)
        self.write_message(json.dumps(playlist))
        logging.info(device_id + '播放列表推送成功:' + str(json.dumps(playlist)))
        # 推送定时开关机数据
        time_switch = BaseFunctionHandler.get_time_switch(device_id)
        self.write_message(json.dumps(time_switch))
        logging.info(device_id + '定时开关机推送成功:' + str(json.dumps(time_switch)))

    # 获取websocket 数据时调用
    def on_message(self, message):
        if message == 'heart':
            device_id = str(self.get_argument('device_id'))
            logging.info(device_id + ': 心跳连接正常')
        else:
            key, value = message.split("::")
            if key == 'res_data':
                data_list = value.split("||")
                data_dict = dict()
                # 向服务器注册
                for data in data_list:
                    key1, value1 = data.split("__")
                    data_dict[key1] = value1
                logging.info("before服务器注册" + str(data_dict))
                res = BaseFunctionHandler.device_res(self, data_dict)
                logging.info("after服务器注册" + str(res))
                self.write_message(json.dumps([{
                    'cmd': 'res_data',
                }, {
                    'form_user': 'system',
                    'data': res,
                }]))
            else:
                self.write_message(json.dumps([{
                    'cmd': 'error',
                }, {
                    'form_user': 'system',
                    'data': 'key_error',
                }]))

    # 设备断线时调用
    def on_close(self):
        device_id = str(self.get_argument("device_id"))
        del ApiDeviceSocketHandler.device_client_map[device_id]
        logging.info("device_client_map: " + str(ApiDeviceSocketHandler.device_client_map))
        logging.info("device_id:" + device_id + "on_close")
