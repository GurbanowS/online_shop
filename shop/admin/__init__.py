from flask import Blueprint

bp = Blueprint('ADMIN', __name__)

from shop.admin import routes