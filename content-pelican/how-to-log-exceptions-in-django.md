Title: How to log exceptions to stderr in Django
Date: 2014-01-23 13:35
Tags: django, logging, exceptions, debugging
Author: Harry
Summary: <p>Django logging can be a little baffling.  Here's an answer to the "how do I make django log all exceptions to the console?" question, which isn't necessarily obvious.</p>


Here's a common set of questions about Django:

* How do I get django to log errors to stderr?
* Why can't I see Django exceptions in the console?
* How do I get Django to log exceptions?
* How to print debug messages in Django?

I know they're common because I've often found asking myself some kind of variant
on these questions, at some point or other.  Then I saw that, in Django 1.6/1.7, the
[default logging configuration](https://docs.djangoproject.com/en/1.7/topics/logging/#django-s-default-logging-configuration) actually does send logging messages to the console

So does this mean that exceptions in Django are going to start appearing in the console
then?  No.

## Just because you wish for it doesn't make it so

I think my own difficulties with this issue stemmed from the fact that,
*obviously*, in my mind, the thing you'd want to log would be exceptions, and
that, since Django will show us a clever debug page (if DEBUG is True), or a 
standard server 500 page, then I sort of assumed it would log that exception
as well. But it doesn't


The reason I struggled with this because I wasn't clear on the fact that there are
actually two systems involved here:

* Django's logging system (based on the Python `logging` module)
* Django's exception handling layer (middleware)

By default (as of Django 1.6), Django *is* configured to send logging messages to
the console.  There are two gotchas however:

* Django's default logging level is set to WARNING, which means any attempt to use
`logging.debug` or `logging.info` will fail
* Django has a middleware layer that automatically catches exceptions, and handles
them differently depending on whether you have `DEBUG = True` or not, but it 
*doesn't* explicitly log them.


## Unit testing Django's logging config (if you want)

This is a blog about TDD, so let's write a test first.  It works by monkey-patching
in an extra view function into the project's url config (mwahahaha). The view then
tries to do various calls to, eg, `logging.debug`, just we'd like to be able to in 
our real views.

Finally it explodes with an exception, so we can test whether any information about
the exception ends up in the logs

We mock out sys.stderr to pick up on what was actually sent to the console.


    :::python
    # test assumes django 1.6 and project called 'myproj'
    # also assumes this file is saved in myproj/myproj/test_logging.py,
    # ie in the same folder as settings.py
    from django.test import TestCase
    from django.conf.urls import url
    from unittest.mock import patch
    import logging
    import sys
    from django.http import HttpResponse
    from .urls import urlpatterns
    from .settings  import DEBUG # django.conf.settings are messed with by test runner


    def do_logging(request):
        # dummy view that tries to log at all levels, and then raises an exception
        logging.debug('debug logged')
        logging.info('info logged')
        logging.warning('warning logged')
        logging.critical('critical logged')
        raise Exception('arg')
    urls_with_logging_test = urlpatterns + [url(r'^testlogging/$', do_logging)]


    class LoggingTest(TestCase):

        def test_level(self):
            root_log_level = logging.getLogger().level
            if DEBUG:
                self.assertEqual(logging.getLevelName(root_log_level), 'DEBUG')
            else:
                self.assertEqual(logging.getLevelName(root_log_level), 'INFO')


        @patch('myproj.urls.urlpatterns', urls_with_logging_test)
        @patch('myproj.test_logging.sys.stderr')
        def test_logs_to_stderr(self, mock_stderr):
            try:
                self.client.get('/testlogging/')
            except:
                pass
            written = ''.join(c[0][0] for c in mock_stderr.write.call_args_list)
            print(written)
            self.assertIn('critical logged', written)
            self.assertIn('warning logged', written)
            self.assertIn('info logged', written)
            if settings.DEBUG:
                self.assertIn('debug logged', written)
            else:
                self.assertNotIn('debug logged', written)
            self.assertIn('arg', written, 'Could not see exception in logs')
            self.assertIn('do_logging', written, 'Could not see traceback info')



## Setting the base log level (if you want):

Here's what you need to add to *settings.py* if you want to set the log
level lower, so that, say, `logging.info` actually works.  You don't actually
need this to get the exception logging to work, but I discovered it while 
investigating this problem, so I thought I'd write it up here, since it's 
not obvious from the docs.

    :::python
    LOGGING = {
        'version': 1,
        'root': {'level': 'DEBUG' if DEBUG else 'INFO'},
    }

I have a feeling someone will tell me that resetting the root log level is a 
silly thing to do, but it does work.  By all means enlighten me if this isn't
a good idea.

## Using middleware to catch and log exceptions

Onto the real answer to this problem. Normally, to log an exception, you'd have
something like this

    :::python
    try:
        do_something_that_might_explode()
    except:
        logging.exception('Oh noes, it exploded')

And then `logging.exception` will automagically print a full traceback as well
as our little message.

But how to get this to just happen, by default, for any exceptions in our code?
The answer is what Django calls "middleware", code that can get run while handling
any request.


    :::python

    import logging

    class ExceptionLoggingMiddleware(object):

        def process_exception(self, request, exception):
            logging.exception('Exception handling request for ' + request.path)

Cf the [Django docs on
middleware](https://docs.djangoproject.com/en/1.6/topics/http/middleware/#process-exception),
but that's really all you need!

If this is saved to, say, *myproj/myproj/exception_logging_middleware.py*, you would
then add it to your project in *settings.py* by:


    :::python
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'myproj.exception_logging_middleware.ExceptionLoggingMiddleware',
    )

If you've actually used the test, you'll find it now passes.

## Summary

In summary "how do I get Django to log all exceptions to stderr", which seems such
a straightforward question, actually does involve several different components:

* the logging module, and Django's logging config
* Django's exception-handling middleware.

Whilst the former is where youd' go to choose *where* things get logged to
(eg stderr or a file), and what the minimum log level is, the latter is the
place you actually need to go to if you want to log exceptions. 

