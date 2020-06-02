from src.app import app
from src.dbconfig import init_db
from src.routes import init_routes

db = init_db(app)
routes = init_routes(routes)
