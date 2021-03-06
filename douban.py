# coding: utf-8

import urllib, urllib2, cookielib, re, json, eyeD3, os, httplib
import Cookie
from contextlib import closing
import download
import download_album

RE_ALBUM = re.compile(r'/subject/\d+/')

def html_decode(html):
    #return html.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
    import HTMLParser
    return HTMLParser.HTMLParser().unescape(html)

def get(myurl, cookie):
    print myurl, cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    urllib2.install_opener(opener)
    req = urllib2.Request(myurl)
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    req.add_header('Cookie', cookie)
    req.add_header('Referer', 'http://douban.fm/mine')
    content = urllib2.urlopen(req, timeout=20).read()
    for s in json.loads(content)['songs']:
        sid = s['id']
        album = RE_ALBUM.search(s['path']).group(0)
        try:
            print "song:" + html_decode(s['title']) + "\nsinger:" + html_decode(s['artist']) + "\nalbum:" + s['path']
        except:
            print 'song...'
        try:
            ssid = download_album.get_ssid(album, sid)
            if download.handle(sid, ssid):
                print 'succeed!\n\n'
            else:
                print 'fail!\n\n'
        except:
            print 'fail!\n\n'

def login(username, password):
    data = urllib.urlencode({'form_email':username, 'form_password':password})
    with closing(httplib.HTTPConnection("www.douban.com")) as conn:
        conn.request("POST", "/accounts/login", data, {"Content-Type":"application/x-www-form-urlencoded"})
        cookie = Cookie.SimpleCookie(conn.getresponse().getheader('Set-Cookie'))
        if not cookie.has_key('dbcl2'):
            print 'login failed'
            return
        dbcl2 = cookie['dbcl2'].value
        if dbcl2 and len(dbcl2) > 0:
            uid = dbcl2.split(':')[0]
        bid = cookie['bid'].value
        print cookie

def main():
    #username = raw_input('username:')
    #password = raw_input('password:')
    #login(username, password)
    #cookie = raw_input('cookie:')
    cookie_file = open('cookie.txt', 'r')
    # cookie should include:
    # flag="ok"; ac="1349244677"; bid="m4uoOiPelk4"; person_tags=; person_tag_names=; openExpPan=Y; dbcl2="53360401:j1FKEjqvWuM"; fmNlogin="y"; ck="OEu-";
    cookie = cookie_file.read().strip()
    c = Cookie.SimpleCookie()
    c.load(cookie)
    ck = c.get('ck').value
    url = 'http://douban.fm/j/play_record?ck=' + ck + '&type=liked&start=%d'
    print 'you should enter the pages you want to download'
    start = int(raw_input('page from:'))
    end = int(raw_input('page to:'))
    for i in range(end - start + 1):
        get(url%((start + i - 1) * 15), cookie)

if __name__ == '__main__':
    main()
