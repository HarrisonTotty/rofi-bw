#!/usr/bin/env python3
'''
rofi-bw

A handy script for browsing bitwarden passwords with rofi.
'''

import datetime
import os
import sys

from . import bw
from . import cli
from . import cmd

def main():
    '''
    The entrypoint of the program.
    '''
    args = cli.parse_arguments()

    if os.path.isfile(args.session_file):
        session = bw.load_session(args.session_file)

    if not bw.login_check():
        bw.login(args.client_id, args.client_secret, cmd.prompt_tfa())

    status = bw.status()

    if status['status'] == 'locked':
        bw.unlock(cmd.prompt_password())
        bw.save_session(args.session_file)

    if 'lastSync' in status and status['lastSync']:
        now = datetime.datetime.now()
        oldest = now - datetime.timedelta(minutes = args.sync_threshold)
        last_sync = datetime.datetime.strptime(status['lastSync'].rsplit('.', 1)[0], '%Y-%m-%dT%H:%M:%S')
        if last_sync <= oldest:
            try:
                bw.sync()
            except Exception:
                sys.stderr.write('Warning: Unable to synchronize vault.\n')
    else:
        try:
            bw.sync()
        except Exception:
            sys.stderr.write('Warning: Unable to synchronize vault.\n')

    logins = bw.get_logins()
    rofi_entries = []
    for l in logins:
        if 'username' in l and l['username']:
            rofi_entries.append(
                f'{l["path"]} <span weight="light" size="small"><i>({l["username"]})</i></span>'
            )
        else:
            rofi_entries.append(
                l['path']
            )
    selected = cmd.rofi(rofi_entries).split(' ', 1)[0].strip()
    sys.stdout.write(next(l['password'] for l in logins if l['path'] == selected).strip())
    sys.exit(0)
