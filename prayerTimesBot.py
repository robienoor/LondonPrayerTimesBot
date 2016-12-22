#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages. This is built on the API wrapper, see
# echobot2.py to see the same example built on the telegram.ext bot framework.
# This program is dedicated to the public domain under the CC0 license.
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import fetchPrayerTimes
#from nltk.tokenize import TweetTokenizer


update_id = None

mosquesWebsites = {'Regents': "http://www.iccuk.org/",
               "DSM": "http://britasiauk.com/mosque/",
               "ELM": "http://www.eastlondonmosque.org.uk/"}


mosquesDictionary = {"drum": "DSM",
                    "euston": "DSM",
                    "north gower": "DSM"}

timesDictionary = {"today": 0,
                    "tomorrow": 1,
                    "week": 7}


def main():
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot('303434540:AAHZFQmhUfMuhKTPXWaseSmFa1ArUKDZi1c')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    global update_id
    # Request updates after the last update_id
    for update in bot.getUpdates(offset=update_id, timeout=10):
        # chat_id is required to reply to any message
        chat_id = update.message.chat_id
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            #update.message.reply_text(update.message.text + " to you too")

            bot.sendMessage(parse_mode='HTML', chat_id=chat_id, text=parseRequest(update.message.text))


def parseRequest(text):

    if text == "hello":
        return "wa alaykum assalam, how can I help you today?"

    return parseMessage(text)

def parseMessage(text):
    message = text.lower()

    mosque = " "
    timeShift = 0

    #search for mention of mosque
    for key, value in mosquesDictionary.items():
        if key in message:
            print("found a mosque")
            mosque = value

    if mosque == " ":
            return "Sorry, I'm not familiar with that mosque"


    #search for time mention:
    for key, value in timesDictionary.items():
        if key in text:
            timeShift = value

    return fetchPrayerTimes.getPrayerTimes(mosque, timeShift)


if __name__ == '__main__':
    main()