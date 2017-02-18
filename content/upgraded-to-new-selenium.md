Title: Upgraded to Selenium 3! (and Geckodriver)
Date: 2017-02-11 10:12
Tags: Book, second edition, Selenium
Author: Harry
Summary: Well, that was  bit of a slog!  I've managed to get the book upgraded to the newer version of selenium, and it involved quite a lot of pain with explicit waits, and renumbering all the chapters, but I think the book is better for it.  read on!


## Selenium 3 and Geckodriver

Selenium 3 came out earlier this year, and the Mozilla project, those wonderful technohippies,
have been pushing the standard forward (did someone say "bleeding edge"?), and
the lastest versions of Firefox will only work with the new Selenium 3 and its
"geckodriver" client driver.

The project it still young and has
[plenty](https://github.com/mozilla/geckodriver/issues) of [minor
bugs](https://developer.mozilla.org/en-US/docs/Mozilla/QA/Marionette/WebDriver/status) still, but it's
functional enough, and I don't want to have to continue recommending people downgrade to Firefox 45 ESR,
or (Saint RMS forbid!) switch to one of the other evil browsers, compromised as they are by corporate interests.

So selenium 3 it is!


## Explicit waits all the way

"implicit waits", whereby Selenium automatically tries to wait for things to happen (eg for the page to
load after a click) have always been a bit flakey, and 
[the official line](https://groups.google.com/d/msg/selenium-developers/hA_jTx4vrDM/zZOtVX1_jQEJ)
is to prefer explicit waits at all times.  And unfortunately with Selenium 3 implicit waits have
become all the more unreliable (or simply [not implemented](https://github.com/mozilla/geckodriver/issues/308)).

So while in the first edition I was able to avoid the topic of explicit waits all the way until about
chapter 20, in the new one I have to introduce them upfront.  And as a result I've had to insert a
new chapter after chapter 5: [the first explicit waits chapter](http://www.obeythetestinggoat.com/book/chapter_explicit_waits_1.html)

It did allow me to introduce two wait helpers I'm quite fond of though:

* a generic [wait_for function](https://www.obeythetestinggoat.com/book/chapter_organising_test_files.html#_a_new_functional_test_tool_a_generic_explicit_wait_helper)

* a generic [wait decorator](http://www.obeythetestinggoat.com/book/chapter_fixtures_and_wait_decorator.html#_our_final_explicit_wait_helper_a_wait_decorator)  (mmmh, Pythonic!)

Functional programming goodness!

Overall I think the book is better for it.


## Lesson: avoid numerical chapter names

Inserting a new chapter after chapter 5 proved to be lots of "fun".  I certainly learned the lesson
of avoiding numerical names for my chapter source files!  Up until this point, all the files were
called things like `chapter_05.html`.  And of course all the associated source code examples were
in branches named similarly.  And all the book's tests (the meta-tests if you will) have similar
dependencies.  So everything was off by one, and I've spent the last few weeks
[shaving that yak](https://github.com/hjwp/Book-TDD-Web-Dev-Python/commits/rename-all-chapters).


## Also: computers.

I've enabled comments on each chapter using Disqus. By default it uses URLs as
the identifier for my threads. So the recent renumbering meant about half the
comments ended up on the wrong pages. Thankfully Disqus have a tool to deal with
this called the "URL mapper", and "hooray", I thought, problem solved, and so I
submitted a mapping a bit like this:

```
page7 -> page8
page8 -> page9
page9 -> page10
etc
```

Turns out that was a disaster. The disqus migration tool took me at my word I
guess, and went down the list in order, moving all the comments from page 7
onto page 8 (can you guess what happens next?) Then it took all the comments on
page 8 (which now included the ones from page 7), and moved them onto page 9...
and the end result is that almost all the pages have no comments, except for
the last page, which has ended up with all the 600 comments from all the other
pages glommed together in a massive mess. oh no. computers eh?

Pending help from disqus (which 
[doesn't seem to be forthcoming](https://disqus.com/home/discussion/channel-discussdisqus/admin_undo_url_mapper_or_manually_reassign_comments_to_threads/)) it'll have
to be a fresh start on comments then!

## As always, your feedback is enthusiastically solicited

Follow the links above for some of the content that's specifically new to
Selenium 3, and let me know what you think!

