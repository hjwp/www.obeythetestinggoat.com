import pytest
import uuid
from dataclasses import dataclass

@dataclass
class Supplier:
    ref: str
    name: str
    country: str


@dataclass
class Product:
    ref: str
    name: str
    supplier: Supplier
    net_price: float

    @property
    def total_price(self):
        return self.net_price if self.supplier.country == "US" else self.net_price * 1.2


def random_ref():
    return random_name()

def random_name():
    return str(uuid.uuid4())


class FakeDB:
    def add(self, thing):
        pass

    def remove(self, thing):
        pass


@pytest.fixture
def db():
    return FakeDB()




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



def test_US_supplier_has_total_price_equal_net_price(product):
    assert product.total_price == product.net_price

def test_EU_supplier_has_total_price_including_VAT(supplier, product):
    supplier.country = "FR" # oh, this doesn't work
    assert product.total_price == product.net_price * 1.2


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


@pytest.fixture
def make_supplier(db):
    s = Supplier(
        ref=random_ref(),
        name=random_name(),
    )

    def _make_supplier(country):
        s.country = "US",
        db.add(s)
        return s

    yield _make_supplier
    db.remove(s)


def test_EU_supplier_has_total_price_including_VAT(make_supplier, product):
    supplier = make_supplier(country="FR")
    product.supplier = supplier # OH, now this doesn't work.
    assert product.total_price == product.net_price * 1.2



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


@pytest.mark.parametrize('n', [1, 2, 3])
def test_doubling(n):
    assert n * 2 < 6 # will pass twice and fail once


def test_US_supplier_has_no_VAT_but_EU_supplier_has_total_price_including_VAT(product):
    # this test is magically run twice, but:
    if product.supplier.country == 'US':
        assert product.total_price == product.net_price
    if product.supplier.country == 'FR':
        assert product.total_price == product.net_price * 1.2


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


@pytest.mark.parametrize('country', ["US"])
def test_US_supplier_has_total_price_equal_net_price(product):
    assert product.total_price == product.net_price

@pytest.mark.parametrize('country', ["EU"])
def test_EU_supplier_has_total_price_including_VAT(product):
    assert product.total_price == product.net_price * 1.2

