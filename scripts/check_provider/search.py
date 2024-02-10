
import json
from urllib.parse import unquote
import requests
import re

from ehp_mod import *
from similarity import similar, clean_words, to_exclude
from pprint import pprint

#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# fencekey needed for torrentgalaxy
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
    "Cookie": "fencekey=8e4a1a83911ff4607fd224cf2fec1691"
}

sim_min = 0.34
sim_mid = 0.42
sim_max = 0.68

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def simcolor(value):
	if value >= sim_max: c = bcolors.OKGREEN
	elif value >= sim_mid: c = bcolors.OKBLUE
	elif value >= sim_min: c = bcolors.WARNING
	else: c = bcolors.FAIL
	return f"{c}{value}{bcolors.ENDC}"

def read_json():	
	with open('../../burst/providers/providers.json') as f:
		data = json.load(f)
		return data

def extract(content):
	matches = re.findall(r'magnet:\?[^\'"\s<>\[\]]+', content)
	if matches:
		return matches

def mag_name(name):
	r = re.findall(r'[?&(&amp;)]dn=([^&]+).*', name)
	return r[0] if len(r) >= 1 else ''

def mag_hash(name):
	r = re.findall(r'urn:btih:([a-zA-Z0-9]+).*', name)
	return r[0] if len(r) >= 1 else None

def check_sim(q, name):
	empty = ''
	if name == '': empty = f"{bcolors.WARNING}magnet sem nome{bcolors.ENDC}"
	q1 = clean_words(unquote(q)).lower()
	name1 = clean_words(unquote(name)).lower()
	result = round(similar(q1, name1), 3)
	print(f"{bcolors.HEADER} similarity - query:{q1} / name:{name1} - {simcolor(result)} {empty}")
	return result

def test_site(query, base_url, name, row, torrent, show_links = False):
	print('test_site()')
	c = requests.get(base_url, headers=headers)
	dom = Html().feed(c.text)

	results = []

	items = eval('dom.' + row)
	print('\n\n', f'{bcolors.OKGREEN}NEW PROVIDER{bcolors.ENDC}')
	print(base_url, len(items), ' resultados - response ', c) 
	for item in items:
		if not item: continue
		n = eval(name)
		t = eval(torrent)
		if not t.startswith('magnet'):
			try:
				s = requests.get(t, headers=headers)
			except Exception as e:
				print(e)
				continue
			links = extract(s.text)
			print(n, t, 'subpage links ', len(links) if links != None else None,
											links if show_links and links else '',
											'\n\n\n' if links != None and show_links else '')
			
			if links != None:
				for rl in links:
					results.append([n, len(links), check_sim(query, mag_name(rl)), mag_name(rl), rl])

		else:
			print(n, ''.join((t[:75])))
			results.append([n, t, 'place', 'place', 'place'])
	
	return results

def test_all_providers(i, j, limit = 5):
	not_br_to_check = ['bitsearch', 'magnetdl', 'thepiratebay', 'torrentgalaxy', 'yts']
	main_key = 'filebase' # last not br provider
	#main_key = "cinetorrent.com.br" # first br provider
	all_keys = list(j.keys())
	index = all_keys.index(main_key)
	br_keys = [x for x in all_keys if all_keys.index(x) >= index]
	br_keys.reverse()
	print('index: ', index)
	#print(br_keys)

	results = []
	unique_results = {}

	for site in br_keys + not_br_to_check:
		name = j[site]["parser"]["name"]
		row = j[site]["parser"]["row"]
		torrent = j[site]["parser"]["torrent"]
		subpage = j[site]["subpage"]
		base_url = j[site]["base_url"].replace('QUERY', i).replace('EXTRA', '')

		try: c = requests.get(base_url, headers=headers, timeout=7)
		except Exception:
			print('timeout', base_url)
			continue

		dom = Html().feed(c.text)
		if dom == None:
			print('\ndom is none for site ', site)
			continue

		try: items = eval('dom.' + row)
		except:
			print('items eval error for', site)
			continue
		#breaks = '\n\n'
		breaks = '\n'
		print(breaks, f'{bcolors.OKGREEN}NEW PROVIDER{bcolors.ENDC}')
		print(base_url, len(items), ' resultados - response ', c)
		counter = 0
		for item in items:
			if not item: continue
			n = eval(name)
			t = eval(torrent)
			if subpage and not t.startswith('magnet') and not to_exclude(n):
				print(n, t)
				if check_sim(i, n) < sim_min:
					continue
				try: s = requests.get(t, headers=headers, timeout=4)
				except Exception:
					print('timeout', t)
					continue
				links = extract(s.text)
				print('    subpage links ', len(links) if links != None else None)
				
				if links != None:
					for rl in links:
						results.append([n, len(links), check_sim(i, mag_name(rl)), mag_name(rl), rl])
						
						#print(rl)
						if mag_hash(rl) not in unique_results.keys():
							unique_results[mag_hash(rl)] = {'n':mag_name(rl), 'f':rl}
						elif mag_hash(rl) in unique_results.keys() and len(rl) > len(unique_results[mag_hash(rl)]['f']):
							unique_results[mag_hash(rl)] = {'n':mag_name(rl), 'f':rl}
				
			else:
				print(f"{n}")
				check_sim(i, mag_name(t))
				results.append([n, t, 'place', 'place', 'place'])

			counter += 1
			#if counter == limit: break

		#yield results
	print('\n\n\n')
	ans = input('Show all magnets? [Y][n]')
	if ans == 'Y': pprint(unique_results)
	#yield results


def make_rules(rowType, nameOrder, rowItem, rowClasses, torrentOrder, nameTag = 'a', onceType = 'id', onceItem = '', onceValue = '', torrentSelector = ''):
	# nameTag: a, span
	# nameOrder: 1,2 ...
	# rowItem, onceItem: article, div, li ...
	# rowClasses, onceValue: 'post', ['post'], 'post-item', 'blog-post'
	# torrentOrder: 1,2 ...
	# onceType: id, class

	rowString = None
	if rowType == 'b':
		rowString = "find_all('%s', ('class',%s))" % (rowItem, rowClasses)

	elif rowType == 'f':
		rowString = "find_once('%s', ('%s', '%s')).find_all('%s', ('class',%s))" % (onceItem,onceType,onceValue,rowItem,rowClasses)

	elif rowType == 'fa':
		rowString = "find_once('%s', ('%s', '%s')).find_all('%s')" % (onceItem,onceType,onceValue,rowItem)

	return {
		'parsing_name': "item('%s', order=%s)" % (nameTag, nameOrder),
		'parsing_row': rowString,
		'parsing_torrent': "item(tag='a',%s attribute='href', order=%s)" % (torrentSelector, torrentOrder)
		}

	#{
	#'parsing_name': "item('a', order=1)",
	#'parsing_row': "find_all('article', ('class','post'))",
	#'parsing_torrent': "item(tag='a', attribute='href', order=1)"
	#}


	
