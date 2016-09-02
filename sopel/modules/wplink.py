# coding=utf-8
"""
wplink.py - Sopel Wikipedia linking module
Copyright 2016, tom29739
Licensed under the Eiffel Forum License 2.

http://sopel.chat/
"""
from __future__ import unicode_literals, absolute_import, print_function, division
from sopel.module import commands


@commands('link', 'wplink', 'enwplink', 'linkto')
def wplink(bot, trigger):
    """Link to the English Wikipedia."""
    #No input
    if not trigger.group(2):
        return bot.say('https://en.wikipedia.org/')
    bot.say('enwp.org/' + trigger.group(2).replace(' ', '_'))
