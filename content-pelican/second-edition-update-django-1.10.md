Title: Second Edition update: Virtualenvs, Django 1.10, REST APIs, cleaner FTs...
Date: 2016-12-06 17:12
Tags: Book, second edition, Django, REST
Author: Harry
Summary: Progress on the second edition is pretty good!  I've got a first cut of some appendices on REST APIs, I've upgraded to Django 1.10, I'm recommending a virtulaenv all the way through, and I've improved the massive Chapter 6 rewrite slog by separating out FTs into one for regression and one for new stuff.

A brief update on my progress for the second edition. 

<img src="/static/images/second_edition_plan.png" alt="screenshot of book project plan, almost done" width="80%" />
*Getting there!*


## Virtualenvs all the way down.

In the first edition, I made the judgement call that telling people to use virtualenvs
at the very beginning of the book would be too confusing for beginners.  I've decided
to revisit that decision, since virtualenvs are more and more *de rigueur* these days.
I mean, if the [djangogirls tutorial](https://tutorial.djangogirls.org/) is recommending
one, given that it's the most beginner-friendly tutorial on Earth, then it really must
be a good idea.  So there's new instructions in the 
[pre-requisite installations chapter](http://www.obeythetestinggoat.com/book/pre-requisite-installations.html#_setting_up_your_virtualenv).  Let me know if you think they could be clearer.


## Django 1.10

Django 1.10 doesn't introduce that many new features over 1.8, but upgrading was still
pretty fiddly.  Thank goodness for my
[extensive tests](https://github.com/hjwp/Book-TDD-Web-Dev-Python/tree/master/tests)
(tests for the tests in the book about testing, yes. because of course.)  The main changes
you'll likely to notice is in
[Chapter 4](http://www.obeythetestinggoat.com/book/chapter_04.html#_the_don_t_test_constants_rule_and_templates_to_the_rescue)
where I introduce the Django Test Client, much earlier than I used to (which,
through a long chain of causes, is actually because of a 
[change to the way csrf tokens are generated](https://code.djangoproject.com/ticket/20869)).
Other than that, Django 1.10 was pretty much a drop-in replacement.  The main thing
I'm preparing for really is the upgrade to 1.11LTS early next year.


## REST APIs

I was thinking of having a couple of in-line chapters on building a REST API,
but for now I've decided to have them as appendices.  It starts with 
[how to roll your own](http://www.obeythetestinggoat.com/book/appendix_VI_rest_api.html),
 including an example of 
[how to test client-side ajax javascript with sinon](http://www.obeythetestinggoat.com/book/appendix_VI_rest_api.html#_testing_the_client_side_with_sinon_js),
and then there's a 
[second appendix on Django Rest Framework](http://www.obeythetestinggoat.com/book/appendix_VII_DjangoRestFramework.html).
These are both very much just skeleton outlines at the moment, but, still,
feedback and suggestions appreciated.


## A cleaner flow for Chapter 6

Chapter 6 is all about rewriting an app that *almost* works, to be one
that actually works, but trying to work incrementally all along, and using
the FTs to tell us when we make progress, and warn us if we introduce 
regressions.  I used to have just the one FT, and track progress/regressions
by "what line number is the FT failing at?  is it higher or lower than before?".
Instead I've split out 
[one FT that tests that the existing behaviour still works](http://www.obeythetestinggoat.com/book/chapter_06.html#_ensuring_we_have_a_regression_test),
and one FT for the new behaviour, and that's much neater I think.


## Next: geckodriver and Selenium 3 (uh-oh!)

There are plenty more little tweaks and nice-to-have additions I can think
of (React? Docker? Oh yeah, I got your trendy topics covered), but the main
task that's really outstanding is upgrading to Selenium 3 and geckodriver.
And the reason that's scary is because the
[current status of implicit waits is up for debate](https://lists.w3.org/Archives/Public/public-browser-tools-testing/2016OctDec/0033.html),
and I rely on implicit waits a lot.
Introducing explicit waits earlier might be a good thing (they're currently
only mentioned in Chapter 20), but it would definitely add to the learning
curve in the early chapters (I think they'd have to go in chapter 4 or 5,
which feels very early indeed).  So I'm kinda in denial about this at the
moment, hoping that maybe Mozilla will reintroduce the old behaviour, or
maybe I'll build some magical wrapper around selenium that just does implicit
waits for you  (maybe using my
[stale element check trick](http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html))
(in my copious spare time), or maybe switch to chromedriver, or I don't 
know I don't want to think about it.  Suggestions, words of encouragement,
moral support all welcome here.

In the meantime, I hope you enjoy the new stuff.  Keep in touch!

