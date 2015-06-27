HLS Tool
========

This is a set of tool for working with HLS in real life.

hlsdump.py
----------

`hlsdump.py` is a command line utility to dump HLS stream to stdout or
single destination file from specifying playlist url or HTML url
containing dynamic playlist url.

For example, saving playlist url into output.mp4.

```
python hlsdump.py -o output.mp4 http://xxx.com/playlist.m3u8
```

Streaming playlist url to stdout and playing by mplayer.

```
python hlsdump.py -o - http://xxx.com/playlist.m3u8 | mplayer -
```

Saving playlist url embedded in iframe inside another html.

```
python hlsdump.py --regexp 'src="(http://xxx.com/[^"]+)"' --regexp 'file: "([^"]+)"' -o output.mp4 http://xxx.com/page.html
```
