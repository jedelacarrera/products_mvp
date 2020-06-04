from flask import Blueprint, request, render_template
from src.models import db
from src.routes.products import controllers

products_app = Blueprint("projects", __name__, url_prefix="/products")


@products_app.route("/", methods=["GET"])
def get_products():
    search = request.args.get("search", "")
    products = controllers.get_products(search=search)
    return render_template(
        "products.html", search=search, categories=products["categories"]
    )


@products_app.route("/<pid>/", methods=["GET"])
def product(pid):
    result = controllers.get_offers_by_product(pid)
    return render_template(
        "product.html",
        product=result["product"],
        offers=result["offers"],
        similar_products=result["similar_products"],
    )
