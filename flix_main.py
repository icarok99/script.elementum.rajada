# -*- coding: utf-8 -*-

import os
import sys
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'site-packages'))

try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from flix.provider import Provider, ProviderResult
from burst.elementum_provider import log
from burst import burst
from burst.update_providers import do_update

try: arg = sys.argv[1].lower()
except Exception: arg = None

if arg == "update_providers":
	do_update()
	exit()

def included_rx(value, keys):
	value = ' ' + value.lower() + ' '
	for key in keys:
	    rr = r'\W+(' + key + r')\W*'
	    if re.search(rr, value):
	        return True
	return False

def check_is_at(name, dicti, default_value):
    idx = 0
    count = -1
    res = default_value # Default Value
    for r in dicti:
        count += 1
        if included_rx(name, keys=dicti[r]):
            idx = count
            res = r
    return res, idx

color_map = {
	'filter_240p': 'FFFC3401',
	'filter_480p': 'FFA56F01',
	'filter_720p': 'FF539A02',
	'filter_1080p': 'FF0166FC',
	'filter_2K': 'FFF15052',
	'filter_4K': 'FF6BB9EC'
}

def check_resolution(name):
	resolutions = OrderedDict()
	resolutions['filter_240p'] = ['240[pр]', 'vhs\-?rip']
	resolutions['filter_480p'] = ['480[pр]', 'xvid|dvd|dvdrip|hdtv|web\-(dl)?rip|iptv|sat\-?rip|tv\-?rip']
	resolutions['filter_720p'] = ['720[pр]|1280x720', 'hd720p?|hd\-?rip|b[rd]rip']
	resolutions['filter_1080p'] = ['1080[piр]|1920x1080', 'hd1080p?|fullhd|fhd|blu\W*ray|bd\W*remux']
	resolutions['filter_2K'] = ['1440[pр]', '2k']
	resolutions['filter_4K'] = ['4k|2160[pр]|uhd', '4k|hd4k']

	res, idx = check_is_at(name, resolutions, 'filter_480p')
	return '[COLOR %s]%s[/COLOR]' % (color_map[res], res.split('_')[1]), idx


def check_release(name):
    release_types = {
        'filter_brrip': ['brrip|bd\-?rip|blu\-?ray|bd\-?remux'],
        'filter_webdl': ['web_?\-?dl|web\-?rip|dl\-?rip|yts'],
        'filter_hdrip': ['hd\-?rip'],
        'filter_hdtv': ['hd\-?tv'],
        'filter_dvd': ['dvd|dvd\-?rip|vcd\-?rip'],
        'filter_dvdscr': ['dvd\-?scr'],
        'filter_screener': ['screener|scr'],
        'filter_3d': ['3d'],
        'filter_telesync': ['telesync|ts|tc'],
        'filter_cam': ['cam|hd\-?cam'],
        'filter_tvrip': ['tv\-?rip|sat\-?rip|dvb'],
        'filter_vhsrip': ['vhs\-?rip'],
        'filter_iptvrip': ['iptv\-?rip'],
        'filter_trailer': ['trailer|трейлер|тизер'],
        'filter_workprint': ['workprint'],
        'filter_line': ['line']
    }
    res, idx = check_is_at(name, release_types, 'filter_dvd')
    return res.split('_')[1]

def check_codecs(name):
	pass

def elementum_general_payload(query):
	return {
		#'proxy_url': '',
		#'internal_proxy_url': 'http://127.0.0.1:65222',
		#'elementum_url': 'http://127.0.0.1:65220',
		'silent': False,
		'skip_auth': False,
		'query': query,
	}

def elementum_movie_payload(tmdb_id, title, titles, year):
	return {
		#'proxy_url': '',
		#'internal_proxy_url': 'http://127.0.0.1:65222',
		#'elementum_url': 'http://127.0.0.1:65220',
		'silent': False,
		'skip_auth': False,
		#'imdb_id': '',
		'tmdb_id': tmdb_id,
		'title': title,
		'year': year,
		#'years': {},
		'titles': titles,
	}

def elementum_show_payload(tmdb_id, title, titles, season, episode):
	return {
		#'proxy_url': '',
		#'internal_proxy_url': 'http://127.0.0.1:65222',
		#'elementum_url': 'http://127.0.0.1:65220',
		'silent': False,
		'skip_auth': False,
		#'imdb_id': '',
		#'tvdb_id': '',
		'tmdb_id': tmdb_id,
		'show_tmdb_id': tmdb_id,
		'title': title,
		'season': season,
		#'season_name': '',
		'episode': episode,
		#'year': year,
		#'season_year': '',
		#'show_year': '',
		'titles': titles,
		#'absolute_number': 1,
		#'anime': False,
	}
	
def convert_results(obj):
    obj = sorted(obj, key = lambda x: check_resolution(x['name'])[1], reverse=True) # sort by resolution
    #log.debug("[COLOR blue]obj result for flix: %s[/COLOR]" % obj)
    result = []
    for item in obj:
        crrt_res, crrt_idx = check_resolution(item['name'])
        size_str = "[B][%s][/B]" % item['size'] if len(item['size']) > 0 else ''
        release_str = '' #check_release(item['name'])
        label_str = "%s (%s / %s) %s %s - %s" % (crrt_res, item['seeds'], item['peers'], size_str, release_str, item['provider'])
        result.append(ProviderResult(
            label = label_str,
            label2 = item['name'],
            icon = item["icon"],
            url = "plugin://plugin.video.torrest/play_magnet?magnet={}".format(quote_plus(item["uri"])),
        ))
    return result

class RajadaProvider(Provider):

    def search(self, query):
        #log.debug("[COLOR blue]current query for flix: %s[/COLOR]" % query)
        s = burst.search(elementum_general_payload(query), "general")
        s = convert_results(s)
        #log.debug("[COLOR blue]final general result for flix: %s[/COLOR]" % repr(s))
        return s

    def search_movie(self, tmdb_id, title, titles, year=None):
        #s = burst.search(elementum_movie_payload(tmdb_id, title, titles, year or ""), "movie")
        s = burst.search(elementum_general_payload("%s %s" % (title, year)), "general")
        s = convert_results(s)
        #log.debug("[COLOR blue]final movie result for flix: %s[/COLOR]" % repr(s))
        return s

    def search_show(self, tmdb_id, show_title, titles, year=None):
        #s = burst.search(elementum_movie_payload(tmdb_id, show_title, titles, year or ""), "show")
        s = burst.search(elementum_general_payload("%s %s" % (show_title, year)), "general")
        s = convert_results(s)
        #log.debug("[COLOR blue]final show result for flix: %s[/COLOR]" % repr(s))
        return s

    def search_season(self, tmdb_id, show_title, season_number, titles):
        #s = burst.search(elementum_show_payload(tmdb_id, show_title, titles, season_number, 1), "season")
        s = burst.search(elementum_general_payload("%s %s temporada" % (show_title, season_number)), "general")
        s = convert_results(s)
        #log.debug("[COLOR blue]final season result for flix: %s[/COLOR]" % repr(s))
        return s

    def search_episode(self, tmdb_id, show_title, season_number, episode_number, titles):
        #s = burst.search(elementum_show_payload(tmdb_id, show_title, titles, season_number, episode_number), "episode")
        s = burst.search(elementum_general_payload("%s %s temporada" % (show_title, season_number)), "general")
        s = convert_results(s)
        #log.debug("[COLOR blue]final episode result for flix: %s[/COLOR]" % repr(s))
        return s

    def resolve(self, provider_data):
		# this should be called only if 'url' is not at ProviderResult object
        #log.debug("[COLOR blue]resolve provider data: %s[/COLOR]" % repr(provider_data))
        if isinstance(provider_data, dict):
            return provider_data["url"]
        raise NotImplementedError("Resolve method can't be called on this provider")

RajadaProvider().register()
