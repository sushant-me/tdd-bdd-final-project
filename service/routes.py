from flask import jsonify, request, abort
from service.models import Product, Category, DataValidationError
from service.common import status
from . import app

@app.route("/products", methods=["GET"])
def list_products():
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")
    
    if name:
        products = Product.find_by_name(name)
    elif category:
        products = Product.find_by_category(getattr(Category, category.upper()))
    elif available:
        products = Product.find_by_availability(available.lower() in ["true", "1"])
    else:
        products = Product.all()
    
    return jsonify([p.serialize() for p in products]), status.HTTP_200_OK

@app.route("/products", methods=["POST"])
def create_product():
    """Create a new product in the catalog"""
    product = Product()
    try:
        product.deserialize(request.get_json())
    except DataValidationError:
        abort(status.HTTP_400_BAD_REQUEST)
    product.create()
    return jsonify(product.serialize()), status.HTTP_201_CREATED

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND)
    return jsonify(product.serialize()), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND)
    product.deserialize(request.get_json())
    product.update()
    return jsonify(product.serialize()), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.find(product_id)
    if product:
        product.delete()
    return "", status.HTTP_204_NO_CONTENT