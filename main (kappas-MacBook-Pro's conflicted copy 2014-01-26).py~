#!/usr/bin/env python
# coding=utf-8


import webapp2
import urllib

import os
from google.appengine.ext.webapp import template

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

from datetime import datetime
from google.appengine.api import memcache

from google.appengine.api import images

from google.appengine.ext import db
from google.appengine.ext import webapp

import datetime
import logging


TIME_OUT = 1.5

def render_greetings():
    logging.info('redering memcache.')
    q = Kakikomi.all()
    q.order("-date")

    kakikomis = q.fetch(40)
    page = 1
    for i in kakikomis:
        i.date = i.date+datetime.timedelta(hours=9)
   
    # 出力
    template_values = {'kakikomi': '<font color="red">kakikomi</font>', 'kakikomis': kakikomis,
                       'upload_url': blobstore.create_upload_url('/write'),
                       'prev_page': '<a href="/?page=%s"><u><-- 前のページ</u></a>' % str(page-1) if page > 1 else '',
                       'next_page': '<a href="/?page=%s"><u>次のページ --></u></a>' % str(page+1),
                       }        
    
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    return template.render(path, template_values)


class Kakikomi(db.Model):
    name = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    mail = db.StringProperty(required=True)
    age = db.StringProperty(required=True)
    place = db.StringProperty(required=True)
    message = db.StringProperty(required=True, multiline=True)
    delkey = db.StringProperty(required=True)
    color = db.StringProperty()
    file_key = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

import time
class WriteHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
	if self.request.get('isSpam') != u'エロプロ':
	    logging.error('it was spam.')
 	    self.redirect('/')
	    return 

        kakikomi = Kakikomi(name=self.request.get('name'),
                            mail=self.request.get('mail'),
                            title=self.request.get('title'),
                            age=self.request.get('age'),
                            place=self.request.get('place'),
                            message=self.request.get('message'),
                            delkey=self.request.get('delkey'),
        )
        kakikomi.put()

        time.sleep(3)
        greetings = render_greetings()
        if not memcache.set("greetings", greetings):
            logging.error("Memcache set failed.")        
        
        self.redirect('/upload?key=%s' % kakikomi.key())


class EditHandler(webapp2.RequestHandler):
    def get(self):
        """
        編集フォームの生成
        """
        res = db.get(self.request.get('key'))
        template_values = {'key': self.request.get('key'), 'r': res}

        path = os.path.join(os.path.dirname(__file__), 'edit.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        """
        編集および削除をする
        """
        if self.request.get('delete'):
            res = db.get(self.request.get('key'))
            if self.request.get('delkey') == res.delkey:
                res.delete()
                
                time.sleep(TIME_OUT)
                greetings = render_greetings()
                if not memcache.set("greetings", greetings):
                    logging.error("Memcache set failed.")
                    
            self.redirect('/')

        if self.request.get('edit'):
            res = db.get(self.request.get('key'))
            if self.request.get('delkey') == res.delkey:
                res.name = self.request.get('name')
                res.mail = self.request.get('mail')
                res.title = self.request.get('title')
                res.age = self.request.get('age')
                res.place = self.request.get('place')
                res.message = self.request.get('message')
                res.put()
                
                time.sleep(TIME_OUT)
                greetings = render_greetings()
                if not memcache.set("greetings", greetings):
                    logging.error("Memcache set failed.")                        

            self.redirect('/')


    
class MainHandler(webapp2.RequestHandler):
    def get(self):

        #ページ番号の読み込み
        limit = 40
        page = self.request.get('page')
        page = int(page) if page else 1

        if page == 1:
            self.response.out.write(self.get_greetings())
            return 

        
        q = Kakikomi.all()
        q.order("-date")
        kakikomis = q.fetch(limit, (page-1)*limit)

        for i in kakikomis:
            i.date = i.date+datetime.timedelta(hours=9)
        
        # 出力
        template_values = {'kakikomi': '<font color="red">kakikomi</font>', 'kakikomis': kakikomis,
                           'upload_url': blobstore.create_upload_url('/write'),
                           'prev_page': '<a href="/?page=%s"><u><-- 前のページ</u></a>' % str(page-1) if page > 1 else '',
                           'next_page': '<a href="/?page=%s"><u>次のページ --></u></a>' % str(page+1),
                           }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

    def get_greetings(self):
        greetings = memcache.get("greetings")
        if greetings is not None:
            logging.info('Using memcache.')
            return greetings
        else:
            greetings = render_greetings()
            if not memcache.add("greetings", greetings):
                logging.error("Memcache set failed.")
            return greetings



        

class About(webapp2.RequestHandler):
    def get(self):
        template_values = dict(test='<font color="red">kakikomi</font>')

        path = os.path.join(os.path.dirname(__file__), 'about.html')
        self.response.out.write(template.render(path, template_values))


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        template_values= {'key': self.request.get('key'), 'upload_url': blobstore.create_upload_url('/upload'), 'error': self.request.get('error')}
        path = os.path.join(os.path.dirname(__file__), 'upload.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        key = self.request.get('key')
        res = db.get(key)
        upload_files = self.get_uploads('file')
        if upload_files:
            blob_info = upload_files[0]
            #self.response.out.write(blob_info.content_type + str(blob_info.size))
            image_types = ('image/bmp', 'image/jpeg', 'image/png', 'image/gif')
            if blob_info.content_type in image_types and blob_info.size < 500000:
                res.file_key = str(blob_info.key())
                res.put()

                time.sleep(TIME_OUT)
                greetings = render_greetings()
                if not memcache.set("greetings", greetings):
                    logging.error("Memcache set failed.")        
                self.redirect('/')
            else:
                self.redirect('/upload?key=%s&error=%s' % (key, 'error'))
        else:
            self.redirect('/')


class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)


class Photo(db.Model):
    title = db.StringProperty()
    full_size_image = db.BlobProperty()


class Thumbnailer(webapp.RequestHandler):
    def get(self):
        blob_key = self.request.get('key')

        if blob_key:
            blob_info = blobstore.get(blob_key)

            if blob_info:
                img = images.Image(blob_key=blob_key)
                img.resize(width=100, height=100)
                thumbnail = img.execute_transforms(output_encoding=images.JPEG)
                self.response.headers['Content-Type'] = 'image/jpeg'
                self.response.out.write(thumbnail)
                return

        self.error(404)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/edit', EditHandler),
    ('/write', WriteHandler),
    ('/about', About),
    ('/upload', UploadHandler),
    ('/thumb', Thumbnailer),
    ('/img/([^/]+)?', ServeHandler),
], debug=True)


