Title: Testing, async, asyncio, and performance
Date: 2015-12-05 14:29
Tags: Async, asyncio, peformance
Author: Harry
Status: draft
Summary: An ill-advised experiment ends up with interesting comparisons of different Python async frameworks, and some tests that work for all of them.

I recently did some experimenting with asyncio, and wanted to report back on
how I got on with writing tests for it.  While I was at it I was also able to
compare its performance with a couple of other approaches to mutlitasking in
Python, namely threads and gevent, so I'll report on that here too.  (tl;dr:
much of a muchness).

At [PythonAnywhere](https://www.pythonanywhere/) we have a "tarpit" where we
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
90% of the time.

The only question was: how to do the "parallelise somehow" part.  Asyncio is
the hot new thing in the world of Python async stuff, and this seemed like a
good potential candidate -- I have a fairly simple algorithms, and there are
lots of places where I use "time.sleep", which are good places to give back
control to some sort of event loop or task manager.

And sure enough, my first cut of the same code with asyncio was pleasingly similar
to the normal procedural code -- I just add a few "yield froms" to signify where
each function can yield control back to the event loop, ready to be woken up again
when there's something for it to do:


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
    pids = yield from get_pids()
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

What is a coroutine, I hear you ask.  Or, at least, I hear some of you ask.
I'm relying on the ones who don't ask to improve the amateurish definition that
follows. Ahem.  A coroutine is a function that defines some points at which
it's happy to suspend and resume execution, or wait until some data or device
becomes available. [wikipedia](https://en.wikipedia.org/wiki/Coroutine)

In asyncio, those places are marked by the `yield from` keywords, where the
function says: I know this next thing will take some time, I'm happy to wait
and let the rest of the program (as controlled by the event loop) get on with
something else.

As I learned while trying to build this thing, `yield from` on its own won't
make your code asynchronous however (check out [this
gist](https://gist.github.com/hjwp/727c932ce3e20c6367e5) for an illustration).
You also need a special way of invoking functions that you want to start off
asynchronously, and that's the purpose of `create_task`.  `create_task` tells
the event loop to start a function "in the background".

Once I'd more or less wrapped my head around that, and built a prototype that
works, I started to think about testing. Or, how to turn my manual testing into
automated testing

> Some wag recently said "when people tell me they don't do TDD, I usually see
> them driving development with a bunch of manual tests which they're going to
> throw away, instead of automating them.

It felt like some "real" tests were in order, tests that would actually start
some real processes, so that's what I went for.  Here was my first cut:

```python
def test_hobbled_process_is_slow(tarpit_pids_file, start_hobbler_in_subprocess):
    timer =  (
        "import time; time.sleep(2.1);"
        " start = time.time();"
        " list(range(int(1e6)));"
        " print(time.time() - start)"
    )
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
    assert normal * 20 < slow
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
        stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
    )
    first_line = process.stdout.readline()
    if 'Traceback' in first_line:
        raise Exception(process.stdout.read())

    yield process

    process.kill()
    print('full hobbler process output:')
    print(process.stdout.read())
```

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
def test_lots_of_processes(fake_tarpit, nontesting_hobbler_process):
def test_get_top_level_processes_returns_list_of_parents_and_with_chidren():
```

You can explore these, and the implementation, in the [repo on GitHub](https://github.com/hjwp/process-hobbler-experiment)

Maybe the most interesting test was the "lots of processes" test, which is a
performance test -- since the hobbler is meant to reduce the load on our
servers, by reducing the resource usage of user processes, it's important that
the hobbler itself shouldn't chew up all the CPU!  So I wanted to see how it
performs with lots of processes to hobble:


```python
def test_lots_of_processes(fake_tarpit, nontesting_hobbler_process):
    start_times = psutil.Process(nontesting_hobbler_process.pid).cpu_times()
    print('start times', start_times)
    procs = []
    for i in range(200):
        p = subprocess.Popen(['sleep', '100'], universal_newlines=True)
        _add_to_tarpit(p.pid, fake_tarpit)
        procs.append(p)

    time.sleep(7) # time for 3 iterations

    end_times = psutil.Process(nontesting_hobbler_process.pid).cpu_times()
    print('end times', end_times)

    assert end_times.user > start_times.user
    assert end_times.system > start_times.system

    psutil.Process(nontesting_hobbler_process.pid).cpu_percent(interval=0.1)  # warm-up
    assert psutil.Process(nontesting_hobbler_process.pid).cpu_percent(interval=2) < 10
```

All that boils down to starting 100 processes, telling the hobbler to hobble all of them, and then measuring the CPU usage of the hobbler -- I wanted it to be less than 10% of CPU.

You

Unfor

https://github.com/hjwp/process-hobbler-experiment/commit/gevent
https://github.com/hjwp/process-hobbler-experiment/commit/threads

Test results:

<table>
<tr><td> asyncio: </td><td> 65.4  </td></tr>
<tr><td> gevent:  </td><td> 100.4 </td></tr>
<tr><td> Threads: </td><td> 172.8 </td></tr>
</table>


* Any experience with async?  what should i change?
* I use e2e tests out of laziness, or maybe ignorance.  Are you a unit test enthusiast?  How would you rewrite this test suite to be more unit-ey?





