from flask import Blueprint

bp = Blueprint('carts',__name__)

from shop.carts import carts