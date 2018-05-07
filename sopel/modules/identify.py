# coding=utf-8
"""WMF Freenode cloak eligibility module"""
# Copyright 2016, tom29739
# Licensed under the Eiffel Forum License 2.

from __future__ import unicode_literals, absolute_import, print_function, division

import os
import sys
import requests

from sopel.config.types import StaticSection, FilenameAttribute
from sopel.module import commands, example

import arrow

@commands('elig', 'cloak', 'cloakelig')
@example('&elig <user>')
def elig(bot, trigger):
    """Cloak eligibility tool"""
    need_verified_email = True
    need_edit_count = 250
    need_months_registered = 3
    if not trigger.group(2):
        return bot.say('To be eligible for a cloak you need: ' + ['', 'a verified email, '][need_verified_email] + 'be registered for ' + str(need_months_registered) + ' months onwiki' + ' and have ' + str(need_edit_count) + ' edits.')
    query = trigger.group(3)
    required_registration_timestamp = arrow.utcnow().replace(months=-need_months_registered).timestamp
    r = requests.get('https://en.wikipedia.org/w/api.php?action=query&meta=globaluserinfo&guiuser='+ query + '&guiprop=editcount&format=json')
    try:
        actual_registration = arrow.get(r.json()['query']['globaluserinfo']['registration'])
    except KeyError:
        return bot.say('No such user (please note that usernames are case-sensitive).')
    actual_registration_timestamp = actual_registration.timestamp
    if not actual_registration_timestamp <= required_registration_timestamp:
        return bot.say('User: "' + query + '" is ineligible for a cloak because they have not been registered onwiki for long enough (there may be other reasons why this user is ineligible too).')
    actual_edit_count = r.json()['query']['globaluserinfo']['editcount']
    if not actual_edit_count >= need_edit_count:
        return bot.say('User: "' + query + '" is ineligible for a cloak because they do not have enough edits onwiki. They need ' + str(need_edit_count - actual_edit_count) + ' more edits to be eligible under this criterion (there may be other reasons why this user is ineligible too).')
    r2 = requests.get('https://en.wikipedia.org/w/api.php?action=query&list=users&ususers=' + query + '&usprop=emailable&format=json')
    try:
        r2.json()['query']['users'][0]['emailable']
    except KeyError:
        return bot.say('User: "' + query + '" is ineligible for a cloak because they do not have a verified email address (this problem may be caused be the user disabling Special:EmailUser in their English Wikipedia preferences).')
    bot.say('User: "' + query + '" is eligible for a cloak. They registered onwiki about ' + actual_registration.humanize() + ', have ' + str(actual_edit_count) + ' edits and have a verified email address.')
