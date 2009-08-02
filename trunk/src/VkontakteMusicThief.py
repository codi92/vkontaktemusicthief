# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Nikolay Kandalintsev  <nicloay@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

import rb, gtk, rhythmdb
import gobject
import urllib2
import re
from VkontakteMusicThiefPreferences import VkontakteMusicThiefPreferences
from Keyring import store_cc_details,get_cc_details
from multiprocessing import Lock

class VkontakteSource(rb.BrowserSource):
    def __init__(self):
        rb.BrowserSource.__init__(self)

       
gobject.type_register(VkontakteSource)

class VkontakteMusicThief (rb.Plugin):
    def __init__(self):
        rb.Plugin.__init__(self)
    def activate(self, shell):
    # First lets see if we can add to the context menu
        self.db = shell.props.db
        self.entry_type = self.db.entry_register_type("MyEntryType")
        self.vksource = gobject.new (VkontakteSource, shell=shell, name=_("Vkontakte Thief"), entry_type=self.entry_type)
        shell.append_source(self.vksource, None)
        mail,pwd,hash,id=get_cc_details()
        self.__mail=mail
        self.__pwd=pwd
        self.__hash=hash
        self.__id=id

        self.generate_playlist()


    def create_configure_dialog(self, dialog=None):
        if not dialog:
            dialog=VkontakteMusicThiefPreferences()
        dialog.window.connect("destroy", self.test_calback)
        dialog.window.present()
        return dialog.window

    def test_calback(self):
        print 100*"==++=="
        
    def deactivate(self, shell):
        self.db.entry_delete_by_type(self.entry_type)
        self.db.commit()
        self.db = None
        self.entry_type = None

        self.vksource.delete_thyself()
        self.vksource = None

    def generate_playlist(self):
        AUDIO_PAGE_REF="audio.php"
        current_page=AUDIO_PAGE_REF
        active_page=0     
        summary=0
        while current_page:
            print 100*"="
            print current_page
            tmp= self.getAudioPage(current_page);
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
                    entry = self.db.entry_new(self.entry_type, filepath)
                    self.db.set(entry, rhythmdb.PROP_TITLE, composition)
                    self.db.set(entry, rhythmdb.PROP_ARTIST, artist)
                    self.db.set(entry, rhythmdb.PROP_DURATION, duration)
                except Exception, e: 
                    #print e
                    pass

            #<ul class="commentsPages"><li class="current"><a href="#">1</a></li><li><a href="javascript: getPageContent(100, 1);">2</a></li><li><a href="javascript: getPageContent(200, 1);">3</a></li></ul><div style='height: 20px' id='progrWrapTop'><img style='vertical-align: -4px' src='images/upload.gif' id='progrTop' /></div></div>   <div id="audios" style="padding: 5px 30px">
            if (summary==0):
                exprStr=r"class=\"summary\"><div>(\d*)"
                p = re.compile(exprStr)
                wtf=p.findall(tmp)
                summary=int(wtf[0])
                print 100*"+"
                print summary

            active_page=active_page+100
            print active_page
            if (active_page<summary):
                current_page=AUDIO_PAGE_REF+"?act=getpages&auto=1&id="+self.__id+"&offset="+str(active_page)
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
        print cookies
        data=""
        headers = { 'User-Agent' : user_agent, "Cookie" : cookies }
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        the_page = response.read()
        info = response.info()
        charset = info['Content-Type'].split('charset=')[-1]
        result=unicode(the_page,charset)
        return result
