from sopel.module import commands
from sopel.tools import stderr

@commands('whereisthebot', 'where', 'whereami')
def whereisthebot(bot, trigger):
    bot.say('Hello, I\'m ' + bot.nick + '. This channel is: ' trigger.sender + '. Thanks for asking.')
    stderr('Command: "whereisthebot" ran by ' + trigger.nick + '.')
