
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def clean_words(querywords): # ToDO: put these words at settings.xml
    words_to_remove = ['4k', '(4k)', 'dual', 'áudio', 'dublado', '720p', '1080p', '5.1', '7.1', 'web-dl', 'webdl', '2160p', 'download',
    'hd', 'bluray', 'hdcam', '3d', 'hsbs', 'torrent', 'blu-ray', 'rip', 'legendado', 'legenda', '/', '|', '-', '–', 'bd-r', '720p/1080p', 'bdrip', '(Blu-Ray)',
    '720p/1080p/4K', 'novela', 'seriado', 'full', 'hdr', 'h264', 'x264', 'sdr', 'x265', 'h265', '[Dublado', 'Portugues]', 'hdtc', 'ac-3', '720p/1080p/4k',
    'webrip', '10bit', 'hdr10plus', 'atmos', 'pt', 'br', '(bluray)', 'aac', 'ddp5', 'dd2', 'camrip', 'avc', 'dts-h', 'dts', '1080p/4k', 'audio',
    '5.1ch', 'remux', 'hevc', 'dts-hd', 'truehd', 'ma', '[1080p]', '[720p]', '[2160p]', 'hdts', 'amzn', 'dublagem',
    'trilogia', 'imax', 'remastered', '3d', 'stereoscopic', 'hdtv',
	'----------abaixo-stopwords-dos-releasers----------',
    'tpf', '1win', 'rarbg', '210gji', '(by-luanharper)', 'comando.to', 'bludv', '(torrentus', 'filmes)', 'andretpf', 'jef', 'derew', 'fgt', 'filmestorrent',
    'www', 'ThePirateFilmes']
    treated_word = querywords.replace('+', ' ').replace('5.1','').replace('7.1','').replace('.',' ').replace("'","").replace(':','')
    resultwords  = [word for word in treated_word.split() if not word.lower() in words_to_remove]
    return ' '.join(resultwords)
