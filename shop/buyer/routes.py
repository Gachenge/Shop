from flask import Blueprint, request, jsonify, abort
from utils import login_is_required, get_user
from shop.models.cart_item import CartItem
from shop.models.product import Product
from shop.models.cart import Cart
from shop import db

buyer_bp = Blueprint('buyer', __name__, url_prefix='/api/buy')

@buyer_bp.route("/product/<string:product_id>", methods=['POST'])
@login_is_required
def add_to_cart(product_id):
    try:
        product = Product.query.filter_by(id=product_id).first()
        if product is None:
            return jsonify({"error": "Product not found"}), 404

        user = get_user()

        if not user.is_active:
            return jsonify({"error": "Please verify your email address first"}), 422

        # Check if the user already has a cart
        cart = Cart.query.filter_by(user_id=user.id).first()
        if cart is None:
            cart = Cart(user_id=user.id)
            db.session.add(cart)
            db.session.commit()

        if product.copies <= 0:
            return jsonify({"error": "Sorry, we are currently out of stock"}), 422

        if product.copies < 1:
            return jsonify({"error": f"Only {product.copies} available"}), 422

        # Check if the product is already in the cart
        existing_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()
        if existing_item:
            existing_item.quantity += 1
        else:
            item = CartItem(cart_id=cart.id, product_id=product.id, quantity=1)
            db.session.add(item)

        product.copies -= 1
        db.session.commit()

        return jsonify({"message": "Product added to cart successfully"}), 201

    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Internal Server Error: {str(e)}")


