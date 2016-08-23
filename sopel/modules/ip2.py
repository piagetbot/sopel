# coding=utf-8
"""GeoIP lookup module"""
# Copyright 2011, Dimitri Molenaars, TyRope.nl,
# Copyright © 2013, Elad Alfassa <elad@fedoraproject.org>
# Licensed under the Eiffel Forum License 2.

from __future__ import unicode_literals, absolute_import, print_function, division

import socket
import os
import ipaddress
import sys
import requests
import re

from sopel.config.types import StaticSection, FilenameAttribute
from sopel.module import commands, example

@commands('ip', 'iplookup', 'iplookup2', 'ip2', 'whois', 'geolocate')
@example('&ip 8.8.8.8')
def ip2(bot, trigger):
    """IP Lookup tool"""
    if not trigger.group(2):
        return bot.reply("No search term. Please provide an IP address.")
    query = trigger.group(3)
    try:
        ipaddress.ip_address(query)
    except ValueError:
        if not re.match('^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])(\.([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9]))*$', query):
            return bot.say('Invalid IP address/hostname (if a hostname, try resolving it to an IP first).')
    r = requests.get('http://ip-api.com/json/' + query + '?fields=187072')
    if r.json()['status'] != 'success':
        return bot.say('Unknown error: ' + r.json()['message'])
    response = "[IP/Host Lookup] "
    if r.json()['reverse']:
        hostname = r.json()['reverse']
        response += "Hostname: %s | " % hostname 
    isp = r.json()['isp']
    response += "ISP/Organisation: %s" % isp
    if r.json()['as']:
        asname = ' (AS Name: ' + r.json()['as'] + ')'
        response += asname
    r2 = requests.get('http://legacy.iphub.info/api.php?ip=' + query + '&showtype=4&email=tom29739@tools.wmflabs.org')
    if r2.json()['proxy']:
        proxy = 'YES'
        response += " | Possible proxy/hosting provider: %s" % proxy
    else:
        proxy = 'NO'
        response += " | Possible proxy/hosting provider: %s" % proxy
    coords = str(r.json()['lat']) + ', ' + str(r.json()['lon'])
    response += " | Coordinates: %s" % coords
    r3 = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng=' + unicode(r.json()['lat']) + ',' + unicode(r.json()['lon']) + '&key=' + bot.config.google.apikey)
    location = r3.json()['results'][1]['formatted_address']
    response += " | Location: %s" % location
    response += " (approximate)"
    try:
        r4 = requests.get('https://en.wikipedia.org/w/api.php?action=query&list=blocks&format=json&bkip=' + query)
        r4.json()['query']['blocks'][0]['id']
        response += " | Blocked on enwiki: YES"
    except:
        try:
            r4 = requests.get('https://en.wikipedia.org/w/api.php?action=query&list=globalblocks&format=json&bgip=' + query)
            r4.json()['query']['globalblocks'][0]['id']
            response += "| Blocked globally: YES (global block)"
        except:
            response += " | Blocked on enwiki or globally: NO"
    finally:
        bot.say(response)

if __name__ == "__main__":
    from sopel.test_tools import run_example_tests
    run_example_tests(__file__)
