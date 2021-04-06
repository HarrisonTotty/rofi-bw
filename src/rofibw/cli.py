#!/usr/bin/env python3
'''
Contains functions for interacting with the CLI.
'''

import argparse
import os
import sys

HELP_DESCRIPTION = """
A handy script for browsing bitwarden passwords with rofi.
"""
HELP_EPILOG = """
"""

def parse_arguments():
    '''
    Parses the command-line arguments passed to the script, returning the
    result.
    '''
    argparser = argparse.ArgumentParser(
        description = HELP_DESCRIPTION,
        epilog = HELP_EPILOG,
        usage = 'rofi-bw [...]',
        add_help = False,
        formatter_class = lambda prog: argparse.RawDescriptionHelpFormatter(prog, max_help_position=45, width=100)
    )
    argparser.add_argument(
        '-i',
        '--client-id',
        default = os.getenv('BW_CLIENTID', ''),
        dest = 'client_id',
        help = '[env: BW_CLIENTID] Specifies the API Client ID to use when authenticating with Bitwarden.',
        metavar = 'STR'
    )
    argparser.add_argument(
        '-s',
        '--client-secret',
        default = os.getenv('BW_CLIENTSECRET', ''),
        dest = 'client_secret',
        help = '[env: BW_CLIENTSECRET] Specifies the API Client Secret to use when authenticating with Bitwarden.',
        metavar = 'STR'
    )
    argparser.add_argument(
        '-f',
        '--session-file',
        default = os.getenv('ROFIBW_SESSION_FILE', '/tmp/rofibw-session'),
        dest = 'session_file',
        help = '[env: ROFIBW_SESSION_FILE] Specifies the session file to use. Defaults to "/tmp/rofibw-session".',
        metavar = 'FILE'
    )
    argparser.add_argument(
        '-S',
        '--sync-threshold',
        default = int(os.getenv('ROFIBW_SYNC_THRESHOLD', '60')),
        dest = 'sync_threshold',
        help = '[env: ROFIBW_SYNC_THRESHOLD] Specifies how old the local vault can be before it is resyncronized. Defaults to 60 mins.',
        metavar = 'MIN',
        type = int
    )
    argparser.add_argument(
        '-h',
        '--help',
        action = 'help',
        help = 'Displays help and usage information.'
    )
    return argparser.parse_args()
