# coding=utf-8
"""Live CSD feed module"""
# Copyright 2016, tom29739
# Licensed under the Eiffel Forum License 2.

from __future__ import unicode_literals, absolute_import, print_function, division

import logging
import re
from socketIO_client import SocketIO, BaseNamespace

from sopel.config.types import StaticSection, FilenameAttribute
from sopel.module import commands, example

def setup(bot):
    logging.basicConfig(level=logging.INFO)

@commands('startcsdfeed')
@example('&startcsdfeed')
def startcsdfeed(bot, trigger):
    """CSD feed"""
    class MainNamespace(BaseNamespace):
        def on_change(self, change):
            if change['type'] == 'categorize':
                if change['title'] == 'Category:Candidates for speedy deletion':
                    if re.search('.\]\] added to category$', change['comment']):
                        strippedtitle = change['comment'].lstrip('[[').rstrip(']] added to category')
                        unspacedstrippedtitle = strippedtitle.replace(' ','_')
                        bot.say('[Page CSD] ' + 'Wiki: ' + change['wiki'] + ' | Page: http://enwp.org/' + unspacedstrippedtitle + ' | User: ' + change['user'])

        def on_connect(self):
            bot.say('Connected.')
            self.emit('subscribe', 'en.wikipedia.org')
            bot.say('Subscribed to en.wikipedia.org feed.')

    bot.say('Connecting...')
    socketIO = SocketIO('https://stream.wikimedia.org')
    socketIO.define(MainNamespace, '/rc')

    socketIO.wait()
