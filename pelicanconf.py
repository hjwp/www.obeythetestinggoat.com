#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'Harry J.W. Percival'
SITENAME = u'Obey the Testing Goat!'
SITEURL = 'http://www.obeythetestinggoat.com'
FEED_DOMAIN = SITEURL

TIMEZONE = 'Europe/London'
DEFAULT_LANG = u'en'


# Blogroll
LINKS = (
    ('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
    ('Python.org', 'http://python.org'),
    ('Jinja2', 'http://jinja.pocoo.org'),
)

# Social widget
SOCIAL = (
    ('You can add links in your config file', '#'),
    ('Another social link', '#'),
)

DEFAULT_PAGINATION = 10

THEME = 'theme'
STATIC_PATHS = [
    'static', 'book',
]
READERS = {
    'html': None
}

OUTPUT_PATH = 'output/'
DISQUS_SITENAME = 'obeythetestinggoat'

PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['asciidoc_reader']
ASCIIDOC_OPTIONS = [
    '-a source-highlighter=pygments'
]
ASCIIDOC_BACKEND = 'html5'
