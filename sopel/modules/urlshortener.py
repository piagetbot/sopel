# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from apiclient.discovery import build
from apiclient.errors import HttpError
import re
import httplib2
import json

from sopel.config.types import StaticSection, ValidatedAttribute
class GoogleSection(StaticSection):
    apikey = ValidatedAttribute('apikey', str)

def setup(bot):
    bot.config.define_section('google', GoogleSection)
    service = build('urlshortener', 'v1', developerKey=bot.config.google.apikey)

def configure(config):
    config.define_section('google', GoogleSection, validate=False)
    config.google.configure_setting('apikey',
                                    'Please enter a Google API key. If this is left blank, then some modules may not work, or may work unauthenticated.')

@sopel.module.commands('shorten')
@sopel.module.example('&shorten')
def shorten_url(bot, trigger):
    regex = re.compile('^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,}))\.?)(?::\d{2,5})?(?:[\/?#]\S*)?$', re.I)
    if regex.match(trigger.group(2)):
        try:
            body = {'longUrl': trigger.group(2)}
            response = service.url().insert(body = body, fields='id, longUrl').execute()
            bot.reply(response['longUrl'] + ' is ' + response['id'] + '.')
        except:
            bot.reply('Unknown error.')
    else:
        bot.reply('Invalid URL entered (' + trigger.group(2) + '). Please note that the protocol needs to be in the entered URL.')

@sopel.module.commands('expand')
@sopel.module.example('&expand')
def expand_url(bot, trigger):
    regex = re.compile('^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,}))\.?)(?::\d{2,5})?(?:[\/?#]\S*)?$', re.I)
    if regex.match(trigger.group(2)):
        http = httplib2.Http(cache="~/.sopelcache")
        service = build('urlshortener', 'v1', developerKey=bot.config.google.apikey)
        try:
            http = httplib2.Http(cache="~/.sopelcache")
            service = build('urlshortener', 'v1', developerKey=bot.config.google.apikey)
            global response
            response = service.url().get(shortUrl = trigger.group(2), fields='id, longUrl').execute()
            bot.reply(response['id'] + ' is ' + response['longUrl'] + '.')
        except HttpError:
            if response['error']['errors'][0]['reason'] == 'invalid':
                body = {'longUrl': trigger.group(2)}
                response2 = service.url().insert(body = body, fields='id, longUrl').execute()
                bot.reply('This is an invalid short URL, so I shortened it instead: ' + response2['longUrl'] + ' is ' + response2['id'] + '.')
            elif response['error']['errors'][0]['reason'] == 'notFound':
                bot.reply('Invalid short URL (1).')
            else:
                bot.reply('Unknown error: ' + response['error']['message'])
        except KeyError:
            bot.reply('Invalid short URL (2).')
        except:
            bot.reply('Unknown error.')
    else:
        bot.reply('Invalid URL entered (' + trigger.group(2) + '). Please note that the protocol needs to be in the entered URL.')
