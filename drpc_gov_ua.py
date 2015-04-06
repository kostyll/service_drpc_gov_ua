#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import collections
import urllib
import urllib2
import urlparse
import xml.etree.ElementTree
import bs4

import service_api

class DRPC_GOV_UA(service_api.SynchronizedBaseAPI):
    u"""
    automated system of electronic tickets
    http://dprc.gov.ua

    DRPC-Service short describtion of iteration:
        To get trains list by station name:
            'http://dprc.gov.ua/awg/xml?class_name=IStations&method_name=search_station&var_0=3&var_1=2&var_2=0&var_3=16&var_4=%D0%9A%D0%B8'
            Returns :
            '<?xml version="1.0" encoding="WINDOWS-1251" ?>
            <MSG>
                <var_0>
                    <childs>
                        <i v="22200001"/>
                        <i v="\xca\xc8\xaf\xc2-\xcf\xc0\xd1\xc0\xc6\xc8\xd0\xd1\xdc\xca\xc8\xc9"/>
                    </childs>
                    <childs>
                        <i v="22200004"/>
                        <i v="\xca\xc8\xaf\xc2 \xcc\xce\xd1\xca\xce\xc2\xd1\xdc\xca\xc8\xc9"/>
                        </childs><childs>
                        <i v="22200005"/>
                        <i v="\xca\xc8\xaf\xc2 \xc4\xcd\xb2\xcf\xd0\xce\xc2\xd1\xdc\xca\xc8\xc9"/>
                    </childs>
                    <childs>
                        <i v="22200003"/>
                        <i v="\xca\xc8\xaf\xc2-\xc2\xce\xcb\xc8\xcd\xd1\xdc\xca\xc8\xc9"/>
                    </childs>
                    <childs>
                        <i v="22200660"/>
                        <i v="\xca\xc8\xaf\xc2-\xc6\xce\xc2\xd2\xcd\xc5\xc2\xc8\xc9"/>
                    </childs>
                    <childs>
                        <i v="22064050"/>
                        <i v="\xca\xc8\xd1\xcb\xce\xc2\xce\xc4\xd1\xca"/>
                    </childs>
                    <childs>
                        <i v="22300000"/>
                        <i v="\xca\xc8\xd8\xc8\xcd\xdd\xd3"/>
                    </childs>
                    <childs>
                        <i v="22204512"/>
                        <i v="\xca\xc8\xd0\xc8\xca\xb2\xc2\xca\xc0"/>
                        </childs><childs><i v="22060600"/>
                        <i v="\xca\xc8\xd0\xce\xc2 \xcf\xc0\xd1\xd1"/>
                    </childs>
                    <childs>
                        <i v="22210703"/>
                        <i v="\xca\xc8\xd0\xc8\xcb\xb2\xc2\xca\xc0"/>
                    </childs>
                    <childs>
                        <i v="22208429"/>
                        <i v="\xca\xc8\xd0\xcd\xc0\xd1\xb2\xc2\xca\xc0"/>
                    </childs>
                    <childs>
                        <i v="22010060"/>
                        <i v="\xca\xc8\xcd\xc5\xd8\xcc\xc0"/>
                    </childs>
                    <childs>
                        <i v="22214092"/>
                        <i v="\xca\xc8\xcf\xd3\xd7\xc0"/>
                    </childs>
                    <childs>
                        <i v="22060006"/>
                        <i v="\xca\xc8\xd0\xce\xc2-\xca\xce\xd2\xcb\xc0\xd1\xd1\xca\xc8\xc9"/>
                    </childs>
                    <childs>
                        <i v="22010123"/>
                        <i v="\xca\xc8\xc2\xc5\xd0"/>
                    </childs>
                    <childs>
                        <i v="22000149"/>
                        <i v="\xca\xc8\xcc\xce\xc2\xd1\xca"/>
                    </childs>
                </var_0>
            </MSG>'

        To get trains for selected direction:
           browser = robobrowser.RoboBrowser ()
            url = 'http://dprc.gov.ua/show.php'
            params = dict(src=22200001, dst=22218025, dt='2015-01-09')
            browser.open(url+'/?'+urllib.urlencode(params))

            trains = browser.select ('.train_row')

            # <tr class="train_row" id="row_0">
            # <td class="info_row train first" style="font-size: 14pt; vertical-align: top; margin-top: 0px; padding-top: 1px; padding-right: 0px;">143К</td>
            # <td class="info_row name">КИЇВ-ПАСАЖИРСЬКИЙ</td>
            # <td class="info_row name">ІВАНО-ФРАНКІВСЬК</td>
            # <td class="info_row depart">21:04</td>
            # <td class="info_row onway"> 08:53</td>
            # <td class="info_row arrive">05:57</td>
            # <td class="divider"></td>
            # <td class="wagon_row empty c_1050"></td>
            # <td class="wagon_row c_1040"><p class="price">268.65<span class="grn"> грн.</span><br/><span class="sts red">1 місць, </span><span class="order"><a href="#">Заказать</a></span></p><p class="seats_avail">Залишилось вільних місць:1</p></td>
            # <td class="wagon_row c_1030"><p class="price">187.36<span class="grn"> грн.</span><br/><span class="sts red">1 місць, </span><span class="order"><a href="#">Заказать</a></span></p><p class="seats_avail">Залишилось вільних місць:1</p></td>
            # <td class="wagon_row empty c_1025"></td>
            # <td class="wagon_row empty c_1020"></td>
            # <td class="wagon_row empty c_1001 last"></td>
            # </tr>
    """

    def _make_search_station_query(self,station_name_query):
        query_params = dict(
            var_3=16,
            var_2=0,
            var_1=2,
            var_0=3,
            var_4=station_name_query,
            method_name='search_station',
            class_name='IStations'
        )
        query_url = 'http://dprc.gov.ua/awg/xml'
        return "?".join((query_url,urllib.urlencode(query_params)))

    def _parse_search_station_results(self,results_in_xml_string):
        result = {}

        #MSG element
        root_tag = xml.etree.ElementTree.fromstring(results_in_xml_string)

        #var_0 element
        var_0 = root_tag.getchildren()[0]

        children = var_0.getchildren()

        for child in children:
            number,name = child.getchildren()
            result.update({name.attrib['v']:number.attrib['v']})
        return result

    def _stations_py_name_pattern(self,name_pattern):
        if name_pattern is None:
            return None
        query = self._make_search_station_query(name_pattern)
        response = urllib2.urlopen(query)
        if response.code != 200:
            return None
        raw_xml_string = response.read()
        return self._parse_search_station_results(raw_xml_string)

    def method_get_stations_by_name_pattern(self,kwargs):
        """
        Gets the station's numbers and names in external service API by name pattern query
        Params:
            1.name_pattern: string
        Returns:
            list of names
        """
        name_pattern = kwargs.get('name_pattern',None)
        return self._stations_py_name_pattern(name_pattern).keys()

    def method_get_station_identifiers_by_name(self,kwargs):
        """
        Gets the station number in external service API by name query
        Params:
            1.name: string
        Returns:
            list of identifiers
        """
        name = kwargs.get('name',None)
        if not name:
            return None
        resuls = []
        return self._stations_py_name_pattern(name).values()

    def method_get_trains(self,kwargs):
        """
        get_trains method returns info about raices
        from station1 to station2 at some date

        Params:
            1.from: string :station identifier
            2.to : string :station identifier
            3.date : string : date of race in format YYYY-MM-DD
        Returns:
            list of race info's with free places and their kinds and prices

        TrainRace = collections.namedtuple("TrainRace", "number direction wagons depart onway arrivement date")
        Wagon = collections.namedtuple("Wagon", "kind free_places_count price")
        """
        src = kwargs.get('from',None)
        if src is None:
            return None
        dst = kwargs.get('to',None)
        if dst is None:
            return None
        dt = kwargs.get('date',None)
        if dt is None:
            return None

        trains_page_html = self._get_train_races_page(src, dst, dt)

        if trains_page_html is None:
            return None

        return self._parse_train_races_page(trains_page_html,dt)

    def _get_train_races_page(self,from_,to_,date):
        params = dict(src=from_, dst=to_, dt=date)
        url = 'http://dprc.gov.ua/show.php'
        print params

        full_url = url+'?'+urllib.urlencode(params)
        print full_url

        response = urllib2.urlopen(full_url)
        if response.code != 200:
            return None

        return response.read()

    def _parse_train_races_page(self,html_string,dt):
        place_kinds = {
        '.c_1050':u'Люкс'.encode('utf-8'),
        '.c_1040':u'Купе фірмовий'.encode('utf-8'),
        '.c_1030':u'Купе'.encode('utf-8'),
        '.c_1025':u'Плацкарт фірмовий'.encode('utf-8'),
        '.c_1020':u'Плацкарт'.encode('utf-8'),
        '.c_1001':u'Сидя'.encode('utf-8'),
        }

        soup = bs4.BeautifulSoup(html_string)

        trains = soup.select('.train_row')

        TrainRace = collections.namedtuple("TrainRace", "number direction wagons depart onway arrivement date")
        Wagon = collections.namedtuple("Wagon", "kind free_places_count price")

        races = []

        for train in trains:
            number = train.select('.first')[0].text
            names =  train.select('.name')
            direction = ">".join(map(lambda x: x.text,names))
            wagons = []

            for kind in place_kinds.keys():
                places = train.select(kind)[0]
                if 'empty' not in places['class']:
                    # print "Тип вагона : {}".format(place_kinds[kind])
                    seats_avail = train.select(kind)[0].select('.seats_avail')[0].text.rpartition(':')[2]
                    # print  "Вільних місць: {}".format(seats_avail)
                    price = float(filter(lambda x: x.isdigit() or x == '.',list(train.select(kind)[0].select('.price')[0].children)[0]))
                    # print "Ціна: {}".format(price)

                    wagon = Wagon(
                            kind=place_kinds[kind],
                            free_places_count=seats_avail,
                            price=price,
                        )
                    wagons.append(wagon)

            depart = train.select('.depart')[0].text
            onway = train.select('.onway')[0].text
            arrive  = train.select('.arrive')[0].text

            train_race = TrainRace(
                    number=number,
                    direction=direction,
                    wagons=wagons,
                    depart=depart,
                    onway=onway,
                    arrivement=arrive,
                    date=dt,
                )

            #print "Depart: {}, onway: {}, arrive: {} ".format(depart,onway, arrive)
            races.append(train_race)
        return races

    @classmethod
    def represent(some_class):
        return "DRPC_GOV_UA"


__all__ = []

def register():
    return [DRPC_GOV_UA,]
