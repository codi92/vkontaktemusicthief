# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Nikolay Kandalintsev  <nicloay@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

import pygtk
pygtk.require('2.0')
import gtk
import urllib2
import hashlib
from Keyring import store_cc_details,get_cc_details


class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable


class VkontakteMusicThiefPreferences:


    def save_and_quit(self, widget, event, data=None):
        __mail=self.mail.get_text()
        __pwd=self.pwd.get_text()

        url="http://vkontakte.ru/login.php?op=a_login_attempt&email="+__mail+"&pass="+__pwd+"&expire=0"
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        cookies=""
        data=""
        headers = { 'User-Agent' : user_agent, "Cookie" : cookies }
        req = urllib2.Request(url,data,headers)
        response = urllib2.urlopen(req)
        result = response.read()        

        if result=="failed":
            print "fuck"
        else:
            __hash=hashlib.md5(__pwd).hexdigest()
            __id=result.split('good')[1]
            
            store_cc_details(__mail,__pwd,__hash,__id)
        return   
        


    def destroy(self, widget, data=None):
        pass

    def __init__(self):
        def add_label(string):
            label = gtk.Label(string)
            self.window.vbox.pack_start(label, True, True, 0)
            label.show()
        self.window = gtk.Dialog()

        self.window.connect("destroy", self.destroy)
        add_label("User Name (email)")
        self.mail=gtk.Entry(max=25);
        self.window.vbox.pack_start(self.mail, True, True, 0)
        self.mail.show()
        add_label("Password")
        self.pwd=gtk.Entry();
        self.pwd.set_visibility(False)
        self.window.vbox.pack_start(self.pwd, True, True, 0)
        self.pwd.show()
        self.window.set_border_width(10)
        buttonCancel = gtk.Button(stock="_Cancel")
        buttonCancel.connect("clicked",self.destroy,None)
        self.window.action_area.pack_start(buttonCancel, True, True, 0)
        buttonCancel.show()
        button = gtk.Button(stock="_OK")
        button.connect("clicked", self.save_and_quit, None)
        button.connect_object("clicked", gtk.Widget.destroy,self.window)
        self.window.action_area.pack_start(button, True, True, 0)
        try:
            print get_cc_details()
            __mail,__pwd,__hash,__id=get_cc_details()
            self.mail.set_text(__mail)
            self.pwd.set_text(__pwd)
        except Exception, e:
            print e   

        button.show()
        
        
    def main(self):
        gtk.main()

    def get_dialog (self):
        return self.window


