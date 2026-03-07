import os
import logging
import unittest
from service import app
from service.models import Product, Category, db
from tests.factories import ProductFactory

DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres")

class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        Product.init_db(app)

    def setUp(self):
        db.session.query(Product).delete()
        db.session.commit()

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="Fedora", category=Category.CLOTHS, price=25.0, available=True)
        product.create()
        self.assertIsNotNone(product.id)
        self.assertEqual(product.name, "Fedora")

    def test_find_by_name(self):
        """It should Find a Product by Name"""
        products = ProductFactory.create_batch(5)
        for prod in products:
            prod.create()
        name = products[0].name
        count = len([p for p in products if p.name == name])
        found = Product.find_by_name(name)
        self.assertEqual(found.count(), count)