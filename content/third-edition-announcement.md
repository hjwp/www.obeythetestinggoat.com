Title: Progress on the Third Edition of the Book!
Date: 2024-08-07 16:13
Tags: Book, third edition, Django
Author: Harry
Summary: I never announced it on this blog, but I've been working on a 3e for the book, updated for the latest Django and Python.  Progress is good so far, I've updated all but 4 of the main chapters, including some major rewrites of the deployment chapters to use Docker and Ansible.

In lieu of a formal announcement about the Third Edition, how about a progress update?


## Core technology updates: Django + Python

> Embarrassment-Driven Development

One of the main motivations for a third edition was that the 2e is based on Django 1.11,
which dropped out of support back in 2017, and that's been a big turnoff for readers for a while,
and quite embarrassing really.

So, the plan is to upgrade to Django 5.x, and progress is good -- I've already updated
most of the core chapters to Django 4.2, and upgrade Python to 3.12 while I was at it.
Django 5 is next, and I'm hoping/assuming it will be a smaller leap that 1->4 was,
so that won't be far behind.


## New Deployment Technologies:  Docker + Ansible

I've always been proud that the book includes several chapters on how to actually deploy our app
to production, and make the app live on the actual public Internet.
But the deployment process from the first and second editions--broadly speaking,
SSH in to your server, hack about to figure out how to get your app deployed manually,
and then automate what you did with glorified shellscripts, aka Fabric--was starting
to look less and less like what modern deployment looks like, or my experience of it at least.

I uhmmed and ahhed about it for a while, but in the end I decided to go with a deployment
process that looks like this:

* Package up our app into a Docker container, and use our tests to confirm it really works
* Use Ansible to automate pushing that container onto a server and running it.

Check out the latest version of the deployment chapters here:

* [Chapter 9: Containerization aka Docker](/book/chapter_09_docker.html)
* [Chapter 10: Making our App Production-Ready](/book/chapter_10_production_readiness.html)
* [Chapter 11: Infrastructure As Code: Automated Deployments With Ansbile](/book/chapter_11_ansible.html)

I think I like how it's turned out,
a lot of the fiddliness and debugging of deployment/production-readiness can now happen locally
(in Docker containers on your own machine),
so I think that tightens and speeds up the feedback loop a fair bit.


## JavaScript

The Javascript chapter was another head-scratcher.
I wanted to move away from QUnit, and include some more modern/ES6 syntax.
In the end, I decided to go with Jasmine, which is old but still popular,
but to keep the browser-based test runner, which is a bit of an unconventional choice,
but it does mean we can avoid the whole Node.js and `node_modules` learning curve.

Aside from that, I've wound down the "JavaScript is such a nightmare" jokes,
because they're really not fair any more, and were probably never that funny besides.

Check out the new version here:

* [Chapter 16: A Gentle Excursion Into JavaScript](/book/chapter_16_javascript.html)

## Some changes of emphasis

The other main changes to the book are going to be around how
I talk about some of the tradeoffs involved in the use of mocking,
and unit vs integration vs functional/e2e tests.
I think the first and second editions were perhaps a little too opinionated on this front
(I still cringe to think how defensive I was when I first wrote the [Hot Lava](/book/chapter_hot_lava.html) chapter, sorry CaseY!!),
and my thinking has evolved a lot since I wrote my [second book](https://www.cosmicpython.com/) with Bob.

That's still very much on the drawing board though,
so you'll have to watch this space for updates on that front.


Anyways, all the latest versions of the 3e chapters are live here on the site,
and also as an [Early Release on O'Reilly Learning](https://learning.oreilly.com/library/view/test-driven-development-with/9781098148706/),
so do dive in and let me know what you think!

