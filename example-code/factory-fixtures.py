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


@pytest.fixture()
def product(db, make_supplier):
    p = Product(
        ref=random_ref(),
        name=random_name(),
        supplier=make_supplier("US"),
        net_price=9.99,
    )
    db.add(p)
    yield p
    db.remove(p)



@pytest.fixture
def make_supplier(db):
    s = Supplier(
        ref=random_ref(),
        name=random_name(),
        country=None,
    )

    def _make_supplier(country):
        s.country = country
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
        supplier=None,
        net_price=9.99
    )

    def _make_product(supplier):
        p.supplier = supplier
        db.add(p)
        return p

    yield _make_product
    db.remove(p)


def test_EU_supplier_has_total_price_including_VAT2(make_supplier, make_product):
    supplier = make_supplier(country="FR")
    product = make_product(supplier=supplier)
    assert product.total_price == product.net_price * 1.2

