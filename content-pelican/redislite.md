Title: Better tests for Redis integrations with redislite
Date: 2015-12-01 08:29
Tags: Redis, Mocks, integration tests
Author: Harry
Summary: How we replaced a bunch of ugly, mocky tests for our redis integration with redislite, and made them much better.

A colleague and I were staring at some ugly, mocky tests for our redis integration the other day, when I remembered someone at Pycon last year showing me a cool library called [redislite](https://github.com/yahoo/redislite) -- basically, a lightweight, self-contained, pip installable version of redis, that can be installed almost anywhere and run totally separately from the system redis.  (That was [Dwight](https://twitter.com/dwighthubbard), who I now realise is the main author of redislite.  Yay Pycon.)

He'd said "it's great for testing", so we thought we'd give it a go.

<img src="/static/images/pip_install_redislite.png" alt="console output from pip installing redislite"></img>
<caption><i>pip installs and compiles in 20 seconds</i></caption>

Here's the sample usage from the docs:

```python
>>> import redislite
>>> r = redislite.StrictRedis()
>>> r.set('foo', 'bar')
True
>>> r.get('foo')
'bar'
```

Couldn't be simpler!  You can initiate a lightweight version of redis just like that, have one for each test even, and throw it away at the end, without having to worry about ports, passwords, or any interaction with the system redis.


The code under test is meant to parse a web server log line, and then update some hit counts in redis.  Here's how our tests looked before:

```python

@patch('hit_counter.redis')
def test_write_to_redis_updates_appropriate_keys(self, mock_redis):
    write_to_redis('www.nowhere.com', datetime(2013, 11, 14, 16, 54, 21, 0), 2323)

    self.assertItemsEqual(
        mock_redis.method_calls,
        [
            call.incr('count|www.nowhere.com'),
            call.incr('count|www.nowhere.com|2013'),
            call.incr('count|www.nowhere.com|2013-11'),
            call.incr('count|www.nowhere.com|2013-11-14'),
            call.incr('count|www.nowhere.com|2013-11-14 16'),
            call.incr('count|www.nowhere.com|2013-11-14 16:54'),
            call.incrby('bytes|www.nowhere.com', 2323),
            call.incrby('bytes|www.nowhere.com|2013', 2323),
            call.incrby('bytes|www.nowhere.com|2013-11', 2323),
            call.incrby('bytes|www.nowhere.com|2013-11-14', 2323),
            call.incrby('bytes|www.nowhere.com|2013-11-14 16', 2323),
            call.incrby('bytes|www.nowhere.com|2013-11-14 16:54', 2323),
        ]
    )
```


And here's how they look after:


```python
class WriteToRedisTest(unittest.TestCase):

    def setUp(self):
        self.fake_redis = redislite.StrictRedis()
        self.patcher = patch('hit_counter.redis', self.fake_redis)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()


    def test_increments_all_counts(self):
        timestamp = datetime(2013, 11, 14, 16, 54, 21, 0)
        expected_counts = [
            'count|www.nowhere.com',
            'count|www.nowhere.com|2013',
            'count|www.nowhere.com|2013-11',
            'count|www.nowhere.com|2013-11-14',
            'count|www.nowhere.com|2013-11-14 16',
            'count|www.nowhere.com|2013-11-14 16:54',
        ]
        for key in expected_counts:
            self.fake_redis.set(key, 11)

        write_to_redis('www.nowhere.com', timestamp, 2323)

        for key in expected_counts:
            self.assertEqual(self.fake_redis.get(key), '12')


    def test_increments_all_bytes(self):
        timestamp = datetime(2013, 11, 14, 16, 54, 21, 0)
        expected_bytes = [
            'bytes|www.nowhere.com',
        # etc
```

Look at that!

* Instead of mocking the library, I'm mocking out a particular Redis instance, with a real, functioning redis that I have full control over

* I now no longer need to care about exactly how I use the redis API in my code -- no need to check whether I'm calling `incr` or `incrby`, I can just set an actual value before, and check the actual value after. It allows me to obey one of the key rules of testing, "test behaviour, don't test implementation".

The approach only continued to deliver benefits.  The reason we were looking at this code was because we wanted to start setting some expiry times on keys.  As a result of using redislite, the tests for expiry came out really sane and readable:

```python
def test_hourly_data_expires_after_one_week(self):
    timestamp = datetime(2013, 11, 14, 16, 54, 21, 0)
    write_to_redis('www.thing.com', timestamp, 123)
    ttl = int(self.fake_redis.ttl('count|www.thing.com|2013-11-14 16'))
    self.assertAlmostEqual(
        ttl,
        7 * 24 * 60 * 60,
        delta=2,
    )

```

Imagine that test with mocks! 

```python
    self.assertItemsEqual(
        mock_redis.method_calls,
        [
            call.incr('count|www.thing.com'),
            call.incr('count|www.thing.com|2013'),
            # ... 
            call.incr('count|www.thing.com|2013-11-14 16'),
            call.expire('count|www.thing.com|2013-11-14 16', expected_expiry),
            # and so on
```

Ugh. And that's glossing over the complexities of timestamping -- the `assertAlmostEqual` works nicely in the redislite tests, but here I'd have to either mock out `datetime`, or pull all of the `call` instances out of `.method_calls` one by one...  Oh I just don't even want to think about it.


So, remember kids, friends don't let friends use mocks when there's a better alternative around.  Definitely check out redislite if you ever find yourself writing some tests for a redis integration in your own codebase.

*[thanks to [Nicole](https://twitter.com/nlhkabu) for prompting me to write this post]*

