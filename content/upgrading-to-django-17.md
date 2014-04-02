Title: Book upgraded to Django 1.7!
Date: 2014-04-02 12:23
Tags: django, beta, migrations
Author: Harry
Summary: <p>I've just completed the process of upgrading the whole book to the Django 1.7 beta release.  Migrations were the biggest change.  They've meant a slight increase to the learning curve for chapters 5 & 6, but on the other hand I was able to drop the dedicated migrations chapter altogether!</p>

In a (futile) attempt to future-proof the book, I decided to upgrade it to
Django 1.7. Here's how that went down.

## Overview 

Unsurprisingly, the biggest change was to do with migrations.  Like any new
change, my initial reaction was dislike, and I resented the new things, but I
think overall it's a definite improvment.

In brief, here's what happened:

* The new migrations framework means 'any' change to models needs a migration,
  or tests won't pass.

* This meant introducing the concept of migrations much earlier in the book; 
  in fact, at the same time as I introduce the ORM.  I resented this because
  it made the learning curve of the book steeper.

* On the other hand, because the new version of migrations essentially forces
  you to have them from the very beginning, I was able to drop an entire 
  chapter that was devoted to retrospectively building migrations after the
  first deployment, which included all sorts of checking out of old versions,
  and using `--fake`, and so on.  So that's a big win.

* Using step-by-step TDD also forces you to make more migrations than you really
  want to, if you're adding fields and constraints step-by-step.  It means I have
  to introduce the reader early on to the idea of replacing existing migrations
  too, another steepening of the learning curve.

Here's some detail on the changes.


## Migrations make the introduction of *models.py* more complex

In chapter 5, where we build the first model, the narrative used to go:

1. Write a test 
2. See it fail
3. Add code in *models.py*, step by step
4. Get the tests further, see a different failure
5. Add more code in *models.py*
6. Get the tests passing

Now it goes:

1. Write a test 
2. See it fail
3. Add code in *models.py*, step by step
4. See a database error
5. Create a migration
6. See the tests get further, see a different failure
7. Add more code in *models.py*
8. See a database error
9. Explain the concept of squashing migrations into one
10. Delete the existing migration and re-create it. 
11. See the tests pass

So you can see it's more complicated.  On the other hand, understanding
how Django gets from *models.py* to the database is important.  I had been
just hand-waving and saying "use syncdb, and just delete the database if
anything goes wrong", so maybe it's better to address this stuff head-on,
rather than wait for a complicated later chapter.

If you're curious, you can [view the whole narrative here](http://chimera.labs.oreilly.com/books/1234000000754/ch05.html#_the_django_orm_amp_our_first_model)

*(If you're a Django core developer and you're reading this, I'd love to
hear your thoughts btw.  There's a few weeks before the book goes to print
yet, so there's still time to tell me I'm doing it all wrong!)*

I still kinda wish I could have kept my nice shallow learning curve - 
I expended a lot of effort with the book, in trying to make sure concepts
are introduced one at a time and gradually, and now I feel I'm slightly
forced to lump two concepts onto the reader at the same time.  But, there's
clearly an upside.


## But they save me from a fairly horrible chapter 13...

It was always going to be an unlucky chapter wasn't it.  Because I'd 
glossed over the concept of migrations until then, I would get the
readers to deploy their code to a server in chapter 8 or so, and
then code some new stuff, including a new database feature.

Then I had a chapter 13 in which we would try and deploy to the staging
site, and see the new feature wouldn't work.  So then I had to explain
migrations, and go through this process:

1. Find the old commit that matches the point at which we did the last
   deployment, and check out the old version of *models.py* from it.
2. Do a `manage.py schemamigration`, and create a migration to match live
3. Check out the latest version of *models.py*, and do another `schemamigration`
   to get the migration we want to apply.
4. Test it out locally.  Check out the old *models.py* again, delete the databse,
   syncdb, then run `migrate 0001 --fake`, then check out the new code, and
   run `migrate`, check it works
5. Adjust the deploy script to include `migrate 0001 --fake` followed by a `migrate`
6. Test deploying to staging... OK
7. Deploy to live
8. And, don't forget to now remove the `migrate 001 --fake` from your deploy 
   script.


Ouch! Quite a lot of pain there!  Especially when you consider that the new
procedure is:

1. Run the deploy script.  It just works, because we've had migrations all
   along.

:-)


## Other thoughts.

I found the fact that tests would fail if you didn't have migrations intriguing,
but unfortunately it's not something you can rely on.  For example, in chapter
12 I introduce a `unique_together` constraint and test it thusly:

    :::python
    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()

To get that passing, I just add my `unique_together` constraint:

    :::python
    class Item(models.Model):
        text = models.TextField()
        list = models.ForeignKey(List)

        class Meta:
            unique_together = ('list', 'text')


And at this point *Django doesn't warn me that I need a migration*, because
the test is actually happening at the validation layer.

I think that's a bit of a shame, but there's probably nothing to be done about
it.  It's all because the concepts of data validation and database integrity
constraints are separate in Django, even though their implementation in 
*models.py* actually often happens in a single place...



## One last thing...

<img src="/static/images/makemigrations_screenshot_colour.png" />

I love the pretty colours!


