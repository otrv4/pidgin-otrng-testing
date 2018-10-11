#!/usr/bin/env python

import subprocess
import time

from dogtail.config import config
from dogtail.tree import root
from dogtail.utils import run

from steps import *

def start_pidgin():
    config.searchCutoffCount = 3
    config.defaultDelay = 1.5
    config.blinkOnActions = True
    config.fatalErrors = True

    pid = subprocess.Popen(['pidgin',  '-c', '/home/tvbinar/.alice_purple'])
    time.sleep(2)
    focus.application('Pidgin')
    return pid



def test_interactive_path():
    pid = start_pidgin()
    root.application('Pidgin')

    open_conversation_with("bob@localhost")
    assert otr_status_is('Not private')
    start_private_conversation()
    assert otr_status_is('Unverified')
    assert message_is_present('bob@localhost' ,'Unverified conversation started.  Your client is not logging this conversation.')
    send_message('bob@localhost', 'Hi bob!')
    assert message_is_present('bob@localhost', 'Hi bob!')

    switch_conversation_tab_with('alice@localhost')
    assert otr_status_is('Unverified')
    #assert message_is_present('bob@localhost' ,'Unverified conversation started.  Your client is not logging this conversation.')
    assert message_is_present('alice@localhost', 'Hi bob!')

    switch_conversation_tab_with('bob@localhost')
    end_private_conversation()
    assert message_is_present('bob@localhost', 'Private conversation lost.')
    assert otr_status_is('Not private')

    raw_input("End?\n")
    pid.terminate()

