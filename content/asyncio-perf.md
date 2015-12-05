Title: Testing, async, asyncio, and performance
Date: 2015-12-05 14:29
Tags: Async, asyncio, peformance
Author: Harry
Status: draft
Summary: An ill-advised experiment ends up with interesting comparisons of different Python async frameworks, and some tests that work for all of them.

At [PythonAnywhere](https://www.pythonanywhere/) we have a "tarpit" where we put users who exceed their usage limits.  Their processes still run, but slower.  We use cgroups for this, and it works pretty well, but I was in a mean mood and I wanted to see whether I could make our tarpit even more mean -- essentially "hobbling" naughty users's processes using OS stop and restart signals.

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
    loop.create_task(hobble_processes_forever(loop))
    loop.run_forever()
    loop.close()


@asyncio.coroutine
def hobble_processes_forever(loop):
    already_hobbled = set()
    while True:
        yield from hobble_current_processes(loop, already_hobbled)
        yield from asyncio.sleep(2)


@asyncio.coroutine
def hobble_current_processes(loop, already_hobbled):
    pids = yield from get_pids()
    for pid in pids:
        if pid in already_hobbled:
            continue
        already_hobbled.add(pid)
        loop.create_task(hobble_process(pid))


@asyncio.coroutine
def hobble_process(pid):
    while True:
        os.kill(pid, signal.SIGSTOP)
        yield from asyncio.sleep(0.2)
        os.kill(pid, signal.SIGCONT)
        yield from asyncio.sleep(0.01)
```

