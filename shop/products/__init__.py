from flask import Blueprint

bp = Blueprint('products', __name__)

from shop.products import routes