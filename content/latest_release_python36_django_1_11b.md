Title: Latest release (the last big one?): Python 3.6, Django 1.11 beta
Date: 2017-03-13 06:12
Tags: Book, second edition, Python 3, Django
Author: Harry
Summary: The last big update has landed!  The book is now fully upgrade to Python 3.6, and the only version of Django that supports it, 1.11 beta.  f-strings a go-go, and a few other nice improvements too.


Hi all!  A brief overview of changes in the latest version, with hopefully a few
pointers for people half-way through the book and looking to adapt.


## Python 3.6 and Django 1.11b: minimal changes, other than f-strings

The main feature in Python 3.6 that's made an impact (for the book and,
arguably, elsewhere)
is [f-strings](https://docs.python.org/3/whatsnew/3.6.html#pep-498-formatted-string-literals).

I have to say when I first heard of them I was pretty skeptical, they sounded
a bit like YOLO-ing `**locals()` all over your code, scary, but those concerns
have occurred to the brighter minds than mine that develop Python, and they figured
there was nothing truly to be scared about, so I should relax.

I'll tell you what really made me relax, which was using them!  I can't count
the number of times I replaced a 3-line `string.format()` or an incoprehensible
`%s` substitution with an f-string one-liner, and felt my code was nicer and
more readable as a result.

The move to 3.6 also forced me to upgrade to [Django
1.11](https://docs.djangoproject.com/en/dev/releases/1.11/) at the same time,
since it's the only version of Django that officially supports Python 3.6,
and that was pretty much entirely painless too.  No major code changes
as a result, and since it's going to be an LTS, I'm hoping I'll be able to
stick with it for a long while over the lifetime of this 2e of the book.


## Other minor improvements: fabric3

While I was at it I decided to upgrade to a Python 3 fork of fabric (thanks
to all the readers who encouraged me to do so), and that saves us from a
pretty awkward hop via subprocess to Python 2.  Here's the old ascii-art diagram,
preserved for posterity:


```
## Locally:

MyListsTest
.create_pre_authenticated_session  →   .management.commands.create_session
                                       .create_pre_authenticated_session

## Against staging:

MyListsTest
.create_pre_authenticated_session      .management.commands.create_session
                                       .create_pre_authenticated_session
     ↓
                                                      ↑
server_tools
.create_session_on_server                run manage.py create_session

     ↓                                                ↑
subprocess.check_output    →    fab   →   fabfile.create_session_on_server
```

*the old, bad way of doing it*


That's now much neater in the [server-side debugging
chapter](/book/chapter_server_side_debugging.html).  Huge thanks to the
[fabric3 developers](https://github.com/mathiasertl/fabric/).



## What to do if you're half-way through the book

I'm always a fan of upgrading!   Because the changes are all quite minor,
you *should* be able to just:

* Install Python 3.6 (downloadable on windows + macos, can use
  [deadsnakes ppa](https://launchpad.net/~fkrull/+archive/ubuntu/deadsnakes) on Ubuntu)

* `rmvirtualenv superlists`

* re-create the virtualenv with Python 3.6 (see the 
  [pre-reqs chapter](/book/pre-requisite-installations.html#_setting_up_your_virtualenv)
  for help, particularly on windows)

* `pip install django==1.11b1 selenium fabric3`


## What about Selenium 3?

If you actually started the book before Jan 30th or so, and you haven't made the upgrade
to Selenium 3 yet, that's a bigger deal, and for that I'd recommend starting again at the
beginning of the book.  Don't worry, you'll zip through the chapters much quicker the
second time, and it should really help bed in the learning.


## What did I miss?

Honestly, it does feel like it was all a bit too easy.  Is there anything I missed?
Any new features from Python 3.6 or Django 1.11 that you think I should have included
in the book?  Let me know!

Thanks, as ever, for reading.

