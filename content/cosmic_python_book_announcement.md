Title: Cosmic Pyhton
Date: 2020-06-03
Tags: architecture, design, ddd
Author: Harry
Summary: Announcing a new book, "Architecture Patterns with Python", aka Cosmic Python

Folks I've written a new book!

Along with my coauthor [Bob](https://twitter.com/bob_the_mighty), we are proud
to release "Architecture Patterns with Python", which you can find out more
about at [cosmicpython.com](https://www.cosmicpython.com).

The cosmic soubriquet is a little joke, _Cosmos_ being the opposite of _Chaos_
in ancient Greek, so we want to propose patterns to minimise chaos in your
applications.

But the subtitle of the book is _Enabling TDD, DDD, and Event-Driven
Microservices_, and the TDD part is relevant to this blog, and fans of the
Testing Goat.  In my two years at MADE and working with Bob, I've refined
some of my thinking and some of the ways I approach testing, and I think
if I were writing TTDwP again today, I might change the way I present some
things.

In brief:

* Mocking is not the only way to handle external (I/O et al) dependencies
  for your unit tests.  Other techniques are possible, and often offer
  major benefits

* If you really want to get to a test pyramid (where unit tests outnumber
  slow/e2e/integration tests by an order of magnitude), then you'll probably
  need to make some specific design choices around identifying business logic
  and decoupling it from infrastructure code.

* When deciding what kind of unit tests to write, there's a lot to be said for
  writing them at the highest level of abstraction possible.  It gives you more
  room to refactor later.

If you're curious about those questions, head on over to [cosmicpython.com](https://www.cosmicpython.com),
and let me know what you think!
