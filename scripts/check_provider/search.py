
import json
import requests
import re

from ehp_mod import *
from similarity import *

#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# fencekey needed for torrentgalaxy
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
    "Cookie": "fencekey=8e4a1a83911ff4607fd224cf2fec1691"
}

sim_min = 0.34
sim_mid = 0.42
sim_max = 0.68

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

def check_sim(q, name):
	return round(similar(clean_words(q).lower(), clean_words(name).lower()), 3)

def test_site(query, base_url, name, row, torrent, show_links = False):
	print('test_site()')
	c = requests.get(base_url, headers=headers)
	dom = Html().feed(c.text)

	results = []

	items = eval('dom.' + row)
	print('\n\n', base_url, len(items), ' resultados - response ', c)	
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
	main_key = "cinetorrent.com.br" # first br provider
	all_keys = list(j.keys())
	index = all_keys.index(main_key)
	br_keys = [x for x in all_keys if all_keys.index(x) >= index]
	print('index: ', index)
	#print(br_keys)

	results = []

	for site in br_keys:
		name = j[site]["parser"]["name"]
		row = j[site]["parser"]["row"]
		torrent = j[site]["parser"]["torrent"]
		subpage = j[site]["subpage"]
		base_url = j[site]["base_url"].replace('QUERY', i).replace('EXTRA', '')

		c = requests.get(base_url, headers=headers)

		dom = Html().feed(c.text)
		if dom == None:
			print('\ndom is none for site ', site)
			continue

		items = eval('dom.' + row)
		print('\n\n', base_url, len(items), ' resultados - response ', c)
		counter = 0
		for item in items:
			if not item: continue
			n = eval(name)
			t = eval(torrent)
			if subpage and not t.startswith('magnet'):
				s = requests.get(t, headers=headers)
				links = extract(s.text)
				print(n, t, 'subpage links ', len(links) if links != None else None)
				
				if links != None:
					for rl in links:
						results.append([n, len(links), check_sim(i, mag_name(rl)), mag_name(rl), rl])
			else:
				print(n, t)
				results.append([n, t, 'place', 'place', 'place'])

			counter += 1
			#if counter == limit: break

		#yield results
	
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


	
