#!/usr/bin/python
# _*_coding:utf-8_*_
from api.api import ApiUserHandler, ApiScreenNumber, ApiDeviceRegister
from api.apiWebSocket import ApiUserSocketHandler, ApiDeviceSocketHandler
from handlers.dev import DeviceManageHandler, DeviceManageDetailHandler, DeviceGroupHandler, DeviceGroupAddHandler, DeviceGroupDeleteHandler, DeviceGroupUpdateHandler, DeviceTimeSwitchHandler, DeviceTimeSwitchAddHandler, DeviceTimeSwitchUpdateHandler, DeviceTimeSwitchDeleteHandler, \
    DeviceDayAddHandler, DeviceDayUpdateHandler, DeviceDayDeleteHandler
from handlers.fra import CompanyHandler, CompanyAddHandler, CompanyDeteleHandler, CompanyUpdateHandler, UserHandler, UserAddHandler, UserUpdateHandler, UserDeleteHandler
from handlers.login import LoginHandler, LogoutHandler
from handlers.myTask import MyTaskHandler, MyTaskDeleteHandler, MyTaskDetailHandler, SendTimeSwitchHandler, SendPlaylistHandler, SendDeviceRestartHandler
from handlers.res import ResHandler, ResTextHandler, ResTextDetailHandler, ResTextAddHandler, ResTextDeleteHandler, ResWebHandler, ResWebDetailHandler, ResWebAddHandler, ResWebDeleteHandler, ResImageHandler, ResImageDetailHandler, ResImageDeleteHandler, ResImageAddHandler, ResVideoHandler, \
    ResVideoDetailHandler, ResVideoDeleteHandler, ResVideoAddHandler, ResGroupHandler, ResGroupAddHandler, ResGroupUpdateHandler, ResGroupDeleteHandler, ResGroupAddTextHandler, ResGroupDeleteTextHandler, ResGroupAddWebHandler, ResGroupDeleteWebHandler, ResGroupAddImageHandler, \
    ResGroupDeleteImageHandler, ResGroupAddVideoHandler, ResGroupDeleteVideoHandler


urls = [
    # (r"/", IndexHandler),
    (r"/", DeviceManageHandler),
    (r"/api/user", ApiUserHandler),
    (r"/api/screen", ApiScreenNumber),
    (r"/api/deviceRegister", ApiDeviceRegister),
    (r"/api/userSocket", ApiUserSocketHandler),
    (r"/api/deviceSocket", ApiDeviceSocketHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/fra", CompanyHandler),
    [r"/fra/com", CompanyHandler],
    (r"/fra/com/add", CompanyAddHandler),
    (r"/fra/com/update", CompanyUpdateHandler),
    (r"/fra/com/delete", CompanyDeteleHandler),
    (r"/fra/user", UserHandler),
    (r"/fra/user/add", UserAddHandler),
    (r"/fra/user/update", UserUpdateHandler),
    (r"/fra/user/delete", UserDeleteHandler),
    (r"/dev", DeviceManageHandler),
    (r"/dev/manage", DeviceManageHandler),
    (r"/dev/manage/detail", DeviceManageDetailHandler),
    (r"/dev/group", DeviceGroupHandler),
    (r"/dev/group/add", DeviceGroupAddHandler),
    (r"/dev/group/delete", DeviceGroupDeleteHandler),
    (r"/dev/group/update", DeviceGroupUpdateHandler),
    (r"/dev/timeSwitch", DeviceTimeSwitchHandler),
    (r"/dev/timeSwitch/add", DeviceTimeSwitchAddHandler),
    (r"/dev/timeSwitch/update", DeviceTimeSwitchUpdateHandler),
    (r"/dev/timeSwitch/delete", DeviceTimeSwitchDeleteHandler),
    (r"/dev/day/add", DeviceDayAddHandler),
    (r"/dev/day/update", DeviceDayUpdateHandler),
    (r"/dev/day/delete", DeviceDayDeleteHandler),
    (r"/res", ResHandler),
    (r"/res/text", ResTextHandler),
    (r"/res/text/detail", ResTextDetailHandler),
    (r"/res/text/add", ResTextAddHandler),
    (r"/res/text/delete", ResTextDeleteHandler),
    (r"/res/web", ResWebHandler),
    (r"/res/web/detail", ResWebDetailHandler),
    (r"/res/web/add", ResWebAddHandler),
    (r"/res/web/delete", ResWebDeleteHandler),
    (r"/res/image", ResImageHandler),
    (r"/res/image/detail", ResImageDetailHandler),
    (r"/res/image/delete", ResImageDeleteHandler),
    (r"/res/image/add", ResImageAddHandler),
    (r"/res/video", ResVideoHandler),
    (r"/res/video/detail", ResVideoDetailHandler),
    (r"/res/video/delete", ResVideoDeleteHandler),
    (r"/res/video/add", ResVideoAddHandler),
    (r"/res/group", ResGroupHandler),
    (r"/res/group/add", ResGroupAddHandler),
    (r"/res/group/update", ResGroupUpdateHandler),
    (r"/res/group/delete", ResGroupDeleteHandler),
    (r"/res/group/add/text", ResGroupAddTextHandler),
    (r"/res/group/delete/text", ResGroupDeleteTextHandler),
    (r"/res/group/add/web", ResGroupAddWebHandler),
    (r"/res/group/delete/web", ResGroupDeleteWebHandler),
    (r"/res/group/add/image", ResGroupAddImageHandler),
    (r"/res/group/delete/image", ResGroupDeleteImageHandler),
    (r"/res/group/add/video", ResGroupAddVideoHandler),
    (r"/res/group/delete/video", ResGroupDeleteVideoHandler),
    (r"/myTask", MyTaskHandler),
    (r"/myTask/delete", MyTaskDeleteHandler),
    (r"/myTask/detail", MyTaskDetailHandler),
    (r"/myTask/send_time_switch", SendTimeSwitchHandler),
    (r"/myTask/send_playlist", SendPlaylistHandler),
    (r"/myTask/deviceRestart", SendDeviceRestartHandler),
]
