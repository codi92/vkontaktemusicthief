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

import re
from VkontakteMusicThiefPreferences import VkontakteMusicThiefPreferences
from Keyring import store_cc_details,get_cc_details
from MySource import MySource


class VkontakteMusicThief (rb.Plugin):
    def __init__(self):
        rb.Plugin.__init__(self)
    def activate(self, shell):
    # First lets see if we can add to the context menu
        self.db = shell.props.db
        self.entry_type = self.db.entry_register_type("VkontakteMyEntryType")
        group = rb.rb_source_group_get_by_name ("vkontakte")
        if not group:
            group = rb.rb_source_group_register ("vkontakte",
 							     _("Vkontakte"),
 							     rb.SOURCE_GROUP_CATEGORY_FIXED)

        self.vksource = gobject.new (MySource, shell=shell, name=_("My Music"), entry_type=self.entry_type,source_group=group)
        shell.register_entry_type_for_source(self.vksource, self.entry_type)
        shell.append_source(self.vksource, None)



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
