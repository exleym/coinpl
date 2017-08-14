from flask import current_app, jsonify, request
from coinpl import get_session
from coinpl.models import Product
from coinpl.util.errors import (DatabaseIntegrityError,
                                MissingResourceError,
                                MissingJSONError,
                                PostValidationError)

from coinpl.blueprints.api_v1 import api_v1, error_out, verify_required_fields


# API Routes for accessing and managing currency information
# With these API endpoints, products can retrieve currency information by id,
# retrieve a list of products, add new products, update existing products.
@api_v1.route('/products', methods=['POST'])
def create_product():
    """ POST to /api/v1.0/products will create a new Product object
    """
    if not request.json:
        return error_out(MissingJSONError())
    expected_fields = ['symbol', 'base_currency_id', 'quote_currency_id',
                       'base_min_size', 'base_max_size', 'quote_increment',
                       'display_name', 'margin_enabled']
    data = request.json

    # Ensure that required fields have been included in JSON data
    if not verify_required_fields(data, expected_fields):
        return error_out(PostValidationError())
    session = get_session(current_app)
    product = Product(symbol=data['symbol'],
                      base_currency_id=data['base_currency_id'],
                      quote_currency_id=data['quote_currency_id'],
                      base_min_size=data['base_min_size'],
                      base_max_size=data['base_max_size'],
                      quote_increment=data['quote_increment'],
                      display_name=data['display_name'],
                      margin_enabled=data['margin_enabled'])
    session.add(product)
    try:
        session.commit()
    except:
        return error_out(DatabaseIntegrityError())
    p = session.query(Product).filter(Product.symbol == data["symbol"]).first()
    return jsonify(p.shallow_json), 201


@api_v1.route('/product/<int:product_id>', methods=['GET'])
def read_product_by_id(product_id):
    session = get_session(current_app)
    exch = session.query(Product).filter(Product.id == product_id).first()
    if not exch:
        return error_out(MissingResourceError('Product'))
    return jsonify(exch.shallow_json), 200


@api_v1.route('/products/', methods=['GET'])
def read_products():
    session = get_session(current_app)
    products = session.query(Product).all()
    if not products:
        return error_out(MissingResourceError('Product'))
    return jsonify([product.shallow_json for product in products]), 200


@api_v1.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """ PUT request to /api/product/<exchane_id> will update Product object
        <id> with fields passed
    """
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return error_out(MissingJSONError())
    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        return error_out(MissingResourceError('Product'))
    for k, v in put_data.items():
        setattr(product, k, v)
    session.add(product)
    session.commit()
    return jsonify(product.shallow_json)


@api_v1.route('/product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """ DELETE request to /api/v1.0/product/<product_id> will delete the
        target Product object from the database
    """
    session = get_session(current_app)
    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        return error_out(MissingResourceError('Product'))
    session.delete(product)
    session.commit()
    return jsonify(200)
