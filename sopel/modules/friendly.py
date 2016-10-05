# coding=utf-8
"""
ping.py - Sopel Ping Module
Author: Sean B. Palmer, inamidst.com
About: http://sopel.chat
"""
from __future__ import unicode_literals, absolute_import, print_function, division

import random
from sopel.module import rule, priority, thread


@rule(r'(?i)(hi|hello|hey),? $nickname[ \t]*$')
def hello(bot, trigger):
    greeting = random.choice(('Hi', 'Hey', 'Hello', 'How do you do', 'Howdy', 'Welcome', 'Greetings', 'Hiya', 'Good morning/afternoon/evening/night', 'Hullo', 'Good day', 'Yo', 'Buenos dias', 'How are you', 'Aloha', 'Ciao', 'G\'day', 'Bonjour', 'Hail', 'What\'s up', 'How does it', 'S\'up', 'Sup', 'Howdy do', 'What\'s happening', 'Hallo', 'Wassup', 'Heyo', 'Ahoy', 'Gidday', 'Allo', 'Hello there', 'Hola', 'How do', 'What ho', 'Yello', 'Cheerio', 'Halloo', 'Bonsoir', 'Morning/afternoon/evening/night'))
    punctuation = random.choice(('', '!', '.'))
    bot.say(greeting + ' ' + trigger.nick + punctuation)


@rule(r'(?i)(Fuck|Screw) you,? $nickname[ \t]*$')
def rude(bot, trigger):
    bot.say('Watch your mouth, ' + trigger.nick + ', or I\'ll tell your mother!')


@rule('$nickname!')
@priority('high')
@thread(False)
def interjection(bot, trigger):
    bot.say(trigger.nick + '!')
