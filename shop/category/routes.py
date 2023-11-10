from shop import db
from flask import Blueprint, request, jsonify, abort
from utils import admin_required
from shop.models.product import Product
from shop.models.category import Category
from shop.models.users import Users

category_bp = Blueprint('category', __name__, url_prefix='/api/category')

@category_bp.route("/", methods=['GET', 'POST'])
@admin_required
def allCategory():
    if request.method == 'GET':
        try:
            categories = Category.query.all()
            cat_info = []

            for category in categories:
                cat_info.append(category.name)

            return jsonify({"Categories": cat_info}), 200

        except Exception as e:
            abort(500, description="Internal Server Error")

    elif request.method == 'POST':
        data = request.get_json()
        if 'category' not in data or not data['category']:
            return jsonify({"Error": "You need a category in the payload"})

        try:
            category = Category(name=data.get('category'))

            db.session.add(category)
            db.session.commit()

            return jsonify({"Message": "Category added successfully"})
        except Exception as e:
            db.session.rollback()
            abort(500, description="Internal Server Error")

    else:
        return jsonify({"Error": "Method not allowed"}), 405

@category_bp.route("/<string:category_id>", methods=['GET', 'PATCH', 'DELETE'])
@admin_required
def category_by_id(category_id):
    try:
        category = Category.query.get(category_id)
        if category is None:
            return jsonify({"Error": "Category not found"}), 404

        if request.method == 'GET':
            product_info = []
            for product in category.products:
                user = Users.query.get(product.seller_id)
                product_data = {
                    "Category": category.name,
                    "Product": product.name,
                    "Description": product.description,
                    "Price": product.price,
                    "Seller": user.username
                }
                product_info.append(product_data)
            return jsonify(product_info)

        elif request.method == 'PATCH':
            data = request.get_json()
            new_category_name = data.get('category')

            if new_category_name == category.name:
                return jsonify({"Message": "Category name unchanged"}), 200

            if not new_category_name:
                return jsonify({"Error": "You need a category name in the payload"}), 400

            category.name = new_category_name
            db.session.commit()

            return jsonify({"Message": "Category name updated successfully"}), 200

        elif request.method == 'DELETE':
            for product in category.products:
                db.session.delete(product)
            db.session.delete(category)
            db.session.commit()

            return jsonify({"Message": "Category and associated products deleted successfully"}), 204

    except Exception as e:
        db.session.rollback()
        abort(500, description="Internal Server Error")
