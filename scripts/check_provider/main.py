
import sys
from PyQt5.QtWidgets import QApplication
from search import read_json, make_rules, test_site, test_all_providers
from gui import SearchApp


def query_correction(q):
    q = q.lower()
    q = q.replace(':', '')
    q = q.replace(',', '')
    q = q.replace('!', '')
    q = q.replace('-', '')
    q = q.replace('+', ' ') # year explorer
    for part in range(1,10):
        q = q.replace(' parte %s' % part, ' ')
        q = q.replace(' parte 0%s' % part, ' ')
        q = q.replace(' parte %s' % 'i'*part, ' ')
    return q


if __name__ == '__main__':

	bu = ''
	#bu = bu.replace('EXTRA', '&lang=15')
	#bu = bu.replace('EXTRA', ' dublado')
	#bu = bu.replace('EXTRA', ' [Dublado Portugues]') # perde resultados
	
	j = read_json()
	#i = 'avatar 2009'
	#i = 'gen v s01e01'
	#i = 'the walking dead 1 temporada'
	i = 'liga da justiça: crise nas infinitas terras - parte 1 2024'
	#i = 'Batem à Porta 2023'
	#i = 'Harry Potter e as Relíquias da Morte: Parte 2 2011'
	#i = 'matrix'
	#i = 'invasores de corpos'
	#i = 'o iluminado'
	#i = 'o vidente 2002'
	#i = 'the last of us'
	#i = 'naruto'
	#i = 'naruto classico'
	#i = 'velozes e furiosos'
	#i = input('Query: ')
	
	
	
	# nerdfilmes.com.br, comandotorrents.to, filmeviatorrents.org, filmestorrents.pro, freefilmes.net
	#pp = make_rules('b',1,'article', "'post'",1 )

	# cinetorrent.com.br
	#pp = make_rules('b',2,'article', "'blog-post'",2)

	# supertorrents.net
	#pp = make_rules('b', 2, 'article', "'container-info-filme'", 2)
	
	# comandofilmeshd.org, filmestorrent.tv, torrentdofilmes.com, torrentdosfilmes.site, bludvfilmes.net, torrentdosfilmes.se
	#pp = make_rules('b', 1, 'div', "'post'", 1)

	# torrentfilmesx.com
	#pp = make_rules('b', 1, 'div', "'post'", 1, 'h2')
	
	# megatorrentsx.com
	#pp = make_rules('b', 2, 'div', "'post'", 2)

	# piratefilmesmega.tech
	#pp = make_rules('b', 1, 'div', "'one-post'", 1)

	# freefilmes.net
	#pp = make_rules('b', 1, 'div', "'inside-article'", 1)

	# semtorrent.com, emtorrents.com
	#pp = make_rules('b', 1, 'div', "'capa_lista'", 1, 'h2')

	# insanostorrent.com
	#pp = make_rules('b', 1, 'div', "'box-filme-item'", 1, 'h1')

	# vamostorrent.com
	#pp = make_rules('b', 1, 'div', "'blog_bloco'", 1)
	
	# hiperflix.org
	#pp = make_rules('f', 2, 'div', "'item'", 1, 'span', 'class', 'div', 'filmes')

	# netjmx.com, comandofilmes3.com, comando4kfilmes.org
	#pp = make_rules('b', 1, 'h1', "'post-title'", 1)

	#
	#pp = make_rules('fa', 1, 'li', "", 1, 'h3', 'class', 'ul', "filmesindex")

	# wolverdonfilme.net
	#pp = make_rules('b', 1, 'li', "'post-item'", 1)

	# torrentgalaxy.to
	#pp = make_rules('f', 2, 'div', "'tgxtablerow'", 1, 'a', 'class', 'div', 'tgxtable', "select=('role', 'button'),")

	# bitsearch
	#pp = {
	#	'parsing_name': "item(tag='h5', select=('class', 'title'))",
	#	'parsing_row': "find_all(tag='li', select=('class', 'search-result'))",
	#	'parsing_torrent': "item(tag='a', select=('class', 'dl-magnet'), attribute='href', order=1)"
	#}

	i = query_correction(i)

	#print(pp)
	#test_site(i, bu.replace('QUERY', i), pp['parsing_name'], pp['parsing_row'], pp['parsing_torrent'], False)


	test_all_providers(i, j, 100)
	
