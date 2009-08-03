# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Nikolay Kandalintsev  <nicloay@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

import rb, rhythmdb
import gobject
from Keyring import store_cc_details,get_cc_details
import time
import urllib2
import re

class MySource(rb.BrowserSource):
    __gproperties__ = {
        'plugin': (rb.Plugin, 'plugin', 'plugin', gobject.PARAM_WRITABLE|gobject.PARAM_CONSTRUCT_ONLY),
    }

    def __init__(self):
        rb.BrowserSource.__init__(self, name=_("My Music"))
        # catalogue stuff
        self.__db = None
        self.__saxHandler = None
        self.__activated = False
        self.__notify_id = 0
        self.__update_id = 0
        self.__info_screen = None
        self.__updating = False
        self.__load_current_size = 0
        self.__load_total_size = 0
        self.__db_load_finished = False
        mail,pwd,hash,id=get_cc_details()
        self.__mail=mail
        self.__pwd=pwd
        self.__hash=hash
        self.__id=id
        self.__catalogue_loader = None
        self.__catalogue_check = None
        
	def do_set_property(self, property, value):
		if property.name == 'plugin':
			self.__plugin = value
		else:
			raise AttributeError, 'unknown property %s' % property.name



    def do_impl_activate(self):
        if not self.__activated:
            shell = self.get_property('shell')
            self.__db = shell.get_property('db')
            self.__entry_type = self.get_property('entry-type')
            self.generate_playlist(self.__db,self.__entry_type)
            self.__activated = True
            rb.UpdateCheck()
        rb.BrowserSource.do_impl_activate (self)
	def do_impl_get_browser_key (self):
		return "/apps/rhythmbox/plugins/vkontakte/my/show_browser"

	def do_impl_get_paned_key (self):
		return "/apps/rhythmbox/plugins/vkontakte/my/paned_position"

	def do_impl_pack_paned (self, paned):
		self.__paned_box = gtk.VBox(False, 5)
		self.pack_start(self.__paned_box)
		self.__paned_box.pack_start(paned)

	def do_impl_delete_thyself(self):
		rb.BrowserSource.do_impl_delete_thyself (self)



    def generate_playlist(self,db,entry_type):
        AUDIO_PAGE_REF="audio.php"
        current_page=AUDIO_PAGE_REF
        active_page=0
        summary=0
        current_song=0
        while current_page:
            tmp= self.getAudioPage(current_page);
            if (summary==0):
                    exprStr=r"class=\"summary\"><div>(\d*)"
                    p = re.compile(exprStr)
                    wtf=p.findall(tmp)
                    summary=int(wtf[0])
                    self.__load_total_size=summary
                    



            exprStr=r"class=\"playimg\" onclick=\"return operate\((.*),(.*),(.*),(.*),(.*)\);\" id"
            p = re.compile(exprStr)
            wtf=p.findall(tmp)
            for i in wtf:
                filepath = 'http://cs' + i[1] + ".vkontakte.ru/u" + i[2] + "/audio/" + i[3].strip("'") + ".mp3";
                exprStr = r"<b id=\"performer"+i[0]+"\"><a .*>(.*)<\/a><\/b>.*>(.*)<\/span>.*\n.*<div class=\"duration\">(.*)<\/"

                res=re.compile(exprStr).findall(tmp)
                if not res:
                    return
                artist= res[0][0]
                composition= res[0][1]
                duration_tmp = res[0][2].split(":")
                try:
                    duration = 60*int(duration_tmp[0])+int(duration_tmp[1])
                except Exception, e:
                    duration=0
                    print e

                if not composition:
                    exprStr = r"<b id=\"performer"+i[0]+"\"><a .*>(.*)<\/a><\/b>.*>(.*)<\/a><\/span>"
                    res=re.compile(exprStr).findall(tmp)
                    composition=res[0][1]
                artist=self.prep_string(artist)
                composition=self.prep_string(composition)
                try:
                    current_song=current_song+1
                    self.__load_current_size=current_song
                    entry = db.entry_new(entry_type, filepath)
                    db.set(entry, rhythmdb.PROP_TITLE, composition)
                    db.set(entry, rhythmdb.PROP_ARTIST, artist)
                    db.set(entry, rhythmdb.PROP_DURATION, duration)
                except Exception, e:
                    #print e
                    pass



            active_page=active_page+100
            if (active_page<summary):
                current_page=AUDIO_PAGE_REF+"?act=getpages&auto=1&id="+self.__id+"&offset="+str(active_page)
                time.sleep(0.2)
            else:
                current_page=""
             




    def prep_string(self,string):
        result=string.replace('&#39;',"'")
        result=result.replace('&quot;','"')
        result=result.replace('&amp;','&')
        r = re.compile(r"&#\d{1,4};")
        result = r.sub("",result)
        return result


    def getAudioPage(self, page_path):
        url="http://vkontakte.ru/"+page_path;
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        mail,pwd,hash,id=get_cc_details()
        cookies="remixfriendsCommon=0; remixemail="+mail+"; remixchk=2; remixvideos=0; remixfriends=1; remixpass="+hash+"; remixmid="+id+";"
        data=""
        headers = { 'User-Agent' : user_agent, "Cookie" : cookies }
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        the_page = response.read()
        info = response.info()
        charset = info['Content-Type'].split('charset=')[-1]
        result=unicode(the_page,charset)
        return result

gobject.type_register(MySource)
