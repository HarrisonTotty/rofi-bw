#!/usr/bin/env python3
'''
A small wrapper library for running command-line programs.
'''

import os
import subprocess

ROFI = '/usr/bin/rofi'
ZENITY = '/usr/bin/zenity'
ZTITLE = 'Password Manager'

def rofi(items: list[str]) -> str:
    '''
    Displays a rofi prompt with the specified list of items.
    '''
    with open('/tmp/rofi-bw.out', 'w') as f:
        for i in sorted(items):
            f.write(f'{i}\n')
    (o, ec) = run(
        f'cat /tmp/rofi-bw.out | {ROFI} -dmenu -i -markup-rows -no-custom -p "password : "'
    )
    os.remove('/tmp/rofi-bw.out')
    if ec:
        print(o)
        raise Exception('Unable to launch rofi')
    return o.strip()


def run(cmd):
    '''
    Runs the specified command as a subprocess, returning the output of the
    command and its exit code.
    '''
    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        shell = True
    )
    output = process.communicate()[0].decode('ascii', 'ignore')
    return (output, process.returncode)


def prompt_password() -> str:
    '''
    Uses zenity to display a password prompt.
    '''
    (o, ec) = run(
        f'{ZENITY} --password --title "{ZTITLE}" --text "Enter Master Password"'
    )
    if ec:
        print(o)
        raise Exception('Unable to prompt for master password')
    return o.strip()


def prompt_tfa() -> str:
    '''
    Uses zenity to display a 2FA prompt.
    '''
    (o, ec) = run(
        f'{ZENITY} --entry --title "{ZTITLE}" --text "Enter TFA Code"'
    )
    if ec:
        print(o)
        raise Exception('Unable to prompt for TFA')
    return o.strip()
