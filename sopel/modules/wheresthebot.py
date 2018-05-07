from sopel.module import commands

@commands('whereisthebot', 'where', 'whereami')
def whereisthebot(bot, trigger):
    bot.say('Hello, I\'m ' + bot.nick + '. This channel is: ' + trigger.sender + '. Thanks for asking.')
