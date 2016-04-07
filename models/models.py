#!/usr/bin/env python
# _*_coding:utf-8_*_

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from handlers.base import engine

BaseModel = declarative_base()


# 新建表
def init_db():
    BaseModel.metadata.create_all(engine)


# 删除表
def drop_db():
    BaseModel.metadata.drop_all(engine)


# ---------------------------------------公司----------------------------------------------------

# 多对多 用户组--设备组
userGroup_deviceGroup = Table('userGroup_deviceGroup', BaseModel.metadata,
                              Column('userGroup_id', ForeignKey('userGroup.id'), primary_key=True),
                              Column('deviceGroup_id', ForeignKey('deviceGroup.id'), primary_key=True)
                              )

# 多对多 用户组--资源组
userGroup_resGroup = Table('userGroup_resGroup', BaseModel.metadata,
                           Column('userGroup_id', ForeignKey('userGroup.id'), primary_key=True),
                           Column('resGroup_id', ForeignKey('resGroup.id'), primary_key=True)
                           )


# 公司表
class Company(BaseModel):
    __tablename__ = 'company'

    id = Column(Integer, Sequence('company_id_seq'), primary_key=True)  # id
    code = Column(String(11), unique=True, nullable=True)  # 公司编码
    name = Column(String(32))  # 公司名称
    address = Column(String(64))  # 公司地址
    parent = Column(String(11))  # 公司母公司
    data = Column(DATE)  # 新建时间
    user_group = relationship("UserGroup", backref="company")  # 对应的用户组
    user = relationship("User", backref="company")  # 对应的用户
    devices = relationship("Device", backref="company")  # 对应的设备
    device_time_switch = relationship("DeviceTimeSwitch", backref="company")  # 对应的定时开关机表
    device_week = relationship("DeviceWeek", backref="company")  # 对应的定时开关每周
    device_day = relationship("DeviceDay", backref="company")  # 对应的定时开关机每天
    device_group = relationship("DeviceGroup", backref="company")  # 对应的设备组
    resources_group = relationship("ResGroup", backref="company")  # 对应的资源组
    res_text = relationship("ResText", backref="company")  # 对应的文字资源
    res_image = relationship("ResImage", backref="company")  # 对应的图片资源
    res_video = relationship("ResVideo", backref="company")  # 对应的视频资源
    my_task = relationship("MyTask", backref="company")  # 对应的任务


# ---------------------------------------用户----------------------------------------------------

# 多对多  用户--用户组
user_userGroup = Table('user_userGroup', BaseModel.metadata,
                       Column('user_id', ForeignKey('user.id'), primary_key=True),
                       Column('userGroup_id', ForeignKey('userGroup.id'), primary_key=True)
                       )


# 用户组表
class UserGroup(BaseModel):
    __tablename__ = 'userGroup'

    id = Column(Integer, Sequence('userGroup_id_seq'), primary_key=True)  # id
    name = Column(String(32))  # 用户组名称
    company_id = Column(Integer, ForeignKey('company.id'))  # 外键  公司
    user = relationship('User', secondary=user_userGroup, back_populates='userGroup')
    deviceGroup = relationship('DeviceGroup', secondary=userGroup_deviceGroup, back_populates='userGroup')
    resGroup = relationship('ResGroup', secondary=userGroup_resGroup, back_populates='userGroup')


# 用户表
class User(BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)  # id
    username = Column(String(32))  # 用户名
    password = Column(CHAR(64))  # 密码
    email = Column(String(32))  # 邮箱
    is_active = Column(BOOLEAN)  # 是否激活
    is_admin = Column(BOOLEAN)  # 是否管理员
    data = Column(DATE)  # 新建时间
    tell_phone = Column(CHAR(11))  # 电话号码
    my_task = relationship("MyTask", backref="user")  # 对应的任务
    company_id = Column(Integer, ForeignKey('company.id'))  # 外键  公司
    userGroup = relationship('UserGroup', secondary=user_userGroup, back_populates='user')


# ---------------------------------------设备----------------------------------------------------


# 设备分屏数量
class DeviceScreenNumber(BaseModel):
    __tablename__ = 'deviceScreenNumber'
    id = Column(Integer, Sequence('deviceScreenNumber_id_seq'), primary_key=True)  # id
    name = Column(String(32))  # 设备分屏名称
    value = Column(String(32))  # 设备分屏值


# 设备组表
class DeviceGroup(BaseModel):
    __tablename__ = 'deviceGroup'

    id = Column(Integer, Sequence('deviceGroup_id_seq'), primary_key=True)  # id
    name = Column(String(32))  # 设备组名称
    company_id = Column(Integer, ForeignKey('company.id'))  # 外键  公司
    device_time_switch_id = Column(Integer, ForeignKey('device_timeSwitch.id'))  # 外键  公司
    resGroup_id = Column(Integer, ForeignKey('resGroup.id'))  # 外键  资源组
    device = relationship("Device", backref="deviceGroup")  # 对应设备
    userGroup = relationship('UserGroup', secondary=userGroup_deviceGroup, back_populates='deviceGroup')


# 设备表
class Device(BaseModel):
    __tablename__ = 'device'

    device_id = Column(String(64), primary_key=True)  # 设备id
    device_id_s = Column(CHAR(6))  # 设备预留码
    device_name = Column(String(32))  # 设备名称
    status = Column(String(16))  # 设备状态 是否审核
    ip = Column(String(64))  # 服务器ip
    port = Column(String(6))  # 服务器端口号
    data = Column(DATE)  # 新建时间
    device_audio = Column(String(16))  # 设备音量
    model = Column(String(32))  # 设备型号
    board_model = Column(String(32))  # 主板型号
    screen_size = Column(String(32))  # 屏幕尺寸
    screen_resolution = Column(String(32))  # 屏幕分辨率
    screen_number = Column(String(32))  # 分屏数量
    cpu_model = Column(String(32))  # cpu型号
    cpu_num = Column(String(32))  # cpu数量
    ram_model = Column(String(32))  # 内存型号
    ram_size = Column(String(32))  # 内存大小
    mac_address = Column(String(32))  # mac地址
    power_type = Column(String(32))  # 供电形式 1、电源 2、电池 3、电源+电池
    voltage = Column(String(32))  # 供电电压
    power_consumption = Column(String(32))  # 耗电量
    device_position = Column(String(32))  # 设备安装位置
    is_horn = Column(String(16))  # 是否有喇叭
    device_use = Column(String(32))  # 设备用途
    ad_environment = Column(String(32))  # 广告机安装环境
    manufacturer = Column(String(32))  # 广告机生产商
    company_id = Column(Integer, ForeignKey('company.id'))  # 外键  公司
    deviceGroup_id = Column(Integer, ForeignKey('deviceGroup.id'))  # 外键 设备组


# ---------------------------------------资源----------------------------------------------------

# 多对多  文字资源--资源组
resText_resGroup = Table('resText_resGroup', BaseModel.metadata,
                         Column('resText_id', ForeignKey('resText.id'), primary_key=True),
                         Column('resGroup_id', ForeignKey('resGroup.id'), primary_key=True)
                         )

# 多对多  图片资源--资源组
resImage_resGroup = Table('resImage_resGroup', BaseModel.metadata,
                          Column('resImage_id', ForeignKey('resImage.id'), primary_key=True),
                          Column('resGroup_id', ForeignKey('resGroup.id'), primary_key=True)
                          )

# 多对多  视频资源--资源组
resVideo_resGroup = Table('resVideo_resGroup', BaseModel.metadata,
                          Column('resVideo_id', ForeignKey('resVideo.id'), primary_key=True),
                          Column('resGroup_id', ForeignKey('resGroup.id'), primary_key=True)
                          )

# 多对多  网站资源--资源组
resWeb_resGroup = Table('resWeb_resGroup', BaseModel.metadata,
                        Column('resWeb_id', ForeignKey('resWeb.id'), primary_key=True),
                        Column('resGroup_id', ForeignKey('resGroup.id'), primary_key=True)
                        )


# 资源组表
class ResGroup(BaseModel):
    __tablename__ = 'resGroup'

    id = Column(Integer, Sequence('resGroup_id_seq'), primary_key=True)  # id
    name = Column(String(32))  # 资源组名称
    data = Column(DATE)  # 新建时间
    company_id = Column(Integer, ForeignKey('company.id'))  # 外键  公司
    resText = relationship('ResText', secondary=resText_resGroup, back_populates='resGroup')
    resImage = relationship('ResImage', secondary=resImage_resGroup, back_populates='resGroup')
    resVideo = relationship('ResVideo', secondary=resVideo_resGroup, back_populates='resGroup')
    resWeb = relationship('ResWeb', secondary=resWeb_resGroup, back_populates='resGroup')
    userGroup = relationship('UserGroup', secondary=userGroup_resGroup, back_populates='resGroup')
    deviceGroup = relationship("DeviceGroup", backref="resGroup")  # 对应的设备组


# 文字资源表
class ResText(BaseModel):
    __tablename__ = 'resText'

    id = Column(Integer, Sequence('resText_id_seq'), primary_key=True)  # 资源id
    name = Column(String(32))  # 资源名称
    content = Column(String(255))  # 资源内容
    memo = Column(String(255))  # 资源备注
    data = Column(DATE)  # 资源新建时间
    is_able = Column(String(16))  # 是否审批通过
    company_id = Column(Integer, ForeignKey('company.id'))  # 外键  公司
    resGroup = relationship('ResGroup', secondary=resText_resGroup, back_populates='resText')


# 图片资源表
class ResImage(BaseModel):
    __tablename__ = 'resImage'

    id = Column(Integer, Sequence('resImage_id_seq'), primary_key=True)  # 资源id
    name = Column(String(32))  # 资源名称
    path = Column(String(128))  # 资源路径
    memo = Column(String(255))  # 资源备注
    data = Column(DATE)  # 资源新建时间
    is_able = Column(String(16))  # 是否审批通过
    company_id = Column(Integer, ForeignKey('company.id'))  # 外键  公司
    resGroup = relationship('ResGroup', secondary=resImage_resGroup, back_populates='resImage')


# 视频资源表
class ResVideo(BaseModel):
    __tablename__ = 'resVideo'

    id = Column(Integer, Sequence('resVideo_id_seq'), primary_key=True)  # 资源id
    name = Column(String(32))  # 资源名称
    path = Column(String(128))  # 资源路径
    memo = Column(String(255))  # 资源备注
    data = Column(DATE)  # 资源新建时间
    is_able = Column(String(16))  # 是否审批通过
    company_id = Column(Integer, ForeignKey('company.id'))  # 外键  公司
    resGroup = relationship('ResGroup', secondary=resVideo_resGroup, back_populates='resVideo')


# 网站资源
class ResWeb(BaseModel):
    __tablename__ = 'resWeb'

    id = Column(Integer, Sequence('resWeb_id_seq'), primary_key=True)  # 资源id
    name = Column(String(32))  # 资源名称
    content = Column(String(128))  # 资源内容
    memo = Column(String(255))  # 资源备注
    data = Column(DATE)  # 资源新建时间
    is_able = Column(String(16))  # 是否审批通过
    company_id = Column(Integer, ForeignKey('company.id'))  # 外键  公司
    resGroup = relationship('ResGroup', secondary=resWeb_resGroup, back_populates='resWeb')


# ---------------------------------------定时器表----------------------------------------------------

# 定时开关机表
class DeviceTimeSwitch(BaseModel):
    __tablename__ = 'device_timeSwitch'

    id = Column(Integer, Sequence('device_timeSwitch_id_seq'), primary_key=True)  # id
    name = Column(String(32))  # 名称
    company_id = Column(Integer, ForeignKey('company.id'))  # 外键  公司
    device_week = relationship("DeviceWeek", backref="device_timeSwitch", cascade="delete, delete-orphan", single_parent=True)  # 对应的定时开关每周
    device_group = relationship("DeviceGroup", backref="device_timeSwitch")  # 对应的设备组


# 定时开关机--周(单位/天)
class DeviceWeek(BaseModel):
    __tablename__ = 'device_week'

    id = Column(Integer, Sequence('device_week_id_seq'), primary_key=True)  # id
    name = Column(String(32))  # 资源名称
    device_timeSwitch_id = Column(Integer, ForeignKey('device_timeSwitch.id'))  # 外键  定时开关机表
    company_id = Column(Integer, ForeignKey('company.id'))  # 外键  公司
    device_day = relationship("DeviceDay", backref="device_week", cascade="delete, delete-orphan", single_parent=True)  # 对应的定时开关机每天


# 定时开关机--天(单位/小时)
class DeviceDay(BaseModel):
    __tablename__ = 'device_day'

    id = Column(Integer, Sequence('device_day_id_seq'), primary_key=True)  # id
    name = Column(String(32))  # 资源名称
    time = Column(Time)  # 时间
    screen = Column(String(32))  # 设备屏幕 开，关
    device_week_id = Column(Integer, ForeignKey('device_week.id'))  # 外键   定时开关机--周
    company_id = Column(Integer, ForeignKey('company.id'))  # 外键  公司


# 任务
class MyTask(BaseModel):
    __tablename__ = 'my_task'

    id = Column(Integer, Sequence('my_task_id_seq'), primary_key=True)  # id
    name = Column(String(32))  # 任务名称
    time = Column(DateTime)  # 时间
    type = Column(String(16))  # 任务类型
    user_id = Column(Integer, ForeignKey('user.id'))  # 外键 用户
    company_id = Column(Integer, ForeignKey('company.id'))  # 外键 公司
    my_task_content = relationship("MyTaskContent", backref="my_task", cascade="delete, delete-orphan", single_parent=True)  # 对应的任务内容


# 任务内容
class MyTaskContent(BaseModel):
    __tablename__ = 'my_task_content'

    id = Column(Integer, Sequence('my_task_content_id_seq'), primary_key=True)  # id
    device_id = Column(String(64))  # 设备id
    from_user = Column(String(32))  # 用户名
    memo = Column(String(255))  # 备注
    new_time = Column(DateTime)  # 新建时间
    send_time = Column(DateTime)  # 发送时间
    send_data = Column(Text)  # 发送的数据
    request_data = Column(Text)  # 返回的数据
    request_time = Column(DateTime)  # 返回的时间
    my_task_id = Column(Integer, ForeignKey('my_task.id'))  # 外键 任务

# drop_db()
# init_db()
