#!/usr/bin/env python

import subprocess
import time

from dogtail.procedural import click, focus, select, keyCombo, type
from dogtail.tree import root

def start_pidgin():
    pid = subprocess.Popen(['pidgin',  '-c', '/home/tvbinar/.alice_purple'])
    time.sleep(3)
    focus.application('Pidgin')
    return pid

def open_conversation_with(buddy):
    click.tableCell(buddy)
    keyCombo("Enter")
    focus.frame(buddy)
    time.sleep(1)

def start_private_conversation():
    click.menu('OTR')
    click.menuItem("Start private conversation")

def send_message(buddy, message):
    focus.frame(buddy)
    focus.text()
    type(message)
    keyCombo("Enter")

def assert_otr_status(expected):
    try:
        # TODO remove this space from pidgin UI, probably used for formating
        focus.frame.button(' ' + expected)
    except SearchError:
        raise AssertionError("OTR status != then %s", expected)

if __name__ == '__main__':
    pid = start_pidgin()
    root.application('Pidgin')

    try:
        open_conversation_with("bob@localhost")
        assert_otr_status('Not private')
        start_private_conversation()
        assert_otr_status('Unverified')
        send_message('bob@localhost', 'Hi bob!')
    finally:
        raw_input("End?\n")
        pid.terminate()

