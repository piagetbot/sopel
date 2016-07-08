"""
slap.py - Slap Module
Copyright 2009, Michael Yanovich, yanovich.net

http://sopel.chat
"""

import random
from sopel.module import commands, require_chanmsg

verbs = ['slaps', 'kicks', 'destroys', 'annihilates', 'punches', 'roundhouse kicks', 'pwns', 'owns']

@require_chanmsg
@commands('slap', 'slaps')
def slap1(bot, trigger):
    """&slap <target> - Slaps <target>"""
    bot.action(random.choice(verbs) + trigger.group(2))
