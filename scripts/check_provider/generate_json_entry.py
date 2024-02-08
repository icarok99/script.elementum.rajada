
provider = input('Provider: ')

j = """
"PROVIDER_NAME": {
    "anime_extra": "",
    "anime_keywords": "{title:br} {episode}",
    "anime_query": "EXTRA",
    "base_url": "https://PROVIDER_NAME/?s=QUERY",
    "color": "FFF14E13",
    "enabled": true,
    "general_extra": "",
    "general_keywords": "{title:br}",
    "general_query": "EXTRA",
    "language": "br",
    "languages": "br, pt",
    "login_failed": "",
    "login_object": "",
    "login_path": null,
    "movie_extra": "",
    "movie_keywords": "{title:br} {year}",
    "movie_query": "EXTRA",
    "name": "PROVIDER_NAME_CAP",
    "parser": {
        "infohash": "",
        "name": "item('a', order=1)",
        "peers": "-1",
        "row": "find_all('div', ('class','post'))",
        "seeds": "-1",
        "size": "",
        "torrent": "item(tag='a', attribute='href', order=1)"
    },
    "private": false,
    "season_extra": "",
    "season_extra2": "",
    "season_keywords": "{title:br} {season:2} temporada",
    "season_query": "EXTRA",
    "separator": "+",
    "show_query": "",
    "subpage": true,
    "tv_extra": "",
    "tv_keywords": "{title:br} s{season:2}e{episode:2}"
}
"""

j = j.replace('PROVIDER_NAME_CAP', provider.split('.')[0].capitalize())
j = j.replace('PROVIDER_NAME', provider.lower())
print(j)
