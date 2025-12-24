from flask import Blueprint


bp = Blueprint('api', __name__)


from shop.api import routes  # noqa: E402,F401
