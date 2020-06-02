from src.routes.data_routes import data_app
from src.routes.products_routes import products_app
from src.routes.scrapes_routes import scrapes_app


def init_routes(app):
    app.register_blueprint(data_app)
    app.register_blueprint(products_app)
    app.register_blueprint(scrapes_app)
