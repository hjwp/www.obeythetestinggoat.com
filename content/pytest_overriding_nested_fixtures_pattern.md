Title: A Pytest pattern: using parametrize to customise fixtures.
Date: 2018-10-17 11:20
Tags: pytest, fixtures,
Author: Harry
Summary: From time to time we come across a fixture that we want to customise in some way.  Factory functions and factory fixtures are classic options, but you can also (mis-) use the pytest parametrize decorator to achieve this goal. Find out how here!

## The problem: customisable fixtures in pytest

Let's say you're running along merrily with some fixtures that create database objects for you:

```python
@pytest.fixture
def supplier(db):
    s = Supplier(
        ref=random_ref(),
        name=random_name(),
        country="US",
    )
    db.add(s)
    yield s
    db.remove(s)



@pytest.fixture()
def product(db, supplier):
    p = Product(
        ref=random_ref(),
        name=random_name(),
        supplier=supplier,
        net_price=9.99,
    )
    db.add(p)
    yield p
    db.remove(p)
```


And now you're writing a new test and you suddenly realise you need to customise your default "supplier" fixture:


```python
def test_US_supplier_has_total_price_equal_net_price(product):
    assert product.total_price == product.net_price

def test_EU_supplier_has_total_price_including_VAT(supplier, product):
    supplier.country = "FR" # oh, this doesn't work
    assert product.total_price == product.net_price * 1.2
```

For whatever reason, maybe because you need to set the `supplier.country` before you add things to the DB, or before you instantiate product objects, you need to be able to adjust the `country` field on your supplier feature.


## Option 1: more fixtures

We can just create more fixtures, and try do do a bit of DRY by extracting out common logic:

```python
def _default_supplier():
    return Supplier(
        ref=random_ref(),
        name=random_name(),
    )

@pytest.fixture
def us_supplier(db):
    s = _default_supplier()
    s.country = "US"
    db.add(s)
    yield s
    db.remove(s)

@pytest.fixture
def eu_supplier(db):
    s = _default_supplier()
    s.country = "FR"
    db.add(s)
    yield s
    db.remove(s)
```

That's just one way you could do it, maybe you can figure out ways to reduce the duplication of the `db.add()` stuff as well, but you are going to have to have a different, named fixture for each customisation of `Supplier`, and eventually you may decide that doesn't scale.  `us_supplier`, `eu_supplier`, `asia_supplier`, `ch_supplier`, etc etc, too many fixtures!  I'd like just one, customisable fixture please.

## Option 2: factory fixtures

Instead of a fixture returning an object directly, it can return a function that creates an object, and that function can take arguments:

```python
@pytest.fixture
def make_supplier(db):
    s = Supplier(
        ref=random_ref(),
        name=random_name(),
    )

    def _make_supplier(country):
        s.country = country
        db.add(s)
        return s

    yield _make_supplier
    db.remove(s)
```

The problem with this is that, once you start, you tend to have to go all the way, and make _all_ of your fixture hierarchy into factory functions: 
```python
def test_EU_supplier_has_total_price_including_VAT(make_supplier, product):
    supplier = make_supplier(country="FR")
    product.supplier = supplier # OH, now this doesn't work, because it's too late again
    assert product.total_price == product.net_price * 1.2
```

And so...

```python
@pytest.fixture
def make_product(db):
    p = Product(
        ref=random_ref(),
        name=random_name(),
    )

    def _make_product(supplier):
        p.supplier = supplier
        db.add(p)
        return p

    yield _make_product
    db.remove(p)


def test_EU_supplier_has_total_price_including_VAT(make_supplier, make_product):
    supplier = make_supplier(country="FR")
    product = make_product(supplier=supplier)
    assert product.total_price == product.net_price * 1.2
```

That works, but firstly now everything is a factory-fixture, which makes them more convoluted, and secondly, your tests are filling up with extra calls to `make_things`, and you're having to embed some of the domain knowledge of what-depends-on-what into your tests as well as your fixtures.

## Option 3: "normal" fixture parametrization

This is a pretty cool feature of Pytest.  You probably already know that you can parametrize tests, injecting different values for arguments to your test and then running the same test multiple times, once for each value:

```python
@pytest.mark.parametrize('n', [1, 2, 3])
def test_doubling(n):
    assert n * 2 < 6 # will pass twice and fail once
```


A slightly less well-known feature is that you can parametrize fixtures as well.  You need to use the special `request` fixture to access your parameters:

```python
@pytest.mark.parametrize(['US', 'FR'])
@pytest.fixture
def supplier(db, request):
    s = Supplier(
        ref=random_ref(),
        name=random_name(),
        country=request.param
    )
    db.add(s)
    yield s
    db.remove(s)
```

Now any test that depends on `supplier`, directly or indirectly, will be run twice, once with `supplier.country = US` and once with `FR`.

That's really cool for checking that a given piece of logic works in a variety of different cases, but it's not really ideal in our case.  We have to build a bunch of `if` logic into our tests:


```python
def test_US_supplier_has_no_VAT_but_EU_supplier_has_total_price_including_VAT(product):
    # this test is magically run twice, but:
    if product.supplier.country == 'US':
        assert product.total_price == product.net_price
    if product.supplier.country == 'FR':
        assert product.total_price == product.net_price * 1.2
```

So that's ugly, and on top of that, now _every single_ test that depends (indirectly) on supplier gets run twice, and some of those extra test runs may be totally irrelevant to what the country is.


## Presenting: using test parmetrization to override nested default-value fixtures


We introduce an extra fixture that holds a default value for the `country` field:

```python
@pytest.fixture()
def country():
    return "US"


@pytest.fixture
def supplier(db, country):
    s = Supplier(
        ref=random_ref(),
        name=random_name(),
        country=country,
    )
    db.add(s)
    yield s
    db.remove(s)
```


And then in the tests that need to change it, we can use `parametrize`, _even though the country fixture isn't explicitly named in that test_:

```python
@pytest.mark.parametrize('country', ["US"])
def test_US_supplier_has_total_price_equal_net_price(product):
    assert product.total_price == product.net_price

@pytest.mark.parametrize('country', ["EU"])
def test_EU_supplier_has_total_price_including_VAT(product):
    assert product.total_price == product.net_price * 1.2
```


Amazing huh?  The only problem is that you're now likely to build a teetering tower of implicit dependencies where the only way to find out what's actually happening is to spend ages spelunking in `conftest.py`, but, hey, if you didn't like crazy nested fixture magic, why are you using pytest in the first place, right?

Reactions and alternative suggestions on a postcard please :)

