#!/usr/bin/env python
#-*- coding: utf-8 -*-


import os

from collections import namedtuple
import urllib
import urlparse
import random

os.sys.path.insert(0,
    '../',
)
os.sys.path.insert(0,
    '../../',
)

import mock

mock.patch('drpc_gov_ua.service_api.SyncronizedBaseAPI',side_effect=object)

import drpc_gov_ua

test_pages_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),'resources')

def stations_names_by_pattern(pattern):
    def wrapper(*args,**kwargs):
        result = ("""<?xml version="1.0" encoding="WINDOWS-1251" ?>
        <MSG>
            <var_0>
                <childs>
                    <i v="%s"/>
                    <i v="%s"/>
                </childs>
            </var_0>
        </MSG>""" % (pattern['number'],pattern['name'].encode('utf-8')))

        print repr(result)
        print result.decode('cp1251')
        return result
    return wrapper

def query_string_to_dict(query):
    query = urllib.unquote(query)
    d = dict()
    for param_part in query.split('&'):
        key,value = param_part.split('=')
        d.update({key:value})
    return d

def query_string_to_namedtuple(query):
    d = query_string_to_dict(query)
    nt_args = "QueryNamedTuple"," ".join(d.keys())
    nt = namedtuple(*nt_args)
    return nt(**d)

def urlopen(url):
    print url
    mocked = mock.Mock()
    mocked.code = 200
    parsed_url = urlparse.urlparse(url)
    mocked.url = url
    if parsed_url.path == "/show.php":
        mocked.read = lambda: file(os.path.join(test_pages_dir,'drpc.gov.ua.show.html')).read()
    elif parsed_url.path == "/awg/xml":
        # params = query_string_to_namedtuple(parsed_url.query)
        # mocked.read = lambda: stations_names_by_pattern(dict(number=random.randrange(100000,200000),name=params.var_4))()
        mocked.read = lambda: file(os.path.join(test_pages_dir,'xml.xml')).read()
    return mocked

@mock.patch('urllib2.urlopen',side_effect=urlopen)
def test_DRPC_GOV_UA_method_get_stations_by_name_pattern(mock):
    instance = drpc_gov_ua.DRPC_GOV_UA()

    names = instance.method_get_stations_by_name_pattern({'name_pattern':'Ки'})

    assert isinstance(names, list)

@mock.patch('urllib2.urlopen',side_effect=urlopen)
def test_DRPC_GOV_UA_method_station_identifiers_by_name(mock):

    instance = drpc_gov_ua.DRPC_GOV_UA()

    identifiers = instance.method_get_station_identifiers_by_name({'name':'КИЇВ-ПАСАЖИРСЬКИЙ'})

    assert isinstance(identifiers, list)

@mock.patch('urllib2.urlopen',side_effect=urlopen)
def test_DRPC_GOV_UA_method_get_trains(mock):

    instance = drpc_gov_ua.DRPC_GOV_UA()

    races = instance.method_get_trains({'from':12325,'to':3423423,'date':'2015-04-29'})

    assert isinstance(races, list)




