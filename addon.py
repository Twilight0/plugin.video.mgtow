# -*- coding: utf-8 -*-

'''
    MGTOW Addon
    Author Twilight0

        License summary below, for more details please read license.txt file

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 2 of the License, or
        (at your option) any later version.
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import json
from base64 import b64decode
from resources.lib import url, action
from tulip import directory, youtube, cache, control, bookmarks

gr_id = 'UClJB2HvfbnRHaLV-Y59R7mQ'
en_id1 = 'UCudGalFyS2ogM1vNMVK_nQw'
en_id2 = 'UCuroE3DKmb7V_v-ZY-QCGtg'
ffa_id = 'UC6Iaz96RkYE-MOjnq5NPgqw'
sm_id = 'UCeCV-XNeZIoHiCGfNYCLh9Q'
pl_id = 'PLZF-_NNdxpb5b8lmx6x__-wkAyQ6dB_yB'

key = b64decode('QUl6YVN5QThrMU95TEdmMDNIQk5sMGJ5RDUxMWpyOWNGV28yR1I0')  # please do not copy this key


def item_list(cid):

    return youtube.youtube(key=key).videos(cid)


def yt_playlists(cid):

    return youtube.youtube(key=key).playlists(cid)


def playlists(channel_id):

    ilist = cache.get(yt_playlists, 24, channel_id)

    for p in ilist:
        p.update({'action': 'playlist'})

    for p in ilist:
        bookmark = dict((k, v) for k, v in p.iteritems() if not k == 'next')
        bookmark['bookmark'] = p['url']
        bm_cm = {'title': 30006, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
        refresh = {'title': 30008, 'query': {'action': 'refresh'}}
        cache_clear = {'title': 30005, 'query': {'action': 'cache_clear'}}
        p.update({'cm': [refresh, cache_clear, bm_cm]})

    directory.add(ilist)


def playlist(plid):

    ilist = cache.get(youtube.youtube(key=key).playlist, 12, plid)

    if ilist is None:
        return

    for i in ilist:
        i.update({'action': 'play', 'isFolder': 'False'})

    for item in ilist:
        bookmark = dict((k, v) for k, v in item.iteritems() if not k == 'next')
        bookmark['bookmark'] = item['url']
        bm_cm = {'title': 30006, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
        refresh = {'title': 30008, 'query': {'action': 'refresh'}}
        cache_clear = {'title': 30005, 'query': {'action': 'cache_clear'}}
        item.update({'cm': [refresh, cache_clear, bm_cm]})

    directory.add(ilist, content='videos')


def videos(link):

    if link == 'mgtow':

        if control.setting('language') == '0' and control.infoLabel('System.Language') == 'Greek':
            video_list = cache.get(item_list, 12, gr_id)
        elif control.setting('language') == '0' and control.infoLabel('System.Language') != 'Greek' or control.setting('language') == '1':
            video_list = cache.get(item_list, 12, en_id1) + cache.get(item_list, 12, en_id2)
        else:
            video_list = cache.get(item_list, 12, gr_id)

    else:

        video_list = cache.get(item_list, 12, link)

    for v in video_list:
        v.update({'action': 'play', 'isFolder': 'False'})

    for item in video_list:
        bookmark = dict((k, v) for k, v in item.iteritems() if not k == 'next')
        bookmark['bookmark'] = item['url']
        bm_cm = {'title': 30006, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
        refresh = {'title': 30008, 'query': {'action': 'refresh'}}
        cache_clear = {'title': 30005, 'query': {'action': 'cache_clear'}}
        item.update({'cm': [refresh, cache_clear, bm_cm]})

    directory.add(video_list, content='videos')


def bm_list():

    bm = bookmarks.get()

    na = [{'title': 30012, 'action': None, 'icon': 'empty.png'}]

    if not bm:
        directory.add(na)
        return na

    for item in bm:
        bookmark = dict((k, v) for k, v in item.iteritems() if not k == 'next')
        bookmark['delbookmark'] = item['url']
        item.update({'cm': [{'title': 30007, 'query': {'action': 'deleteBookmark', 'url': json.dumps(bookmark)}}]})

    il = sorted(bm, key=lambda k: k['title'].lower())

    directory.add(il, content='videos')


def main():

    menu = [
        {
            'title': 30001,
            'action': 'videos',
            'icon': control.addonInfo('icon'),
            'url': 'mgtow'
        }
        ,
        {
            'title': 30016,
            'action': 'playlists',
            'icon': control.addonInfo('icon'),
            'url': sm_id
        }
        ,
        {
            'title': 30017,
            'action': 'videos',
            'icon': 'youtube.png',
            'url': ffa_id
        }
        ,
        {
            'title': 30018,
            'action': 'playlist',
            'icon': 'youtube.png',
            'url': pl_id
        }
        ,
        {
            'title': 30003,
            'action': 'bookmarks',
            'icon': 'bookmarks.png'
        }
        ,
        {
            'title': 30004,
            'action': 'settings',
            'icon': 'settings.png'
        }
    ]

    cc = {'title': 30005, 'query': {'action': 'cache_clear'}}

    for item in menu:
        item.update({'cm': [cc]})

    directory.add(menu, content='videos')


########################################################################################################################

if action is None:

    main()

elif action == 'videos':

    videos(url)

elif action == 'play':

    directory.resolve(url)

elif action == 'refresh':

    control.refresh()

elif action == 'playlists':

    playlists(url)

elif action == 'playlist':

    playlist(url)

elif action == 'bookmarks':

    bm_list()

elif action == 'addBookmark':

    bookmarks.add(url)

elif action == 'deleteBookmark':

    bookmarks.delete(url)

elif action == 'settings':

    control.openSettings()

elif action == 'cache_clear':

    if control.yesnoDialog(line1=control.lang(30009), line2='', line3=''):

        cache.clear(withyes=False)

    else:

        control.infoDialog(control.lang(30011))
