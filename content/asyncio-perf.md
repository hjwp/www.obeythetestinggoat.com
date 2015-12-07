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

> Some wag recently said "

