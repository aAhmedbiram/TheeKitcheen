from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from extensions import db
from models import Product
from auth import require_admin

products_api = Blueprint("products_api", __name__)


def _bad_request(message: str, status_code: int = 400):
    return jsonify({"ok": False, "error": message}), status_code


@products_api.get("/products")
@cross_origin()
def list_products():
    products = Product.query.order_by(Product.id.desc()).all()
    return jsonify({"ok": True, "items": [p.to_dict() for p in products]})


@products_api.get("/products/<int:product_id>")
@cross_origin()
def get_product(product_id: int):
    product = Product.query.get(product_id)
    if not product:
        return _bad_request("Product not found", 404)
    return jsonify({"ok": True, "item": product.to_dict()})


@products_api.post("/products")
@cross_origin()
@require_admin
def create_product():
    data = request.get_json(silent=True) or {}

    required = ["name_ar", "name_en", "description_ar", "description_en", "price"]
    missing = [k for k in required if not data.get(k)]
    if missing:
        return _bad_request(f"Missing fields: {', '.join(missing)}")

    try:
        price = float(data["price"])
    except (TypeError, ValueError):
        return _bad_request("Invalid price")

    product = Product(
        name_ar=str(data["name_ar"]).strip(),
        name_en=str(data["name_en"]).strip(),
        description_ar=str(data["description_ar"]).strip(),
        description_en=str(data["description_en"]).strip(),
        price=price,
        prep_time_minutes=int(data.get("prep_time_minutes") or 30),
        is_available=bool(data.get("is_available", True)),
        image_url=(str(data["image_url"]).strip() if data.get("image_url") else None),
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"ok": True, "item": product.to_dict()}), 201


@products_api.put("/products/<int:product_id>")
@cross_origin()
@require_admin
def update_product(product_id: int):
    product = Product.query.get(product_id)
    if not product:
        return _bad_request("Product not found", 404)

    data = request.get_json(silent=True) or {}

    if "name_ar" in data:
        product.name_ar = str(data["name_ar"]).strip()
    if "name_en" in data:
        product.name_en = str(data["name_en"]).strip()
    if "description_ar" in data:
        product.description_ar = str(data["description_ar"]).strip()
    if "description_en" in data:
        product.description_en = str(data["description_en"]).strip()
    if "price" in data:
        try:
            product.price = float(data["price"])
        except (TypeError, ValueError):
            return _bad_request("Invalid price")
    if "prep_time_minutes" in data:
        try:
            product.prep_time_minutes = int(data["prep_time_minutes"])
        except (TypeError, ValueError):
            return _bad_request("Invalid prep_time_minutes")
    if "is_available" in data:
        product.is_available = bool(data["is_available"])
    if "image_url" in data:
        product.image_url = str(data["image_url"]).strip() if data["image_url"] else None

    db.session.commit()
    return jsonify({"ok": True, "item": product.to_dict()})


@products_api.delete("/products/<int:product_id>")
@cross_origin()
@require_admin
def delete_product(product_id: int):
    product = Product.query.get(product_id)
    if not product:
        return _bad_request("Product not found", 404)

    db.session.delete(product)
    db.session.commit()
    return jsonify({"ok": True})



