pomo.py
=======

Simple pomodoro timer for i3status (i3 and sway window managers)

Configuration, in ~/.config/i3status/config:

    order += "read_file p"

Below:

    read_file p {
        path = "/var/tmp/pomo.status"
    }


Installation
------------

Put the script in a PATH accessible directory as ~/.local/bin

You can use cp or create a link to the directory you cloned this repo:

    ln -s $(pwd)/pomo.py ~/.local/bin/pomo.py

Runtime dependencies
--------------------

- [zenity](https://gitlab.gnome.org/GNOME/zenity), for the modal dialog
  signaling the end of the period.
- [inotify_simple](https://github.com/chrisjbillington/inotify_simple) to
    watch for changes in the input file

Usage
-----


First the process needs to be running, either on the foreground,
running pomo without parameters, or as a systemd service.

When passed a parameter, it starts a new timer. For example

    pomo.py 25          # Start a new pomodoro timer of 25 min

Install as a local systemd service
----------------------------------

To run it with systemd as a user, write in
~/.config/systemd/user/pomo.service:

    [Unit]
    Description=Pomo User Serivce

    [Service]
    Type=simple
    ExecStart=%h/.local/bin/pomo.py
    Restart=on-failure
    StandardOutput=file:/var/tmp/pomo.log

    [Install]
    WantedBy=default.target

And do

    $ systemctl --user enable pomo
    $ systemctl --user start pomo
