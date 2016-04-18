Title: Intermediate TDD workshops in London and Portland
Date: 2016-03-31 13:22
Tags: Workshop, Outside-In, Mocks
Author: Harry
Summary: I'm running some new workshops loosely based on some of the later chapters in the book, aimed at discussing some intermediate TDD issues: the outside-in approach, and the pros and cons of mocks and test isolation.

After many successful years of running my beginners' TDD/Django tutorial, I
thought it might be time to have a crack at some more intermediate-level
topics, so I'm announcing a couple of workshops.

- the first is [in London, on Monday the 4th of April, at Skillsmatter](https://skillsmatter.com/meetups/7997-in-the-brain-of-harry-percival)

- the second is in [Portland, Oregon, on Sunday the 29th of May, at Pycon](https://us.pycon.org/2016/schedule/presentation/1713/)


> The aim will be to cover some intermediate-level topics.  It assumes you've already started doing a bit of TDD, you've wrapped your head around unit testing, and some basic mocking, but you're starting to ask questions like: What order should I write tests in?  When should I mock, and when should I not?  What are the pros and cons of isolated unit tests vs integration tests?  What do people mean when they say "let the tests drive the design"?

I'm not claiming that I'll come up with perfect answer to these questions, or solve all your problems, but we will go through a worked example that will help to illustrate some of the tradeoffs, and hopefully help you to think about how to apply this for your own projects.   It's based on chapters 17 and 18 in [my book](/pages/book.html).

That London one is next Monday, so book up quick!

And come prepared!  You'll need:

```bash
git clone https://github.com/hjwp/book-example/ tdd-workshop
cd tdd-workshop
git fetch --tags
git checkout chapter_17
mkvirtualenv --python=python3 tdd-workshop  # or however you like to create virtualenvs
pip install -r requirements.txt
pip install selenium
python manage.py test  # these should all pass
```

Ask me if you have any problems!  [obeythetestinggoat@gmail.com](mailto:obeythetestinggoat@gmail.com)

*[update monday PM]*

If the functional tests are being strange, try switching from firefox to chrome.

* Download chromedriver from here: https://sites.google.com/a/chromium.org/chromedriver/downloads

* Extract it and add it to your path

* Switch `webdriver.Firefox()` to `webdriver.Chrome()` in *functional_tests/base.py*

