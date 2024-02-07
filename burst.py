# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'site-packages'))

from burst.burst import search
from burst.update_providers import do_update
from elementum.provider import register

try: arg = sys.argv[1].lower()
except Exception: arg = None

if arg == "update_providers":
	do_update()
	exit()

def search_movie(payload):
    return search(payload, 'movie')


def search_season(payload):
    return search(payload, 'season')


def search_episode(payload):
    return search(payload, 'episode')


register(search, search_movie, search_episode, search_season)
