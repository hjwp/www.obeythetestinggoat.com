Title: Decorators!
Date: 2014-10-23
Tags: Python, decorators, Django
Author: Harry
Summary: <p>Decorators can be quite confusing when you first meet them. The best way to learn is by writing some!  Here's a couple of simple examples for you to try out.</p>

Someone recently wrote to me asking about decorators, and saying they found them a bit confusing.  Here's a post based on the email I replied to them with. 

The best way to understand decorators is to build a couple of them, so here are two examples for you to try out.  The first is in the Django world, the second is actually a simpler, pure-python one.


## Challenge: build a decorator in a simple Django app

We've built a very basic todo lists app using Django.  It has views to deal with viewing lists, creating new lists, and adding to existing lists.  Two of these views end up doing some similar work, which is to retrieve a list object from the database based on its list ID:

```python
def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})
```

(Full code [here](https://github.com/hjwp/book-example/blob/chapter_06/lists/views.py))

This is a good use case for a decorator.

A decorator can be used to extract duplicated work, and also to change the arguments to a function.  So we should be able to build a decorator that does the list-getting for us.  Here's the target:

```python
@get_list
def add_item(request, list_):
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))


@get_list
def view_list(request, list_):
    return render(request, 'list.html', {'list': list_})
```

So how do we build a decorator that does that?  A decorator is a function that takes a function, and returns another function that does a slightly modified version of the work the original function was doing.  We want our decorator to transform the simplified view functions we have above, into something that looks like the original functions.

> (you end up saying "function" a lot in any explanation of decorators...)

Here's a template:

```python
def get_list(view_fn):

    def decorated_view(...?):
        ???
        return view_fn(...?)

    return decorated_view
```

Can you get it working?  Thankfully, our code has tests, so they'll tell you when you get it right...

    git clone -b chapter_06 https://github.com/hjwp/book-example
    python3 manage.py test lists # dependencies: django 1.7


## Some rules of thumb for decorators:

- they usually contain an "internal" function definition, which ends up being what the decorator returns.
- that internal function usually calls the original function.
- that internal function also needs to return something.



Decorators definitely are a bit brain-melting, so it may take a bit of effort to wrap your head around it.  Once you get the hang of them, they're dead useful though,


## A simpler decorator challenge:

If you're finding it impossible, you could start with a simpler challenge...  say, building a decorator to make functions return an absolute value:


```python
def absolute(fn):
    # this decorator currently does nothing
    def modified_fn(x):
        return fn(x)
    return modified_fn


def foo(x):
    return 1 - x

assert foo(3) == -2


@absolute
def foo(x):
    return 1 - x

assert foo(3) == 2  # this will fail, get is passing!
```

    git clone https://gist.github.com/2cc523b66d9c0fe41c4b.git deccy
    python3 deccy/deccy.py

Enjoy!

