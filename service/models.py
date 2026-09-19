"""
Product Model

The Product model is the persistent representation of a product in the
catalog.  It also owns the small data-access helpers used by the routes.
"""
from enum import Enum

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DataValidationError(Exception):
    """Raised when product data fails validation"""


class Category(Enum):
    """Enumeration of the product categories the service supports"""

    CLOTHS = 1
    FOOD = 2
    HOUSEWARES = 3
    AUTOMOTIVE = 4
    TOOLS = 5


class Product(db.Model):
    """Product model that maps to the products table"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(256))
    # NOTE: Flask-SQLAlchemy 3.x no longer re-exports `Decimal`; `Numeric` is
    # the SQLAlchemy type for fixed-precision decimal columns.
    price = db.Column(db.Numeric(10, 2), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=True)
    category = db.Column(db.Enum(Category), nullable=False)

    def __repr__(self):
        return f"<Product {self.name} id=[{self.id}]>"

    def create(self):
        """Add this product to the database"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Commit changes made to this product"""
        db.session.commit()

    def delete(self):
        """Remove this product from the database"""
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Return this product as a plain dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "available": self.available,
            "category": self.category.name,
        }

    def deserialize(self, data):
        """Populate this product from a dictionary (e.g. a JSON body)"""
        try:
            self.name = data["name"]
            self.description = data.get("description", "")
            self.price = data["price"]
            self.available = data.get("available", True)
            category = data["category"]
            self.category = (
                category
                if isinstance(category, Category)
                else Category[category.upper()]
            )
        except KeyError as error:
            raise DataValidationError(
                f"Invalid product: missing {error.args[0]}"
            ) from error
        except AttributeError as error:
            raise DataValidationError(
                "Invalid product: body must be a JSON object"
            ) from error
        return self

    @classmethod
    def init_db(cls, app):
        """Initialize the database and create all of its tables"""
        db.init_app(app)
        app.app_context().push()
        db.create_all()

    @classmethod
    def all(cls):
        """Return every product"""
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Find a product by its id"""
        return db.session.get(cls, by_id)

    @classmethod
    def find_by_name(cls, name):
        """Return the query for all products with the given name"""
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category):
        """Return the query for all products in the given category"""
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_availability(cls, available=True):
        """Return the query for all products with the given availability"""
        return cls.query.filter(cls.available == available)
