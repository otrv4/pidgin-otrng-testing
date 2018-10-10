#!/usr/bin/env python

import subprocess
import time

from dogtail.config import config
from dogtail.rawinput import pressKey, typeText
from dogtail.procedural import click, focus, select, type
from dogtail.tree import root
from dogtail.utils import run

def start_pidgin():
    pid = subprocess.Popen(['pidgin',  '-c', '/home/tvbinar/.alice_purple'])
    time.sleep(2)
    focus.application('Pidgin')
    return pid

def open_conversation_with(buddy):
    click.tableCell(buddy)
    pressKey("Enter")
    focus.frame(buddy)
    time.sleep(1)

def start_private_conversation():
    click.menu('OTR')
    click.menuItem("Start private conversation")

def send_message(buddy, message):
    focus.frame(buddy)
    focus.text()
    type(message)
    pressKey("Enter")

def assert_otr_status(expected):
    # TODO remove this space from pidgin UI, probably used for formating
    focus.frame.button(' ' + expected)

if __name__ == '__main__':
    config.searchCutoffCount = 3
    config.fatalErrors = True

    pid = start_pidgin()
    root.application('Pidgin')
    open_conversation_with("bob@localhost")
    assert_otr_status('Not private')
    start_private_conversation()
    assert_otr_status('Unverified')
    send_message('bob@localhost', 'Hi bob!')
    raw_input("End?\n")
    pid.terminate()

