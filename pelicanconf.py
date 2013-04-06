#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'Harry J.W. Percival'
SITENAME = u'Obey the Testing Goat!'
SITEURL = 'http://www.obeythetestinggoat.com'
#FEED_DOMAIN = http://www.example.com'

TIMEZONE = 'Europe/London'
DEFAULT_LANG = u'en'

import os
THEME = 'theme'
THEME = os.path.join(os.path.dirname(__file__), 'theme')

# Blogroll
LINKS =  (('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
          ('Python.org', 'http://python.org'),
          ('Jinja2', 'http://jinja.pocoo.org'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10
