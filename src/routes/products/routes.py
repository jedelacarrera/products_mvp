from flask import Blueprint, request, render_template
from src.routes.products import controllers

products_app = Blueprint("projects", __name__, url_prefix="/products")


@products_app.route("/", methods=["GET"])
def get_products():
    search = request.args.get("search", "")
    selected_category = request.args.get("category", "")
    provider_id = int("0" + request.args.get("provider", ""))
    sales_only = bool(request.args.get("sales_only"))
    products = controllers.get_products(
        search=search,
        provider_id=provider_id,
        sales_only=sales_only,
        category=selected_category,
    )
    category_list = controllers.get_category_list()
    return render_template(
        "products.html",
        search=search,
        provider_id=provider_id,
        categories=products["categories"],
        providers=controllers.get_providers(),
        sales_only=sales_only,
        category_list=category_list,
        selected_category=selected_category,
    )


@products_app.route("/<pid>/", methods=["GET"])
def product(pid):
    result = controllers.get_offers_by_product(pid)
    category_list = controllers.get_category_list()
    return render_template(
        "product.html",
        product=result["product"],
        offers=result["offers"],
        similar_products=result["similar_products"],
        providers=controllers.get_providers(),
        category_list=category_list,
    )
