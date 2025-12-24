from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_msearch import Search
from flask_login import LoginManager
from flask_babel import Babel, lazy_gettext as _l
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config


db = SQLAlchemy()
migrate = Migrate()
search = Search()
babel = Babel()
jwt = JWTManager()


login_manager = LoginManager()
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = _l("Please login First")



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # JWT secret can be overridden via env var.
    app.config.setdefault('JWT_SECRET_KEY', app.config.get('SECRET_KEY'))

    # Allow local React dev server.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    jwt.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    search.init_app(app)
    babel.init_app(app)
    migrate.init_app(app, db)

    from shop.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from shop.products import bp as products_bp
    app.register_blueprint(products_bp)

    from shop.carts import bp as carts_bp
    app.register_blueprint(carts_bp)

    from shop.customers import bp as customers_bp
    app.register_blueprint(customers_bp)

    from shop.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # JSON API for the React frontend
    from shop.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Serve built React app (optional production setup).
    # When you run `npm run build` inside `frontend/`, Flask will serve it.
    react_build = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build')
    react_build = os.path.abspath(react_build)
    if os.path.isdir(react_build):
        from flask import send_from_directory

        @app.route('/')
        @app.route('/products')
        @app.route('/products/<path:_any>')
        @app.route('/cart')
        @app.route('/checkout')
        @app.route('/login')
        @app.route('/register')
        @app.route('/admin')
        def react_app(_any=None):
            return send_from_directory(react_build, 'index.html')

        @app.route('/static/react/<path:filename>')
        def react_static(filename):
            return send_from_directory(os.path.join(react_build, 'static'), filename)

    @app.context_processor
    def inject_conf_var():
        return dict(
            AVAILABLE_LANGUAGE=app.config['LANGUAGES'],
            CURRENT_LANGUAGE=session.get('language','en')
        )
    return app


@babel.localeselector
def get_locale():
    try:
        language = session['language']
    except KeyError:
        language = None
    if language:
        return language
    return 'ru'