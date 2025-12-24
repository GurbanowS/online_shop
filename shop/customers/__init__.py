from flask import Blueprint

bp = Blueprint('customers', __name__)

from shop.customers import routes