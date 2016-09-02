import sopel.module
from sopel.tools import stderr
@sopel.module.commands('Wheresthebot')
def Wheresthebot(bot, trigger):
    bot.say ("Hello, I'm " +bot.nick + " and I'm in the channel, " trigger.sender + ". Thanks for asking.")
stderr("command wheres the bot ran by " + trigger.nick + ".")
