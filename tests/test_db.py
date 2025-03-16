from dataclasses import asdict
from decimal import Decimal

from sqlalchemy import select

from fastapi_products_api.models.enums import ProductType
from fastapi_products_api.models.products import Product


def test_create_product(session, mock_db_time):
    with mock_db_time(model=Product) as time:
        new_product = Product(
            name='kinder_joy',
            brand='kinder',
            price=13.99,
            type=ProductType.GROCERIES,
        )

        session.add(new_product)
        session.commit()
        session.refresh(new_product)

    db_product = session.scalar(
        select(Product).where(Product.id == new_product.id)
    )

    assert asdict(db_product) == {
        'id': 1,
        'name': 'kinder_joy',
        'brand': 'kinder',
        'price': Decimal('13.99'),
        'type': ProductType.GROCERIES,
        'created_at': time,
        'updated_at': time,
    }
