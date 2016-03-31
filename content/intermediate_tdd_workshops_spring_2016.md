Title: Intermediate TDD workshops in London and Portland
Status: draft
Date: 2016-03-27 21:11
Tags: Worskshop, Outside-In, Mocks
Author: Harry
Summary: I'm running some new workshops loosely based on some of the later chapters in the book, aimed at discussing some intermediate TDD issues: the outside-in approach, and the pros and cons of mocks and test isolation.

After many successful years of running my beginners' TDD/django tutorial, I
thought it might be time to have a crack at some more intermediate-level
topics, so I'm announcing a couple of workshops.

- the first is [in London, on Monday the 4th of April, at Skillsmatter](https://skillsmatter.com/meetups/7997-in-the-brain-of-harry-percival)

- the second is in [Portland, Oregon, on Sunday the 29th of May, at Pycon](https://us.pycon.org/2016/schedule/presentation/1713/)

That London one is next Monday, so book up quick!

Come prepared!  You'll need:

```bash
git clone https://github.com/hjwp/book-example/ tdd-workshop
cd tdd-workshop
git fetch --tags
git checkout chapter_17
mkvirtualenv --python=python3 tdd-workshop
pip install -r requirements.txt
python manage.py test  # these should all pass
```

Ask me if you have any problems!  [obeythetestinggoat@gmail.com](mailto:obeythetestinggoat@gmail.com)
