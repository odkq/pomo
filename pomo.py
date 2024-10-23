#!/usr/bin/env python
"""
A simple pomodoro timer to use with i3status for i3 or sway window managers.
https://github.com/odkq/pomo

Copyright (C) 2024 by Pablo Martin <pablo@odkq.com>. See LICENSE file.
"""
from asyncio import set_event_loop, new_event_loop, sleep as asleep
from inotify_simple import INotify, flags
from os.path import exists
from subprocess import call
from sys import argv, exit
from time import time

loop_period = 1
period = 0
inotify = None
start = None
status_path = "/var/tmp/pomo.status"
period_path = "/var/tmp/pomo.period"
expired = False


def reload_period():
    """Reload period (in minutes) from /var/tmp/pomo.period and start timer"""
    global period, start, expired
    try:
        line = open(period_path, "r").readlines()[0]
    except IndexError:
        minutes = 0
    try:
        minutes = int(line)
    except ValueError:
        minutes = 0
    period = minutes * 60
    if period == 0:
        update_tray("   ")
    start = round(time())
    expired = False


def update_tray(s):
    """Update the status path, which will be printed with i3status"""
    try:
        current = open(status_path, "r").readlines()[0]
    except IndexError:  # file is empty
        current = ""
    if len(current) > 0 and current[-1] == "\n":
        current = current[:-1]
    if current == s:  # file contains the same string
        return
    open(status_path, "w").write(s)


def quantum():
    """Update the countdown"""
    global expired
    for event in inotify.read(timeout=1):
        reload_period()
    if period == 0:
        return
    current = round(time())
    delta = current - start
    countdown = period - delta
    if countdown <= 0:
        update_tray("   ")
        if not expired:
            call(["zenity", "--info",
                  "--text=\"<span font='30'>⏳Finished ⏳</span>\"",
                  "--width", "500", "--height", "500"])
            expired = True
        return
    mins, secs = divmod(countdown, 60)
    if mins > 0:
        update_tray(f"⏳{mins}m{secs}s")
    else:
        update_tray(f"⏳{secs}s")


async def run_periodically():
    """Periodic callback for asyncio"""
    while True:
        quantum()
        await asleep(loop_period)


if len(argv) == 2:
    try:
        min = int(argv[1])
    except ValueError:
        print("Parameter must be a number (minutes), for example: pomo 25")
        exit(1)
    open(period_path, 'w').write(f"{min}")
    exit(0)

# Create the temporary files if not there
for file in ["/var/tmp/pomo.status", "/var/tmp/pomo.period"]:
    if not exists(file):
        open(file, "w").write("")

update_tray("   ")
inotify = INotify()
wd = inotify.add_watch(period_path, flags.MODIFY)
loop = new_event_loop()
set_event_loop(loop)
loop.run_until_complete(run_periodically())
