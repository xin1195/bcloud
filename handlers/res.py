#!/usr/bin/env python
# _*_coding:utf-8_*_
import os
import time

import tornado
import tornado.auth
import tornado.web
from handlers.base import BaseHandler
from models.models import ResText, ResImage, ResVideo, ResGroup, ResWeb


# 资源
class ResHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.redirect('/res/group?res_group_id=')


# 文字资源
class ResTextHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # page_now = self.get_argument('page_now')
        # page_size = PAGESIZE
        # text_resources = self.session.query(ResText).filter(ResText.company_id == self.get_secure_cookie('company_id')).all()[1:10]
        text_resources = self.session.query(ResText).filter(ResText.company_id == self.get_secure_cookie('company_id')).order_by(ResText.id.desc()).all()
        self.render("res_text.html", auth_user=self.current_user, text_resources=text_resources)


# 文字资源--详细
class ResTextDetailHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        action = '/res/text/detail'
        err = ""
        text_id = self.get_argument("id")
        text_resource = self.session.query(ResText).filter(ResText.id == text_id).first()
        self.render("res_text_detail.html", auth_user=self.current_user, action=action, text_resource=text_resource, err=err)

    def post(self):
        id = self.get_argument("id")
        name = self.get_argument("name")
        content = self.get_argument("content")
        memo = self.get_argument("memo")
        text_resource = ResText(
                id=id,
                name=name,
                content=content,
                memo=memo
        )
        try:
            self.session.merge(text_resource)
            self.session.commit()
            self.redirect('/res/text')
        except:
            err = "资源修改失败"
            text_resource = self.session.query(ResText).filter(ResText.id == id).first()
            self.render("res_text_detail.html", auth_user=self.current_user, text_resource=text_resource, err=err)


# 文字资源--新增
class ResTextAddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        action = '/res/text/add'
        err = ''
        text_resource = ResText()
        self.render("res_text_detail.html", auth_user=self.current_user, action=action, text_resource=text_resource, err=err)

    @tornado.web.authenticated
    def post(self):
        text_name = self.get_argument("name")
        text_content = self.get_argument("content")
        memo = self.get_argument("memo")
        text_resource = ResText(
                name=text_name,
                content=text_content,
                memo=memo,
                data=time.strftime("%Y-%m-%d"),
                company_id=self.get_secure_cookie('company_id')
        )
        try:
            self.session.add(text_resource)
            self.session.commit()
            self.redirect('/res/text')
        except:
            action = '/res/text/add'
            err = "资源新增失败"
            text_resource = ''
            self.render("res_text_detail.html", auth_user=self.current_user, action=action, text_resource=text_resource, err=err)


# 文字资源-删除
class ResTextDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id")
        text_resource = self.session.query(ResText).filter(ResText.id == id).first()
        self.session.delete(text_resource)
        self.session.commit()
        self.redirect('/res/text')


# 网站资源
class ResWebHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # page_now = self.get_argument('page_now')
        # page_size = PAGESIZE
        # text_resources = self.session.query(ResText).filter(ResText.company_id == self.get_secure_cookie('company_id')).all()[1:10]
        web_resources = self.session.query(ResWeb).filter(ResWeb.company_id == self.get_secure_cookie('company_id')).order_by(ResWeb.id.desc()).all()
        self.render("res_web.html", auth_user=self.current_user, web_resources=web_resources)


# 网站资源--详细
class ResWebDetailHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        action = '/res/web/detail'
        err = ""
        web_id = self.get_argument("id")
        web_resource = self.session.query(ResWeb).filter(ResWeb.id == web_id).first()
        self.render("res_web_detail.html", auth_user=self.current_user, action=action, web_resource=web_resource, err=err)

    def post(self):
        id = self.get_argument("id")
        name = self.get_argument("name")
        content = self.get_argument("content")
        memo = self.get_argument("memo")
        web_resource = ResWeb(
                id=id,
                name=name,
                content=content,
                memo=memo
        )
        try:
            self.session.merge(web_resource)
            self.session.commit()
            self.redirect('/res/web')
        except:
            err = "资源修改失败"
            web_resource = self.session.query(ResWeb).filter(ResWeb.id == id).first()
            self.render("res_web_detail.html", auth_user=self.current_user, web_resource=web_resource, err=err)


# 网站资源--新增
class ResWebAddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        action = '/res/web/add'
        err = ''
        web_resource = ResWeb()
        self.render("res_web_detail.html", auth_user=self.current_user, action=action, web_resource=web_resource, err=err)

    @tornado.web.authenticated
    def post(self):
        web_name = self.get_argument("name")
        web_content = self.get_argument("content")
        memo = self.get_argument("memo")
        web_resource = ResWeb(
                name=web_name,
                content=web_content,
                memo=memo,
                data=time.strftime("%Y-%m-%d"),
                company_id=self.get_secure_cookie('company_id')
        )
        try:
            self.session.add(web_resource)
            self.session.commit()
            self.redirect('/res/web')
        except:
            action = '/res/web/add'
            err = "资源新增失败"
            web_resource = ''
            self.render("res_web_detail.html", auth_user=self.current_user, action=action, web_resource=web_resource, err=err)


# 网站资源-删除
class ResWebDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id")
        web_resource = self.session.query(ResWeb).filter(ResWeb.id == id).first()
        self.session.delete(web_resource)
        self.session.commit()
        self.redirect('/res/web')


# 图片资源
class ResImageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        image_resources = self.session.query(ResImage).filter(ResImage.company_id == self.get_secure_cookie('company_id')).order_by(ResImage.id.desc()).all()
        self.render("res_image.html", auth_user=self.current_user, image_resources=image_resources)


# 图片资源-新增（图片上传）
class ResImageAddHandler(BaseHandler):

    def check_xsrf_cookie(self):
        pass

    @tornado.web.authenticated
    def get(self):
        self.render("res_image_add.html", auth_user=self.current_user)

    @tornado.web.authenticated
    def post(self):
        username = self.get_secure_cookie("username")
        company_id = self.get_secure_cookie('company_id')
        data = time.strftime("%Y%m%d")
        upload_path = '/media/image/' + username + '/' + data
        if not os.path.isdir(upload_path):
            os.makedirs(upload_path)
        # 提取表单中‘name’为‘file’的文件元数据
        file_metas = self.request.files['file']
        for meta in file_metas:
            filename = meta['filename']
            filepath = os.path.join(upload_path, filename)
            # 有些文件需要已二进制的形式存储，实际中可以更改
            with open(filepath, 'wb') as up:
                up.write(meta['body'])
            img_resources = ResImage()
            img_resources.name = filename
            img_resources.memo = filename
            img_resources.path = filepath
            img_resources.company_id = company_id
            img_resources.data = data
            self.session.add(img_resources)
        self.session.commit()
        json_data = dict()
        json_data['uploaded_file_path'] = filepath
        self.write(json_data)


# 图片资源-详细（修改）
class ResImageDetailHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        action = '/res/image/detail'
        err = ""
        image_id = self.get_argument("id")
        image_resource = self.session.query(ResImage).filter(ResImage.id == image_id).first()
        self.render("res_image_detail.html", auth_user=self.current_user, action=action, image_resource=image_resource, err=err)

    @tornado.web.authenticated
    def post(self):
        image_id = self.get_argument("id")
        name = self.get_argument("name")
        memo = self.get_argument("memo")
        image_resource = ResImage(
                id=image_id,
                name=name,
                memo=memo
        )
        try:
            self.session.merge(image_resource)
            self.session.commit()
            self.redirect('/res/image')
        except:
            err = "图片修改失败"
            image_resource = self.session.query(ResImage).filter(ResImage.id == image_id).first()
            self.render("res_image_detail.html", auth_user=self.current_user, image_resource=image_resource, err=err)


# 图片资源-删除
class ResImageDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        image_id = self.get_argument("id")
        image_resource = self.session.query(ResImage).filter(ResImage.id == image_id).first()
        if os.path.exists(image_resource.path):
            os.remove(image_resource.path)
        self.session.delete(image_resource)
        self.session.commit()
        self.redirect('/res/image')


# 视频资源
class ResVideoHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        video_resources = self.session.query(ResVideo).filter(ResVideo.company_id == self.get_secure_cookie('company_id')).order_by(ResVideo.id.desc()).all()
        self.render("res_video.html", auth_user=self.current_user, video_resources=video_resources)


# 视频资源-新增（视频上传）
class ResVideoAddHandler(BaseHandler):

    def check_xsrf_cookie(self):
        pass

    @tornado.web.authenticated
    def get(self):
        self.render("res_video_add.html", auth_user=self.current_user)

    @tornado.web.authenticated
    def post(self):
        username = self.get_secure_cookie("username")
        company_id = self.get_secure_cookie('company_id')
        data = time.strftime("%Y%m%d")
        upload_path = '/media/video/' + username + '/' + data
        if not os.path.isdir(upload_path):
            os.makedirs(upload_path)
        # 提取表单中‘name’为‘file’的文件元数据
        file_metas = self.request.files['video_file']
        for meta in file_metas:
            filename = meta['filename']
            filepath = os.path.join(upload_path, filename)
            # 有些文件需要已二进制的形式存储，实际中可以更改
            with open(filepath, 'wb') as up:
                up.write(meta['body'])
            video_resources = ResVideo()
            video_resources.name = filename
            video_resources.memo = filename
            video_resources.path = filepath
            video_resources.company_id = company_id
            video_resources.data = data
            self.session.add(video_resources)
        self.session.commit()
        json_data = dict()
        json_data['uploaded_file_path'] = filepath
        self.write(json_data)


# 视频资源-详细（修改）
class ResVideoDetailHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        action = '/res/video/detail'
        err = ""
        video_id = self.get_argument("id")
        video_resource = self.session.query(ResVideo).filter(ResVideo.id == video_id).first()
        self.render("res_video_detail.html", auth_user=self.current_user, action=action, video_resource=video_resource, err=err)

    @tornado.web.authenticated
    def post(self):
        video_id = self.get_argument("id")
        name = self.get_argument("name")
        memo = self.get_argument("memo")
        video_resource = ResVideo(
                id=video_id,
                name=name,
                memo=memo
        )
        try:
            self.session.merge(video_resource)
            self.session.commit()
            self.redirect('/res/video')
        except:
            err = "视频修改失败"
            video_resource = self.session.query(ResVideo).filter(ResVideo.id == video_id).first()
            self.render("res_video_detail.html", auth_user=self.current_user, video_resource=video_resource, err=err)


# 视频资源-删除
class ResVideoDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        video_id = self.get_argument("id")
        video_resource = self.session.query(ResVideo).filter(ResVideo.id == video_id).first()
        if os.path.exists(video_resource.path):
            os.remove(video_resource.path)
        self.session.delete(video_resource)
        self.session.commit()
        self.redirect('/res/video')


# 资源组管理
class ResGroupHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        res_group_id = self.get_argument('res_group_id')
        res_groups = self.session.query(ResGroup).filter(ResGroup.company_id == self.get_secure_cookie('company_id')).all()
        if res_groups:
            if res_group_id == '':
                res_group = self.session.query(ResGroup).filter().first()
            else:
                res_group = self.session.query(ResGroup).filter(ResGroup.id == res_group_id).first()
            res_texts = res_group.resText
            res_webs = res_group.resWeb
            res_images = res_group.resImage
            res_videos = res_group.resVideo
            self.render("res_group.html", auth_user=self.current_user, hand_res_group=res_group, res_groups=res_groups, res_texts=res_texts, res_webs=res_webs, res_images=res_images, res_videos=res_videos)
        else:
            self.redirect('/res/group/add')


# 资源组管理--新增资源组
class ResGroupAddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        err = ''
        action = '/res/group/add'
        res_group = ResGroup()
        self.render("res_group_detail.html", auth_user=self.current_user, action=action, res_group=res_group, err=err)

    @tornado.web.authenticated
    def post(self):
        action = '/res/group/add'
        name = self.get_argument('name')
        res_group = self.session.query(ResGroup).filter(ResGroup.name == name).first()
        if res_group:
            err = "资源组名称已经存在"
            res_group = ResGroup()
            self.render("res_group_detail.html", auth_user=self.current_user, action=action, res_group=res_group, err=err)
        else:
            res_group = ResGroup(
                    name=name,
                    data=time.strftime("%Y-%m-%d"),
                    company_id=self.get_secure_cookie('company_id')
            )
            try:
                self.session.add(res_group)
                self.session.commit()
                self.redirect('/res/group?res_group_id=')
            except:
                err = "资源组新增失败"
                res_group = ResGroup()
                self.render("res_group_detail.html", auth_user=self.current_user, action=action, res_group=res_group, err=err)


# 资源组管理--修改资源组名称
class ResGroupUpdateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        err = ''
        action = '/res/group/update'
        res_group_id = self.get_argument('res_group_id')
        res_group = self.session.query(ResGroup).filter(ResGroup.id == res_group_id).first()
        self.render("res_group_detail.html", auth_user=self.current_user, action=action, res_group=res_group, err=err)

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument('id')
        name = self.get_argument('name')
        res_group = self.session.query(ResGroup).filter(ResGroup.id == id).first()
        res_group.name = name
        self.session.merge(res_group)
        self.session.commit()
        self.redirect('/res/group?res_group_id=')


# 资源组管理--删除资源组名称
class ResGroupDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        res_group_id = self.get_argument('res_group_id')
        res_group = self.session.query(ResGroup).filter(ResGroup.id == res_group_id).first()
        self.session.delete(res_group)
        self.session.commit()
        self.redirect('/res/group?res_group_id=')


# 资源组管理--添加文字资源
class ResGroupAddTextHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        err = ''
        res_group_id = self.get_argument('res_group_id')
        res_texts = self.session.query(ResText).filter(ResText.company_id == self.get_secure_cookie('company_id')).all()
        self.render("res_group_add_text.html", auth_user=self.current_user, res_group_id=res_group_id, res_texts=res_texts, err=err)

    @tornado.web.authenticated
    def post(self):
        res_group_id = self.get_argument('res_group_id')
        res_text_ids = self.get_arguments('res_text_ids')
        res_group = self.session.query(ResGroup).filter(ResGroup.id == res_group_id).first()
        for res_text_id in res_text_ids:
            res_text = self.session.query(ResText).filter(ResText.id == res_text_id).first()
            res_group.resText.append(res_text)
        self.session.commit()
        self.redirect('/res/group?res_group_id=' + res_group_id)


# 资源组管理--删除文字资源
class ResGroupDeleteTextHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        res_text_id = self.get_argument('res_text_id')
        res_group_id = self.get_argument('res_group_id')
        res_text = self.session.query(ResText).filter(ResText.id == res_text_id).first()
        res_group = self.session.query(ResGroup).filter(ResGroup.id == res_group_id).first()
        res_group.resText.remove(res_text)
        self.session.commit()
        self.redirect('/res/group?res_group_id=' + res_group_id)


# 资源组管理--添加网站资源
class ResGroupAddWebHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        err = ''
        res_group_id = self.get_argument('res_group_id')
        res_webs = self.session.query(ResWeb).filter(ResWeb.company_id == self.get_secure_cookie('company_id')).all()
        self.render("res_group_add_web.html", auth_user=self.current_user, res_group_id=res_group_id, res_webs=res_webs, err=err)

    @tornado.web.authenticated
    def post(self):
        res_group_id = self.get_argument('res_group_id')
        res_web_ids = self.get_arguments('res_web_ids')
        res_group = self.session.query(ResGroup).filter(ResGroup.id == res_group_id).first()
        for res_web_id in res_web_ids:
            res_web = self.session.query(ResWeb).filter(ResWeb.id == res_web_id).first()
            res_group.resWeb.append(res_web)
        self.session.commit()
        self.redirect('/res/group?res_group_id=' + res_group_id)


# 资源组管理--删除网站资源
class ResGroupDeleteWebHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        res_web_id = self.get_argument('res_web_id')
        res_group_id = self.get_argument('res_group_id')
        res_web = self.session.query(ResWeb).filter(ResWeb.id == res_web_id).first()
        res_group = self.session.query(ResGroup).filter(ResGroup.id == res_group_id).first()
        res_group.resWeb.remove(res_web)
        self.session.commit()
        self.redirect('/res/group?res_group_id=' + res_group_id)


# 资源组管理--添加图片资源
class ResGroupAddImageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        res_group_id = self.get_argument('res_group_id')
        res_images = self.session.query(ResImage).filter(ResImage.company_id == self.get_secure_cookie('company_id')).all()
        self.render("res_group_add_image.html", auth_user=self.current_user, res_group_id=res_group_id, res_images=res_images)

    @tornado.web.authenticated
    def post(self):
        res_group_id = self.get_argument('res_group_id')
        res_image_ids = self.get_arguments('res_image_ids')
        res_group = self.session.query(ResGroup).filter(ResGroup.id == res_group_id).first()
        for res_image_id in res_image_ids:
            res_image = self.session.query(ResImage).filter(ResImage.id == res_image_id).first()
            res_group.resImage.append(res_image)
        self.session.commit()
        self.redirect('/res/group?res_group_id=' + res_group_id)


# 资源组管理--删除图片资源
class ResGroupDeleteImageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        res_image_id = self.get_argument('res_image_id')
        res_group_id = self.get_argument('res_group_id')
        res_image = self.session.query(ResImage).filter(ResImage.id == res_image_id).first()
        res_group = self.session.query(ResGroup).filter(ResGroup.id == res_group_id).first()
        res_group.resImage.remove(res_image)
        self.session.commit()
        self.redirect('/res/group?res_group_id=' + res_group_id)


# 资源组管理--添加视频资源
class ResGroupAddVideoHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        res_group_id = self.get_argument('res_group_id')
        res_videos = self.session.query(ResVideo).filter(ResVideo.company_id == self.get_secure_cookie('company_id')).all()
        self.render("res_group_add_video.html", auth_user=self.current_user, res_group_id=res_group_id, res_videos=res_videos)

    @tornado.web.authenticated
    def post(self):
        res_group_id = self.get_argument('res_group_id')
        res_video_ids = self.get_arguments('res_video_ids')
        res_group = self.session.query(ResGroup).filter(ResGroup.id == res_group_id).first()
        for res_video_id in res_video_ids:
            res_video = self.session.query(ResVideo).filter(ResVideo.id == res_video_id).first()
            res_group.resVideo.append(res_video)
        self.session.commit()
        self.redirect('/res/group?res_group_id=' + res_group_id)


# 资源组管理--删除视频资源
class ResGroupDeleteVideoHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        res_video_id = self.get_argument('res_video_id')
        res_group_id = self.get_argument('res_group_id')
        res_video = self.session.query(ResVideo).filter(ResVideo.id == res_video_id).first()
        res_group = self.session.query(ResGroup).filter(ResGroup.id == res_group_id).first()
        res_group.resVideo.remove(res_video)
        self.session.commit()
        self.redirect('/res/group?res_group_id=' + res_group_id)
