Title: Speeding up Django unit tests with SQLite, keepdb and /dev/shm
Date: 2017-11-23 18:32
Tags: Django, Tests, Sqlite
Author: Harry
Summary: Want to speed up your Django tests?  Tell Django to use the special in-memory filesystem at /dev/shm and skip recreating the database...


Here's the tldr version:

```python
DATABASES = {
    'default': {
        'ENGINE': 'your db settings as normal',
        [...]
        'TEST': {
          # this gets you in-memory sqlite for tests, which is fast
          'ENGINE': 'django.db.backends.sqlite3',
        }
    }
}

if 'test' in sys.argv and 'keepdb' in sys.argv:
    # and this allows you to use --keepdb to skip re-creating the db,
    # even faster!
    DATABASES['default']['TEST']['NAME'] = '/dev/shm/myproject.test.db.sqlite3'
```


## More context

For day-to-day development, running your tests needs to be as fast as possible to
keep you in a good workflow.  Although you're unlikely to be using SQLite as your
production database, using it for tests in dev is often a nice shortcut, particularly
since Django will use an in-memory sqlite database for tests, which is even
faster than one on disk.

But, especially if you have a large and complicated database, re-creating it with each
test run can take quite a bit of time. That's where the `--keepdb` step comes in.  Of
course, normally if you're using an in-memory database, `keepdb` doesn't make
any sense because memory disappears between runs.  That's where the sneaky
trick of using */dev/shm* comes in.  In linux, */dev/shm* is actually a
filesystem against your machine's RAM, and it will persist between processes,
until you reboot your machine.

So you get all the speed of an in-memory SQLite database, with the extra boost of not
having to re-create the database.


## What if the database changes,

... I hear you ask?  Django is smart enough to apply any new migrations to the
`keepdb` database if it notices them.
[Docs here](https://docs.djangoproject.com/en/1.11/ref/django-admin/#cmdoption-test-keepdb).
This works pretty well in my experience, although I have had to blow away the test
db in */dev/shm* manually once or twice...


## Don't do this in CI

But I'm only advocating this for use in development!  Ultimately, Postgres or whichever
database you're using will behave differently from SQLite.  Django does a good job of
abstracting away 90% of those differences, but that still leaves plenty of strange edge
case behaviours to do with default values, ordering and transactions that can easily trip
you up.

Make sure you always run your test suite in CI against the real database.

You could use an environment variable for example, to make sure:

```python
if os.environ.get('CI'):
    del DATABASES['default']['TEST']
```


## Some numbers:


Here's a subset of the PythonAnywhere tests running, first without keepdb:

```
»»»» time ./manage.py test console
Creating test database for alias 'default'...
................................................................................
................................................................................
...........................................................
----------------------------------------------------------------------
Ran 219 tests in 5.261s

OK
Destroying test database for alias 'default'...
10.86user 0.25system 0:11.12elapsed 99%CPU 
```

And now with keepdb:

```
»»»» time ./manage.py test console --keepdb
Using existing test database for alias 'default'...
................................................................................
................................................................................
...........................................................
----------------------------------------------------------------------
Ran 219 tests in 5.557s

OK
Preserving test database for alias 'default'...
6.28user 0.36system 0:06.66elapsed 99%CPU 
```

Notice the time that Django reports is the almost the same in both cases, but the
actual elapsed time is quite different -- that's because Django isn't counting time
spent re-creating the database at the beginning of the test run.

(also, be aware if you're running your own tests here that you will only see an
improvement the *second* time you run with `keepdb`.  On the first run it's still
creating the database)


## Your mileage may vary

On a different project with simpler models I see very different results:

```
»»»» time ./manage.py test opera.tests.test_pages
[...]
Ran 65 tests in 7.620s
15.44user 0.08system 0:15.53elapsed 99%CPU

»»»» time ./manage.py test opera.tests.test_pages --keepdb
[...]
Ran 65 tests in 7.535s
14.91user 0.10system 0:15.02elapsed 99%CPU
```


Really not that much in it!  Although that's on my laptop with a nice fast
processor and SSD. Differences are more pronounced (on both projects) on a
system with a slower CPU and filesystem:

```
$ time ./manage.py test opera.tests.test_pages
Creating test database for alias 'default'...
[...]
Ran 65 tests in 13.620s
real    0m25.720s

$ time ./manage.py test opera.tests.test_pages --keepdb
Using existing test database for alias 'default'...
[...]
Ran 65 tests in 10.648s
real    0m20.632s
```


## Linux only!

*/dev/shm* only exists on Unixey operating systems. A bit of googling might help you
find alternatives on Windows and MacOS though -- I can't vouch for these, but here are
the first two links I found while duckduckgoing:

* https://stackoverflow.com/questions/2033362/does-os-x-have-an-equivalent-to-dev-shm#2033417 
* https://stackoverflow.com/questions/3011464/what-is-the-dev-shm-equivalence-in-windows-system 



## More tips

* Changing the password hashing algorithm (for tests only) can speed up user creation.
  [This, and more tips, here](http://www.daveoncode.com/2013/09/23/effective-tdd-tricks-to-speed-up-django-tests-up-to-10x-faster/).

* If you really want to use Postgres on your dev machine, you can also 
  [hack your postgres config to speed things up](https://stackoverflow.com/questions/9407442/optimise-postgresql-for-fast-testing),
  although, again, you'd want to make sure your config in CI was more
  (exactly?) like production.


Let me know if these help you!

