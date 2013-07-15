# coding: utf-8

import urllib, urllib2, cookielib, re, json, eyed3, os

songs_dir = 'songs'
base_url = 'http://douban.fm/j/mine/playlist?type=n&sid=&pt=0.0&channel=0&from=mainsite'
invalid = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']

def valid_filename(s):
    return filter(lambda x:x not in invalid, s)

def get_songs_information(sid, ssid):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    urllib2.install_opener(opener)
    prereq = urllib2.Request('http://douban.fm?start=%sg%sg' % (sid, ssid))
    prereq.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    urllib2.urlopen(prereq, timeout=20).read()
    req = urllib2.Request(base_url)
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    ret = json.loads(urllib2.urlopen(req, timeout=20).read())
    return ret['song']

def download(song):
    try:
        os.mkdir(songs_dir)
    except:
        pass
    filename = '%s-%s.mp3' % (valid_filename(song['artist']) , valid_filename(song['title']))
    filepath = os.path.join(songs_dir, filename)
    if os.path.exists(filepath):
        return
    try: 
        print 'url: ' + song['url']
        urllib.urlretrieve(song['url'], filepath)
        print 'Song downloaded'
    except ContentTooShortError:
        print 'ContentTooShortError'
        if os.path.exists(filepath):
            os.remove(filepath)
        return False
    except:
        print 'Error'
        if os.path.exists(filepath):
            os.remove(filepath)
        return False
            
    picname = song['picture'][1+song['picture'].rindex('/'):]
    picpath = os.path.join(songs_dir, picname)

    try:
        urllib.urlretrieve(song['picture'].replace('mpic','lpic'), picpath)
        print 'Picture downloaded'
    except Exception, e:
        print 'Error in retrieve picture!'
        pass
    try:
        tag = eyed3.Tag()
        tag.link(filepath)
        tag.header.setVersion(eyed3.ID3_V2_3)
        tag.encoding = '\x01'
        tag.setTitle(song['title'])
        tag.setAlbum(song['albumtitle'])
        tag.setArtist(song['artist'])
        tag.setDate(song['public_time'])
        tag.addImage(3, picpath)
        os.remove(picpath)
        tag.update()
    except Exception, e:
        print 'Error in tag update!%s' % str(e)
        pass

def handle(sid, ssid):
    try:
        songs = get_songs_information(sid, ssid)
        print 'infomation done!'
        for song in songs:
            if sid == song['sid']:
                download(song)
                return True
    except:
        print 'Error in Handle'
        pass
    return False
