import urllib.parse

# urllib.parse.quote(str2)

prefix = 'magnet:?xt=urn:btih:'
hash = '26f89aad3465be3be664348abf871493'
beforeTitle = '&dn='

raw_title = "Harry Potter Collection (Books 1-7)"
title = urllib.parse.quote(raw_title)

trackerPrefix = '&tr='

trackerOne = 'udp://retracker.netbynet.ru:2710/announceudp'
trackerTwo = 'http://tracker.files.fm:6969/announcehttp'
trackerThree = 'https://tracker.publictorrent.net:443/announcehttps'

# ###
testTracker = 'udp://tracker.leechers-paradise.org:6969/announce'
testResult = urllib.parse.quote(testTracker)
print(testResult)
# ###
# delete /announce from end of tracker
# also need to encode // from trackers


magnet_link = prefix + hash + beforeTitle + title + trackerPrefix + urllib.parse.quote(trackerOne)\
              + trackerPrefix + urllib.parse.quote(trackerTwo)\
              + trackerPrefix + urllib.parse.quote(trackerThree)

#print(magnet_link)
