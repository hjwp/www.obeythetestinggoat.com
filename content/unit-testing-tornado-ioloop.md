Title: How to unit test tornado ioloop callbacks
Date: 2013-06-10 19:11
Tags: tornado, async
Author: Harry
Summary: A quick guide to how to write tests for the tornado ioloop, since the official docs can still leave one a little baffled.

*WARNING: this is not battle-tested wisdom of a massively experienced tornado
tester. Today was the first time we ever tried to test something that actually
uses the ioloop, and we've probably got it all totally backwards.  Still, in
case it helps...*

Async. It's always hard to wrap your head around, so perhaps it's not
surprising that it took us a few goes at [work](http://www.pythonanywhere.com)
today before we got the hang of it.

Here's a bit of code that adds a callback to the tornado ioloop:

    :::python
    def sort_that_out(mess):
        IOLoop.instance().add_callback(mess.sort)


How might one naively write a test for it?

    :::python
    class TestSortingStuffOut(unittest.TestCase):

        def test_stuff_get_sorted(self):
            stuff = [3,2,1]
            sort_that_out(mess)
            self.assertEqual(mess, [1, 2, 3])

Well, that doesn't work: 

    AssertionError: Lists differ: [3, 2, 1] != [1, 2, 3] 

A little head-scratching will get you to the fact that it's because the tornado
IOLoop hasn't actually been started, so our callback never gets run.  So, let's fix that:


    :::python
    def test_stuff_get_sorted(self):
        stuff = [3,2,1]
        sort_that_out(stuff)
        IOLoop.instance().start()
        self.assertEqual(stuff, [1, 2, 3])

What about now?  The test hangs, and a little Ctrl-C based profiling tells us where the
busy loop is:


```
  File "/tmp/t.py", line 13, in test_stuff_get_sorted     
    IOLoop.instance().start()
  File "/usr/local/lib/python2.7/site-packages/tornado/ioloop.py", line 627, in start
     event_pairs = self._impl.poll(poll_timeout) 
KeyboardInterrupt 
```

Right.  `start()` on the IOLoop is a blocking call, and just assumes the loop should 
be run forever.  At this point we ventured over to the [official tornado
testing docs](http://www.tornadoweb.org/en/stable/testing.html) but they seem
to suggest a lot of overcomplicated things: using a `self.wait`, overriding
`get_new_ioloop` to return the singleton...

Actually, all you really need to do is this:

    :::python
    def test_stuff_get_sorted(self):
        stuff = [3,2,1]

        sort_that_out(stuff)

        IOLoop.instance().add_callback(IOLoop.instance().stop)
        IOLoop.instance().start()

        self.assertEqual(stuff, [1, 2, 3])

We just add our own callback, telling the loop to shut itself down, making sure
that it's the last callback added before we start the loop.  Voila!

```
.
 ---------------------------------------------------------------------- 
Ran 1 test in 0.001s

OK 
```


Well, that was our first foray into writing a test for tornado that actually used the IOLoop 
(all our other tests have just mocked everything).  No doubt the tornado tools come in useful
for other use cases.  And you'd probably want to use a `tearDown` or `addCleanup` that made 
sure the IOLoop got shut down even when your test doesn't behave as expected....

But I though I'd post this in case anybody else has a simple requirement to
test a tornado async callback, and finds the docs a little hard-going. Hope it helps!

