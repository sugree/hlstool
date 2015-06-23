#!/usr/bin/python

from __future__ import print_function

import sys
import re
import os
import urlparse
import urllib2
import shutil
import argparse

def verbose(*objs):
    print(*objs, file=sys.stderr)

def get_content(url, referer=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.52 Safari/537.36'
    }
    if referer:
        headers['Referer'] = referer
    req = urllib2.Request(url, None, headers)
    return urllib2.urlopen(req).read()

def download(url, fo, referer=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.52 Safari/537.36'
    }
    if referer:
        headers['Referer'] = referer
    req = urllib2.Request(url, None, headers)
    fi = urllib2.urlopen(req)
    shutil.copyfileobj(fi, fo)
    fi.close()

def get_hls_playlist(playlist_url, referer=None):
    s = get_content(playlist_url, referer)
    chunk_list = []
    for line in s.split('\n'):
        if line.startswith('#'):
            continue
        if not line:
            continue
        chunk_list.append(urlparse.urljoin(playlist_url, line))
    return chunk_list

def get_hls_chunk(chunk_url, playlist_url):
    s = get_content(chunk_url, playlist_url)
    media_list = []
    for line in s.split('\n'):
        if line.startswith('#'):
            continue
        if not line:
            continue
        media_list.append(urlparse.urljoin(chunk_url, line))
    return media_list

class App:
    def __init__(self):
        self.args = self.parse_args()

    def parse_args(self):
        parser = argparse.ArgumentParser(description='HLS dump')
        parser.add_argument('url',
                            help='playlist or html')
        parser.add_argument('-o', dest='output_filename', required=True,
                            help='output filename or stdout "-"')
        parser.add_argument('--regexp', dest='regexp', action='append',
                            help='regular expression(s) with a group to extract url')
        return parser.parse_args()

    def run(self):
        verbose(self.args.url)
        verbose(self.args.output_filename)
        verbose(self.args.regexp)

        url = self.args.url
        referer = url
        for regexp in self.args.regexp:
            s = get_content(url, referer)
            cre = re.compile(regexp)
            referer = url
            url = cre.search(s).group(1)
        verbose(url)

        playlist_url = url
        chunk_list = get_hls_playlist(playlist_url)
        verbose(chunk_list)

        if self.args.output_filename == '-':
            fo = sys.stdout
        else:
            fo = open(self.args.output_filename, 'wb')

        for chunk_url in chunk_list:
            media_list = get_hls_chunk(chunk_url, playlist_url)
            for i, media_url in enumerate(media_list):
                path = urlparse.urlparse(media_url).path
                filename = os.path.basename(path)
                verbose('%s %d/%d' % (filename, i+1, len(media_list)))
                download(media_url, fo, chunk_url)

        if self.args.output_filename:
            fo.close()

if __name__ == '__main__':
    app = App()
    app.run()
