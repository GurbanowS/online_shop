from flask import render_template, session, request, redirect, url_for, flash, current_app
from flask_babel import _
from shop import db
from .forms import RegistrationForm, LoginForm
from .models import User
from shop.products.models import Addproduct, Brand, Category
from shop.admin import bp
import os


@bp.route('/admin')
def home():
    if 'email' not in session:
        flash(_("Please login first"))
        return redirect(url_for('ADMIN.login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title ='Admin page', products=products)


@bp.route('/brands')
def brands():
    if 'email' not in session:
        flash(_("Please login first"))
        return redirect(url_for('ADMIN.login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='Brand page', brands=brands)


@bp.route('/categories')
def categories():
    if 'email' not in session:
        flash(_("Please login first"))
        return redirect(url_for('ADMIN.login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title='Category page', categories=categories)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name = form.name.data, username = form.username.data, email = form.email.data, password = form.password.data)
        db.session.add(user)
        flash(_('Welcome %(name)s. Thank you for registering', name=form.name.data))
        db.session.commit()
        return redirect(url_for('ADMIN.login'))
    return render_template('admin/register.html', form=form, title = 'Registration page')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data, password = form.password.data).first()
        if user:
            session['email'] = form.email.data
            flash(_('Welcome email, You are logedin', email=form.email.data))
            return redirect(url_for('ADMIN.home'))
        else:
            flash(_('Wrong password or email please try again'))
            return redirect(url_for('ADMIN.login'))
    return render_template('admin/login.html', form=form, title='Login page')
        

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('products.index'))