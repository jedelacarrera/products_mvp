from src.routes.data.routes import data_app
from src.routes.products.routes import products_app
from src.routes.scrapes.routes import scrapes_app


def init_routes(app):
    app.register_blueprint(data_app)
    app.register_blueprint(products_app)
    app.register_blueprint(scrapes_app)
