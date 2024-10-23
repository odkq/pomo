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

Put the script in a PATH accessible directory, as ~/.local/bin You may
need to set the execution bit (chmod) on it, and rename it to 'pomo' for
convenience

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
    ExecStart=--- home dir ---/.local/bin/pomo
    Restart=on-failure
    StandardOutput=file:%h/log_file

    [Install]
    WantedBy=default.target

And do

    $ systemctl --user enable pomo
    $ systemctl --user start pomo
