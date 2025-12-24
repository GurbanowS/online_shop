import re
from datetime import timedelta

from flask import current_app, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import check_password_hash, generate_password_hash

from shop import db
from shop.api import bp
from shop.admin.models import User as AdminUser
from shop.customers.models import Register, CustomerOrder
from shop.products.models import Addproduct, Brand, Category


def _product_to_dict(p: Addproduct):
    def img_url(filename: str):
        # Uploaded product images are stored under shop/static/images
        return f"/static/images/{filename}" if filename else None

    return {
        "id": p.id,
        "name": p.name,
        "price": float(p.price),
        "discount": int(p.discount or 0),
        "stock": int(p.stock),
        "colors": p.colors,
        "description": p.description,
        "category": {"id": p.category.id, "name": p.category.name} if p.category else None,
        "brand": {"id": p.brand.id, "name": p.brand.name} if p.brand else None,
        "images": [img_url(p.image_1), img_url(p.image_2), img_url(p.image_3)],
    }


@bp.get('/health')
def health():
    return jsonify({"status": "ok"})


@bp.get('/products')
def products_list():
    """List products.

    Query params:
      - q: search by name/description
      - category_id, brand_id: filters
    """
    q = (request.args.get('q') or '').strip()
    category_id = request.args.get('category_id')
    brand_id = request.args.get('brand_id')

    query = Addproduct.query
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(Addproduct.name.ilike(like), Addproduct.description.ilike(like))
        )
    if category_id and category_id.isdigit():
        query = query.filter_by(category_id=int(category_id))
    if brand_id and brand_id.isdigit():
        query = query.filter_by(brand_id=int(brand_id))

    items = query.order_by(Addproduct.id.desc()).all()
    return jsonify([_product_to_dict(p) for p in items])


@bp.get('/products/<int:product_id>')
def product_detail(product_id: int):
    p = Addproduct.query.get_or_404(product_id)
    return jsonify(_product_to_dict(p))


@bp.get('/categories')
def categories_list():
    cats = Category.query.order_by(Category.name.asc()).all()
    return jsonify([{"id": c.id, "name": c.name} for c in cats])


@bp.get('/brands')
def brands_list():
    brands = Brand.query.order_by(Brand.name.asc()).all()
    return jsonify([{"id": b.id, "name": b.name} for b in brands])


def _normalize_email(email: str) -> str:
    return (email or '').strip().lower()


@bp.post('/auth/register')
def register():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip() or 'Customer'
    username = (data.get('username') or '').strip() or re.sub(r'\W+', '', name.lower())
    email = _normalize_email(data.get('email'))
    password = (data.get('password') or '').strip()

    if not email or not password:
        return jsonify({"error": "email_and_password_required"}), 400

    if Register.query.filter_by(email=email).first():
        return jsonify({"error": "email_already_registered"}), 409

    # If legacy DB has plaintext passwords, we still store as hash for new users.
    user = Register(
        name=name,
        username=username,
        email=email,
        password=generate_password_hash(password),
        country=data.get('country'),
        city=data.get('city'),
        contact=data.get('contact') or 0,
        address=data.get('address'),
        zipcode=data.get('zipcode') or 0,
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "email": user.email, "username": user.username}), 201


@bp.post('/auth/login')
def login():
    data = request.get_json(silent=True) or {}
    email = _normalize_email(data.get('email'))
    password = (data.get('password') or '').strip()
    if not email or not password:
        return jsonify({"error": "email_and_password_required"}), 400

    user = Register.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "invalid_credentials"}), 401

    stored = user.password or ''
    # Support legacy plaintext passwords
    ok = stored == password or check_password_hash(stored, password)
    if not ok:
        return jsonify({"error": "invalid_credentials"}), 401

    token = create_access_token(
        identity={"type": "customer", "id": user.id, "email": user.email},
        expires_delta=timedelta(days=7),
    )
    return jsonify({"access_token": token, "user": {"id": user.id, "email": user.email, "name": user.name}})


@bp.get('/auth/me')
@jwt_required()
def me():
    ident = get_jwt_identity() or {}
    if ident.get('type') != 'customer':
        return jsonify({"error": "not_a_customer"}), 403
    user = Register.query.get_or_404(ident.get('id'))
    return jsonify({"id": user.id, "email": user.email, "name": user.name, "username": user.username})


@bp.post('/orders')
@jwt_required()
def create_order():
    ident = get_jwt_identity() or {}
    if ident.get('type') != 'customer':
        return jsonify({"error": "not_a_customer"}), 403

    data = request.get_json(silent=True) or {}
    items = data.get('items') or []
    if not isinstance(items, list) or not items:
        return jsonify({"error": "items_required"}), 400

    # Build legacy-compatible order payload
    orders_payload = {}
    for idx, item in enumerate(items, start=1):
        pid = item.get('product_id')
        qty = item.get('quantity', 1)
        if not isinstance(pid, int):
            return jsonify({"error": "invalid_product_id"}), 400
        if not isinstance(qty, int) or qty < 1:
            return jsonify({"error": "invalid_quantity"}), 400

        p = Addproduct.query.get(pid)
        if not p:
            return jsonify({"error": f"product_not_found:{pid}"}), 404
        orders_payload[str(pid)] = {
            "name": p.name,
            "price": float(p.price),
            "discount": int(p.discount or 0),
            "quantity": qty,
            "image": p.image_1,
            "colors": p.colors,
        }

    import secrets

    invoice = secrets.token_hex(5)
    order = CustomerOrder(invoice=invoice, customer_id=ident.get('id'), orders=orders_payload)
    db.session.add(order)
    db.session.commit()
    return jsonify({"invoice": invoice, "status": order.status, "id": order.id}), 201


@bp.get('/orders')
@jwt_required()
def list_my_orders():
    ident = get_jwt_identity() or {}
    if ident.get('type') != 'customer':
        return jsonify({"error": "not_a_customer"}), 403
    orders = CustomerOrder.query.filter_by(customer_id=ident.get('id')).order_by(CustomerOrder.id.desc()).all()
    return jsonify(
        [
            {
                "id": o.id,
                "invoice": o.invoice,
                "status": o.status,
                "date_created": o.date_created.isoformat(),
                "orders": o.orders,
            }
            for o in orders
        ]
    )


# ------------------------ Admin (simple) ------------------------


@bp.post('/admin/login')
def admin_login():
    data = request.get_json(silent=True) or {}
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '').strip()
    if not username or not password:
        return jsonify({"error": "username_and_password_required"}), 400

    user = AdminUser.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "invalid_credentials"}), 401

    stored = user.password or ''
    ok = stored == password or check_password_hash(stored, password)
    if not ok:
        return jsonify({"error": "invalid_credentials"}), 401

    token = create_access_token(
        identity={"type": "admin", "id": user.id, "username": user.username},
        expires_delta=timedelta(hours=12),
    )
    return jsonify({"access_token": token, "user": {"id": user.id, "username": user.username, "name": user.name}})


def _require_admin(ident):
    if (ident or {}).get('type') != 'admin':
        return False
    return True


@bp.post('/admin/products')
@jwt_required()
def admin_create_product():
    ident = get_jwt_identity() or {}
    if not _require_admin(ident):
        return jsonify({"error": "admin_required"}), 403

    data = request.get_json(silent=True) or {}
    required = ['name', 'price', 'stock', 'colors', 'description', 'category_id', 'brand_id']
    missing = [k for k in required if data.get(k) in (None, '')]
    if missing:
        return jsonify({"error": "missing_fields", "fields": missing}), 400

    p = Addproduct(
        name=data['name'],
        price=float(data['price']),
        discount=int(data.get('discount') or 0),
        stock=int(data['stock']),
        colors=data['colors'],
        description=data['description'],
        category_id=int(data['category_id']),
        brand_id=int(data['brand_id']),
        image_1=data.get('image_1') or 'image.jpg',
        image_2=data.get('image_2') or 'image.jpg',
        image_3=data.get('image_3') or 'image.jpg',
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(_product_to_dict(p)), 201


@bp.put('/admin/products/<int:product_id>')
@jwt_required()
def admin_update_product(product_id: int):
    ident = get_jwt_identity() or {}
    if not _require_admin(ident):
        return jsonify({"error": "admin_required"}), 403
    p = Addproduct.query.get_or_404(product_id)
    data = request.get_json(silent=True) or {}
    for field in ['name', 'colors', 'description', 'image_1', 'image_2', 'image_3']:
        if field in data:
            setattr(p, field, data[field])
    for field in ['price']:
        if field in data:
            setattr(p, field, float(data[field]))
    for field in ['discount', 'stock', 'category_id', 'brand_id']:
        if field in data:
            setattr(p, field, int(data[field]))
    db.session.commit()
    return jsonify(_product_to_dict(p))


@bp.delete('/admin/products/<int:product_id>')
@jwt_required()
def admin_delete_product(product_id: int):
    ident = get_jwt_identity() or {}
    if not _require_admin(ident):
        return jsonify({"error": "admin_required"}), 403
    p = Addproduct.query.get_or_404(product_id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"deleted": True})
