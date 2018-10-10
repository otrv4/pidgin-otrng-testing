#!/usr/bin/env python

import subprocess
import time

from dogtail.config import config
from dogtail.rawinput import pressKey, typeText
from dogtail.predicate import GenericPredicate
from dogtail.procedural import click, focus, select, type
from dogtail.tree import root, SearchError
from dogtail.utils import run

def start_pidgin():
    pid = subprocess.Popen(['pidgin',  '-c', '/home/tvbinar/.alice_purple'])
    time.sleep(2)
    focus.application('Pidgin')
    return pid

def open_conversation_with(buddy):
    click.tableCell(buddy)
    pressKey("Enter")
    focus.window(buddy)
    time.sleep(2)

def start_private_conversation():
    click.menu('OTR')
    click.menuItem("Start private conversation")

def end_private_conversation():
    click.menu('OTR')
    click.menuItem("End private conversation")

def send_message(buddy, message):
    focus.window(buddy)
    focus.text()
    type(message)
    pressKey("Enter")

def assert_otr_status(expected):
    try:
        # TODO remove this space from pidgin UI, probably used for formating
        focus.window.button(' ' + expected)
    except SearchError:
        assert False

def assert_message_is_present(sender, message):
    chat_tab = focus.window.findChild(GenericPredicate(name=sender, roleName='page tab'))
    chat_box = chat_tab.findChild(GenericPredicate(roleName='text'))
    message_len = len(message)
    assert message == chat_box.text[-message_len:]

def switch_conversation_tab_with(tab_name):
    chat_tab = focus.window.findChild(GenericPredicate(name=tab_name, roleName='page tab'))
    chat_tab.click()

if __name__ == '__main__':
    config.searchCutoffCount = 3
    config.defaultDelay = 1.5
    config.blinkOnActions = True
    config.fatalErrors = True

    pid = start_pidgin()
    root.application('Pidgin')

    open_conversation_with("bob@localhost")
    assert_otr_status('Not private')
    start_private_conversation()
    assert_otr_status('Unverified')
    assert_message_is_present('bob@localhost' ,'Unverified conversation started.  Your client is not logging this conversation.')
    send_message('bob@localhost', 'Hi bob!')
    assert_message_is_present('bob@localhost', 'Hi bob!')

    switch_conversation_tab_with('alice@localhost')
    assert_otr_status('Unverified')
    #assert_message_is_present('bob@localhost' ,'Unverified conversation started.  Your client is not logging this conversation.')
    assert_message_is_present('alice@localhost', 'Hi bob!')

    switch_conversation_tab_with('bob@localhost')
    end_private_conversation()
    assert_message_is_present('bob@localhost', 'Private conversation lost.')
    assert_otr_status('Not private')

    raw_input("End?\n")
    pid.terminate()

