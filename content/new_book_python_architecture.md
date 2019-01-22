Title: Announcing the next book: Lightweight Architecture Patterns with Python
Date: 2019-01-22 10:33
Tags: book, architecture, design
Author: Harry
Summary: I'm working on a new book that picks up where the last one left off -- how to structure your code to be able to get the most out of your tests, and manage complexity over time.


## How should we structure an application to get the most out of our tests?

At the [end of the last book](https://www.obeythetestinggoat.com/book/chapter_hot_lava.html)
I concluded on a chapter discussing how to get the most out of your tests, on
the tradeoffs between unit, integration and end-to-end tests, and made some
vague, flailing gestures towards topics I didn't really understand: _ports and
adapters_, _hexagonal architecture_, _functional core imperative shell_, the
_clean architecture_, and so on.

Since then I've been lucky enough to fall in with a [tech team](https://io.made.com/)
that are actively implementing these sorts of patterns, in Python.  And the
thing is, these architectural patterns are nothing new, people have been
exploring them for years in the world of Java and C#.  They were just new to
me... and I may be over-reaching from my own experience here, but they are
perhaps new to the Python community in general.

But as we mature, as what were once small projects and plucky startups turn
into complex business and (whisper it) enterprise software, and bringing
across some of this knowledge feels timely.

I came to it initially from the angle of testing, and the right kind of
architecture really can help you to get the most out of your tests, by
separating out a core of business logic (the "domain model") and freeing it
from all infrastructure dependencies, allowing it to be tested entirely through
fast, flexible unit tests.  It finally felt like the 
[test pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) was
an achievable goal rather than an impossible aspiration.

But it's really about much more than testing.  It's about managing complexity
in software, over time.

## Bob

Despite the full power of Dunning-Kruger and the Expert Beginner syndrome, I
couldn't write this book on my own.  Thankfully, Bob, the architect at 
[made.com](https://www.made.com/) is my coauthor.  I mean, it's pretty much
going to be his book, and I'm just a glorified editor / project manager
really, and my job is to nag Bob enough, suck all the knowledge out of
his head, and get it committed to the page.


## "Lightweight Architecture Patterns with Python".  Probably.

We're still bikeshedding the title (by all means send your suggestions), but
I want to convey something about keeping these architectural patterns Pythonic.
All the classic books ([Evans on DDD](https://domainlanguage.com/ddd/) and 
[Fowler on Architecture Patterns](https://www.martinfowler.com/books/eaa.html),
which _everyone should read_) have their examples in Java, and if you're anything
like me, then wading through all that `public static void main AbstractFactoryManager`
gubbins does get a bit wearing.

But it's more than just avoiding boilerplate, we want to show how, once you let
go of "everything has to be an object", then you can implement these patterns
in a lightweight, readable, natural way.  You should never implement an architectural
design pattern without clearly understanding why you're doing it and whether it's
worth it for your use case, but at least in Python, they don't have to be too ugly.


## Planned outline

* Chapter 1: Domain modelling, and why do we always make it so hard for ourselves?
* Chapter 2: Persistence and the repository pattern
* Chapter 3: A web API.  Flask as a port (as in ports-and-adapters). Our first use case.  Orchestration. Service layer
* Chapter 4: Data integrity concerns 1: unit of work pattern
* Chapter 5: Data integrity concerns 2: choosing the right consistency boundary (Aggregate pattern)
* Chapter 6: CQRS
* Chapter 7: Event-driven architecture part 1: events and the message bus
* Chapter 8: event-driven architecture part 2: domain events
* Chapter 9: event-driven architecture part 3: command handler pattern
* Chapter 10: event-driven architecture part 4: reactive microservices

The idea is to pick an example application and build out each of these
patterns one by one, as new requirements come in.


## Can't wait?  Here's some resources you can get into already

Bob has already written a 4-part blog series on these patterns, which is
excellent:


1. [Ports and Adapters with Command Handler pattern in Python](https://io.made.com/introducing-command-handler/)
2. [Repository and Unit of Work Pattern in Python](https://io.made.com/repository-and-unit-of-work-pattern-in-python/ )
3. [Commands and Queries, Handlers and Views](https://io.made.com/commands-and-queries-handlers-and-views/)
4. [Why use Domain Events?](https://io.made.com/why-use-domain-events/)

There's more on io.made.com but those are the main four, and they're excellent, tuck in.

Also a timely release, check out 
[Clean Architectures in Python](https://leanpub.com/clean-architectures-in-python) by Leonardo Giordani.  It's really two  books in one, part one being an intro to TDD, but part 2 has four chapters introducing very much the kind of architecture that we're planning on talking about, with clear code examples.


And I know I said it already, but you should read some of the classics in the field:

* Patterns of Enterprise Architecture by Martin Fowler [amazon.com](https://amzn.to/2U6HTZN) / [.co.uk](https://amzn.to/2R0WkN3)

* Domain-Driven Design by Eric Evans [amazon.com](https://amzn.to/2W9nANe) / [.co.uk](https://amzn.to/2B7vmOP)

