from flask import Blueprint, request, jsonify, abort
from utils import login_is_required, get_user
from shop.models.category import Category
from shop.models.product import Product
from shop.models.users import Users
from typing import Dict, Union
from shop import db


AttributeTypes = Dict[str, Union[str, float]]

allowed_attributes: AttributeTypes = {
    'name': str,
    'description': str,
    'price': float,
    'category': str,
}

product_bp = Blueprint('product', __name__, url_prefix='/api/product')

@product_bp.route("/", methods=['GET', 'POST'])
@login_is_required
def allProduct():
    if request.method == 'GET':
        try:
            categories = Category.query.all()
            product_info = []

            for category in categories:
                for product in category.products:
                    user = Users.query.get(product.seller_id)
                    product_data = {
                        "Category": category.name,
                        "Product": product.name,
                        "Description": product.description,
                        "Price": product.price,
                        "Items": product.copies,
                        "Seller": user.username
                    }
                    product_info.append(product_data)

            return jsonify(product_info)
        except Exception as e:
            abort(500, description=f"Internal Server Error: {str(e)}")

    elif request.method == 'POST':
        data = request.get_json()

        # Check if all attributes are present and have the correct types
        if not all(
            attr in data and isinstance(data[attr], allowed_attributes[attr])
            for attr in allowed_attributes):
            return jsonify({"error": f"Missing or incorrect data in the request: {str(e)}"}), 400

        category = Category.query.filter_by(name=data['category']).first()

        if category is None:
            return jsonify({"Error": "The category does not exist. Contact the admin for more details"}), 400
        user = get_user()

        try:
            product = Product(name=data['name'], description=data['description'],
                price=data['price'], category_id=category.id, user_id=user.id)

            db.session.add(product)
            db.session.commit()
            return jsonify({"Success": "New product created successfully"}), 201

        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Internal Server Error: {str(e)}")

@product_bp.route("/<string:product_id>", methods=['GET', 'PATCH', 'DELETE'])
@login_is_required
def product_by_id(product_id):
    try:
        product = Product.query.get(product_id)
        if product is None:
            return jsonify({"Error": "Product not found"}), 404

        user = Users.query.get(product.seller_id)
        category = Category.query.get(product.category_id)

    except Exception as e:
        abort(500, description=f"Internal Server Error: {str(e)}")

    if request.method == 'GET':
        product_info = {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "Items": product.copies,
            "seller": user.username,
            "category": category.name
        }
        return jsonify({"Product": product_info}), 200

    if request.method == 'PATCH':
        data = request.get_json()

        # Check if all attributes are present and have the correct types
        if not all(
            attr in data and isinstance(data[attr], allowed_attributes[attr])
            for attr in allowed_attributes):
            return jsonify({"error": f"Missing or incorrect data in the request: {str(e)}"}), 400

        try:
            category = Category.query.filter_by(name=data['category']).first()

            if category is None:
                return jsonify({"Error": "The category does not exist. Contact the admin for more details"}), 400

            for key, value in data.items():
                setattr(product, key, value)

            db.session.commit()
            return jsonify({"Success": "Product updated successfully"}), 200

        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Internal Server Error: {str(e)}")

    if request.method == 'DELETE':
        try:
            db.session.delete(product)
            db.session.commit()
            return jsonify({"Success": "Product deleted successfully"}), 204

        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Internal Server Error: {str(e)}")
