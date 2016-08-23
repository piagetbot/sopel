"""
slap.py - Slap Module
Copyright 2016, tom29739

http://sopel.chat
"""

import random
from sopel.module import commands, require_chanmsg

verbs = ['slaps', 'kicks', 'destroys', 'annihilates', 'punches', 'roundhouse kicks', 'pwns', 'owns']

@require_chanmsg
@commands('slap', 'slaps')
def slap1(bot, trigger):
    """&slap <target> - Slaps <target>"""
    nick = trigger.group(2)
    if not trigger.group(2):
        nick = trigger.nick
    if trigger.group(2) == bot.nick:
        return bot.say("I may be a bot, but I'm not stupid enough to slap myself.")
    bot.action(random.choice(verbs) + ' ' + nick)
