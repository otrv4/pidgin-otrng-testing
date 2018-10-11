#coding: utf-8


import time

from dogtail.rawinput import pressKey, typeText
from dogtail.predicate import GenericPredicate
from dogtail.procedural import click, focus, select
from dogtail.tree import SearchError


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

# TODO: create package assertions
def otr_status_is(expected):
    try:
        # TODO remove this space from pidgin UI, probably used for formating
        focus.window.button(' ' + expected)
        return True
    except SearchError:
        return False

def message_is_present(sender, message):
    chat_tab = focus.window.findChild(GenericPredicate(name=sender, roleName='page tab'))
    chat_box = chat_tab.findChild(GenericPredicate(roleName='text'))
    message_len = len(message)
    return message == chat_box.text[-message_len:]

def switch_conversation_tab_with(tab_name):
    chat_tab = focus.window.findChild(GenericPredicate(name=tab_name, roleName='page tab'))
    chat_tab.click()


