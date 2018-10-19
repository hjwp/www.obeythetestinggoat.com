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


@pytest.fixture(params=['US', 'FR'])
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
