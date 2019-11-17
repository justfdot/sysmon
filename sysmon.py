#!/usr/bin/env python3

import psutil
import telebot
import time

BOT_TOKEN = '652949053:AAGvpXVAkROr3GW9GQVS0pLkIJYKBgZDFQ8'
DESTINATION = '922107755'
# DESTINATION = '-338805972'

tb = telebot.TeleBot(BOT_TOKEN)
telebot.apihelper.proxy = {'https': 'socks5h://127.0.0.1:9050'}


def humanize_bytes(value):
    byte_suffix = list('BKMGT')
    while value > 1024. and len(byte_suffix) > 1:
        value /= 1024.
        byte_suffix.pop(0)
    precision = 1 if value < 10 else 0
    return f'{value:.{precision}f}{byte_suffix[0]}'


def handle_data(value, warn=50, crit=85, label=None):
    value = int(value)

    if crit < warn:
        value *= -1
        warn *= -1
        crit *= -1

    if value >= crit:
        title = 'CRITICAL'
    elif value >= warn:
        title = 'WARNING'
    else:
        return

    if label == 'RAM':
        value = humanize_bytes(value)

    tb.send_message(
        DESTINATION,
        f'System Monitor: {title}\n{label} usage: {value}',
        disable_web_page_preview=True, parse_mode='HTML')


def run_monitor():

    while True:
        handle_data(
            psutil.cpu_percent(),
            warn=75,
            crit=90,
            label='CPU')

        handle_data(
            psutil.virtual_memory().used,
            warn=(2 * 1024 * 1024 * 1024),
            crit=(2.6 * 1024 * 1024 * 1024),
            label='RAM')
        time.sleep(30)


if __name__ == '__main__':
    run_monitor()
