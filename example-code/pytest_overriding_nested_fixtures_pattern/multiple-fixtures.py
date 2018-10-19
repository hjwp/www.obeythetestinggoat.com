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

def test_US_supplier_has_total_price_equal_net_price(product):
    assert product.total_price == product.net_price

def test_EU_supplier_has_total_price_including_VAT(eu_supplier, product):
    eu_supplier.country = "FR" # oh, this doesn't work
    assert product.total_price == product.net_price * 1.2
