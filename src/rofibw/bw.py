#!/usr/bin/env python3
'''
Contains handy definitions for interacting with the bitwarden CLI.
'''

import os
import json

from . import cmd

BW = '/usr/bin/bw'
SESSION_KEY = ''


def get_logins() -> list:
    '''
    Gets a list of all login objects.
    '''
    if SESSION_KEY: os.environ['BW_SESSION'] = SESSION_KEY
    (io, iec) = cmd.run(f'{BW} list items')
    if iec:
        print(io)
        raise Exception('Unable to list items')
    item_data = json.loads(io)
    (fo, fec) = cmd.run(f'{BW} list folders')
    if fec:
        print(fo)
        raise Exception('Unable to list folders')
    folder_data = json.loads(fo)
    data = []
    for item in item_data:
        if not 'login' in item:
            continue
        ni = {
            'name': item['name'],
            'username': item['login']['username'],
            'password': item['login']['password']
        }
        if 'folderId' in item and item['folderId']:
            d = '/' + next(f['name'] for f in folder_data if f['id'] == item['folderId'])
            ni['directory'] = d
            ni['path'] = d + '/' + item['name']
        else:
            ni['directory'] = '/'
            ni['path'] = '/' + item['name']
        data.append(ni)
    return data


def load_session(path: str):
    '''
    Loads a session from the specified session file, setting the `SESSION_KEY`
    variable and also returning the value.
    '''
    global SESSION_KEY
    try:
        with open(path, 'r') as f:
            SESSION_KEY = f.read().strip()
    except Exception as e:
        raise Exception(f'Unable to load session - {e}')
    return SESSION_KEY


def lock():
    '''
    Locks the local bitwarden vault, destroying active session keys.
    '''
    global SESSION_KEY
    if SESSION_KEY: os.environ['BW_SESSION'] = SESSION_KEY
    (o, ec) = cmd.run(f'{BW} lock')
    if ec:
        print(o)
        raise Exception('Unable to lock bitwarden vault.')
    SESSION_KEY = ''


def login(client_id: str, client_secret: str, tfa: str) -> str:
    '''
    Logs-into a user account given the specified API client ID, secret, and 2-factor code.
    '''
    os.environ['BW_CLIENTID'] = client_id
    os.environ['BW_CLIENTSECRET'] = client_secret
    if SESSION_KEY: os.environ['BW_SESSION'] = SESSION_KEY
    (o, ec) = cmd.run(
        f'{BW} login --apikey --raw --code {tfa}'
    )
    if o:
        data = json.loads(o)
    else:
        data = {'statusCode': 200, 'response': { 'error': None }}
    if ec:
        raise Exception(f'Unable to log into bitwarden - {data["statusCode"]} : {data["response"]["error"]}')
    return data


def login_check() -> bool:
    '''
    Checks to see if the user is currently logged-in.
    '''
    if SESSION_KEY: os.environ['BW_SESSION'] = SESSION_KEY
    (o, ec) = cmd.run(f'{BW} login --check')
    return (ec == 0)


def save_session(path: str):
    '''
    Saves the current session to the specified file path.
    '''
    try:
        with open(path, 'w') as f:
            f.write(SESSION_KEY)
    except Exception as e:
        raise Exception(f'Unable to save session token - {e}')


def status() -> dict:
    '''
    Returns the status dictionary of the current session.
    '''
    if SESSION_KEY: os.environ['BW_SESSION'] = SESSION_KEY
    (o, ec) = cmd.run(f'{BW} status')
    data = json.loads(o)
    if ec:
        print(o)
        raise Exception(f'Unable to get bitwarden status.')
    return data


def sync(force: bool = False):
    '''
    Synchronizes the local database.
    '''
    if SESSION_KEY: os.environ['BW_SESSION'] = SESSION_KEY
    cmdstr = f'{BW} sync'
    if force: cmdstr += ' --force'
    (o, ec) = cmd.run(cmdstr)
    if ec:
        raise Exception('Unable to synchronize local bitwarden vault')


def unlock(master_password: str) -> str:
    '''
    Unlocks the bitwarden vault, returning the bitwarden session token.
    '''
    global SESSION_KEY
    if SESSION_KEY: os.environ['BW_SESSION'] = SESSION_KEY
    (o, ec) = cmd.run(f'{BW} unlock "{master_password}" --raw')
    if ec:
        print(o)
        raise Exception(f'Unable to unlock master password.')
    SESSION_KEY = o.strip()
    return SESSION_KEY
