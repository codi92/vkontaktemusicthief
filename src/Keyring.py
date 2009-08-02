# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Nikolay Kandalintsev  <nicloay@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

import gnomekeyring
import string


keyring_attributes = {"mail": "rb-vkmthief-cc-data"}


keyring = gnomekeyring.get_default_keyring_sync()


def store_cc_details( *details):
    print "storing CC details"
    try:
        id = gnomekeyring.item_create_sync(keyring,
            gnomekeyring.ITEM_GENERIC_SECRET,
            "VkontakteThief credit card info", keyring_attributes,
            string.join (details, '\n'), True)
    except Exception, e:
        print e
    return


def get_cc_details():
    print "getting CC details"
    try:
        ids = gnomekeyring.find_items_sync (gnomekeyring.ITEM_GENERIC_SECRET, keyring_attributes)
        data =  ids[0].secret
        return string.split(data, "\n")       
    except Exception, e:
        print e
    return ("", "", "", "")

def clear_cc_details():

    print "clearing CC details"
    try:
        ids = gnomekeyring.find_items_sync (gnomekeyring.ITEM_GENERIC_SECRET, keyring_attributes)
        gnomekeyring.item_delete_sync (keyring, id[0])
    except Exception, e:
        print e