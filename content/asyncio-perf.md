Title: Testing, async, asyncio, and performance
Date: 2015-12-27 13:29
Tags: Async, asyncio, peformance
Author: Harry
Summary: An ill-advised experiment in process management ends up with interesting comparisons of different Python async frameworks, and some tests that work for all of them.

I recently did some experimenting with `asyncio`, and wanted to report back on
how I got on with writing tests for it.  While I was at it I was also able to
compare its performance with a couple of other approaches to mutlitasking in
Python, namely threads and gevent, so I'll report on that here too.  (tl;dr:
it's much of a muchness).


### "hobbling" naughty user processes

At [PythonAnywhere](https://www.pythonanywhere.com/) we have a "tarpit" where we
put users who exceed their usage limits.  Their processes still run, but
slower.  We use cgroups for this, and it works pretty well, but I was in a mean
mood and I wanted to see whether I could make our tarpit even more mean --
essentially "hobbling" naughty users's processes using OS stop and restart
signals.

In synchronous/pseudo code, something like this:

```python
def main():
    while True:
        naughty_processes = find_new_naughty_processes()
        for process in naughty_processes:
            hobble_process(process)  # parallelised somehow
        time.sleep(10)

def hobble_process(process):
    while True:
        try:
            os.kill(process.pid, signal.SIGSTOP)
            time.sleep(0.25)
            os.kill(process.pid, signal.SIGCONT)
            time.sleep(0.01)
```

Every 10 seconds, go fetch a list of "naughty" processes, and then "hobble"
each one of them, by using OS signals to stop and start the process at short
intervals.  The naughty program still runs, but its execution is suspended for
95% of the time.


### A first cut using asyncio

The only question was: how to do the "parallelise somehow" part.  Asyncio is
the hot new thing in the world of Python async stuff, and this seemed like a
good potential candidate -- I have a fairly simple algorithms, and there are
lots of places where I use "time.sleep", which are good places to give back
control to some sort of event loop or task manager.

And sure enough, my first cut of the same code with asyncio was pleasingly
similar to the normal procedural code -- I just add a few "yield froms" to
signify where each function can yield control back to the event loop, ready to
be woken up again when there's something for it to do:


```python
def main():
    loop = asyncio.get_event_loop()
    loop.create_task(hobble_processes_forever())
    loop.run_forever()


@asyncio.coroutine
def hobble_processes_forever():
    already_hobbled = set()
    while True:
        yield from hobble_current_processes(already_hobbled)
        yield from asyncio.sleep(2)


@asyncio.coroutine
def hobble_current_processes(already_hobbled):
    pids = yield from get_naughty_pids()
    for pid in pids:
        if pid in already_hobbled:
            continue
        already_hobbled.add(pid)
        asyncio.get_event_loop().create_task(
            hobble_process(pid)
        )


@asyncio.coroutine
def hobble_process(pid):
    while True:
        os.kill(pid, signal.SIGSTOP)
        yield from asyncio.sleep(0.2)
        os.kill(pid, signal.SIGCONT)
        yield from asyncio.sleep(0.01)
```

> feel free to skip this next section if you already know asyncio

What is a coroutine, I hear you ask?  Or, at least, I hear some of you ask.
I'm relying on the ones who don't ask to improve the amateurish definition that
follows. Ahem.  A coroutine is a function that defines some points at which
it's happy to suspend and resume execution, or wait until some data or device
becomes available. [wikipedia](https://en.wikipedia.org/wiki/Coroutine)

In asyncio, those places are marked by the `yield from` keywords, where the
function says: I know this next thing will take some time, I'm happy to wait
and let the rest of the program (as controlled by the event loop) get on with
something else.

As I learned while trying to build this thing, `yield from` on its own won't
make your code asynchronous (check out [this
gist](https://gist.github.com/hjwp/727c932ce3e20c6367e5) for an illustration).
You also need a special way of invoking functions that you want to start off
asynchronously, and that's the purpose of `create_task`.  `create_task` tells
the event loop to start a function "in the background".

### testing async code with a functional test

Once I'd more or less wrapped my head around that, and built a prototype that
works, I started to think about testing. Or, how to turn my manual testing into
automated testing

> Some wag recently said "When people tell me they don't do TDD, I usually see
> them driving development with a bunch of manual tests which they're going to
> throw away, instead of automating them.

It felt like some "real" tests were in order, tests that would actually start
some real processes and see if they really did get slowed down -- an end-to-end
test, if you will -- so that's what I went for.  Here was my first cut:

```python
def test_hobbled_process_is_slow(tarpit_pids_file, start_hobbler_in_subprocess):
    timer = "; ".join([
        "import time",
        "time.sleep(0.4)",  # give hobbler a chance to spot us
        "start = time.time()",
        "list(range(int(1e6)))",  # do some work
        "print(time.time() - start)",
    ]
    normal = subprocess.check_output(['python', '-c', timer])

    add_self_to_tarpit = (
        "import os;"
        " open({pidsfile}, 'w').write(str(os.getpid()));"
    ).format(pidsfile=tarpit_pids_file)
    slow = subprocess.check_output(
        [ 'python', '-c', add_self_to_tarpit + " "  + timer],
    )

    normal = float(normal)
    slow = float(slow)
    assert normal < slow
    assert normal * 10 < slow
    assert normal * 100 > slow
```

The test depends on two fixtures, one to create a file containing process ids
(pids) that we want to hobble, and one to actually launch the hobbler.py process


```python
@pytest.yield_fixture
def tarpit_pids_file():
    yield tempfile.NamedTemporaryFile()


@pytest.yield_fixture
def start_hobbler_in_subprocess(tarpit_pids_file):
    process = subprocess.Popen(
        ['python3', 'hobbler.py', tarpit_pids_file],
        stdout=subprocess.PIPE, stdin=subprocess.PIPE, 
        stderr=subprocess.STDOUT, universal_newlines=True
    )
    first_line = process.stdout.readline()
    if 'Traceback' in first_line:
        raise Exception(process.stdout.read())

    yield process

    process.kill()
    print('full hobbler process output:')
    print(process.stdout.read())
```

> If you're not familiar with py.test fixtures, they're like things you might put
> in a unittest setUp / tearDown; special functions that get called with each test
> that names them as an argument.  The `yield` pattern I'm using here allows me to
> inject a resource into the test.


Running the code under test as a totally separate Python process has two
benefits -- first, it lets me test the program as it will actually be used,
and secondly, it neatly sidesteps one of the difficulties of testing async code,
which is how to deal with the event loop itself, which has to be launched as a
blocking call..

From that point onwards, I found it was relatively easy to use similar tests
to drive my development, alongside a few manual checks. Here's my final list
of tests:

```python
def test_tarpit_process_is_slow(fake_tarpit, hobbler_process):
def test_spots_process(fake_tarpit, hobbler_process):
def test_spots_multiple_processes(fake_tarpit, hobbler_process):
def test_doesnt_hobble_any_old_process(fake_tarpit, hobbler_process):
def test_stops_hobbling_dead_processes(fake_tarpit, hobbler_process):
def test_hobbles_children(fake_tarpit, hobbler_process):
def test_lots_of_processes(fake_tarpit, hobbler_process):
def test_get_top_level_processes_returns_list_of_parents_and_with_chidren():
```

You can explore these, and the implementation, in the 
[repo on GitHub](https://github.com/hjwp/process-hobbler-experiment)


### Performance comparison:  aysncio vs gevent vs threads

Maybe the most interesting test was the "lots of processes" test, which is a
performance test -- since the hobbler is meant to reduce the load on our
servers, by reducing the resource usage of user processes, it's important that
the hobbler itself shouldn't chew up all the CPU!  So I wanted to see how it
performs with lots of processes to hobble:


```python
def test_lots_of_processes(fake_tarpit, hobbler_process):
    start_times = Process(hobbler_process.pid).cpu_times()
    print('start times', start_times)
    procs = []
    for i in range(200):
        p = subprocess.Popen(['sleep', '100'], universal_newlines=True)
        _add_to_tarpit(p.pid, fake_tarpit)
        procs.append(p)

    time.sleep(7) # time for 3 iterations

    end_times = Process(hobbler_process.pid).cpu_times()
    print('end times', end_times)

    assert end_times.user > start_times.user
    assert end_times.system > start_times.system

    Process(hobbler_process.pid).cpu_percent(interval=0.1)  # warm-up
    assert Process(hobbler_process.pid).cpu_percent(interval=2) < 10
```

All that boils down to starting 100 processes, telling the hobbler to hobble
all of them, and then measuring the CPU usage of the hobbler -- I wanted it to
be less than 10% of CPU. Unfortunately, it was far from that, taking up over
100% CPU in my first test.

So I thought I'd compare asyncio with a couple of other popular Python
multitasking solutions: 
[gevent](http://www.gevent.org/) and plain old
[threads](https://docs.python.org/3/library/threading.html)

Switching from asyncio to gevent was actually very simple -- their programming patterns are
quite similar -- a matter of changing a few `aysncio.sleep`s to `gevent.sleep`s,
and `loop.create_task`s to `gevent.spawn`s:


```diff
-            yield from asyncio.sleep(0.01)
+            gevent.sleep(0.01)
 
-        loop.create_task(
-            hobble_process_tree(parent)
-        )
+        gevent.spawn(hobble_process_tree, parent)

-        yield from hobble_current_processes(loop, already_hobbled, cgroup_dir)
+        gevent.spawn(hobble_current_processes, already_hobbled, cgroup_dir)
```

Check out the full diff here, if you're curious:

* [https://github.com/hjwp/process-hobbler-experiment/commit/gevent](https://github.com/hjwp/process-hobbler-experiment/commit/gevent)

It turns out that didn't buy me any real performance improvement though.  So I
thought I'd try good ol' fashioned threads

```diff

-            yield from asyncio.sleep(0.01)
+            time.sleep(0.01)

-        loop.create_task(
-            hobble_process_tree(parent)
-        )
+        threading.Thread(
+            target=lambda: hobble_process_tree(parent)
+        ).start() 
```

Again, not a massive change to the programming model -- a `loop.create_task` becomes
a `Thread().start()`, and the `asyncio.sleep()` can just be a normal `time.sleep()`,
since we're off the main thread.

Check out the full diff here if you're curious

* [https://github.com/hjwp/process-hobbler-experiment/commit/threads](https://github.com/hjwp/process-hobbler-experiment/commit/threads)


But, performance-wise, it was no better.  Worse, in fact!


### Final test results:  asyncio vs gevent vs threads

> WARNING: NO SCIENCE HERE!

This is the results of just a single run on a single machine, not to be taken
as a general indication of the true, intrinsic performance characteristics of
any of these libraries, etc etc.

<table>
<tr><th> Library </th>    <th> CPU usage  </th></tr>
<tr><td> asyncio: </td>   <td> 85.4  </td></tr>
<tr><td> gevent:  </td>   <td> 100.4 </td></tr>
<tr><td> threading: </td> <td> 172.8 </td></tr>
</table>

Feel free to try and replicate these tests yourself, using the code [here](https://github.com/hjwp/process-hobbler-experiment/commits/master)


### Call to action (1): can this be made more efficient?

I'm inclined to think that this whole process hobbler was just a bad idea, but
maybe you know more about multitasking stuff, and you can see some obvious
improvements for my code, or have some suggestions for different approaches?
Any thoughts on the theoretical reasons for why asyncio should seem so much 
quicker than threads in this instance? Answers on a postcard please...


### Call to action (2): better ways of testing async code and/or process behaviour?

I use functional tests here for a few reasons:

* The code under test crosses a lot of system boundaries -- it affects other
  processes, it relies on operating system signals, and it reads from a file.
  At least one end-to-end / integrationey test felt necessary.  (this feels
  like a good reason)

* Once I'd started, it was easier to just continue in that model, rather than
  figure out the subtleties of factoring out my code for testability, dealing
  with testing the event loop, and mocking all the different layers involved.
  This, maybe, is a bad reason.

The price I paid was a fairly slow test suite -- the basic test of process hobbling
takes 8 or 9 seconds, and any of the other tests still take on the order of a second,
since they involve writing to a temp file, starting a hobbler process and a test process,
waiting for the hobbler to do something, and cleaning up.  The performance test takes a
a good 30 seconds on its own.

The tests are also a little more flakey than I'd like -- the exact amount that
a process gets hobbled is subject to quite a lot of random noise, so just
checking that it's "between 10 and 100 times slower" is a bit more vague than
you might want, and it took me a while to set up the test in such a way that it
reliably passed and failed as appropriate.

On the other hand, of course, I get the benefit you always get from a functional test,
which is that I'm sure my system really does work.

So, I'd be interested -- would you write this test suite differently?  Can you see any
candidates for more "unitey" tests?

You'll see I already made a start on a slightly more isolated test that aims at just
the `get_top_level_processes` function.  The other main candidate that seems like it
could do with a better, more granular test is `hobble_process_tree` function.
Specifically, it's important that the process tree should be hobbled in the
correct order, starting with the top level, then down to children, then
children's children, and so on, and then re-started in the reverse order,
starting from the bottom-level processes and going back up to the top.
(otherwise, if you're hobbling a users' interactive console session, which has
a nested tree of, say, bash and ipython, the user sees really weird things if
you pause the ipython before the bash.)

That's not well tested at the moment.  Can you think of a way of doing so which can handle
the interspered asyncio `yield from`s, and that still feels like testing
behaviour, not implementation?
 
