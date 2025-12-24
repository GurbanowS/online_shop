from flask import render_template, redirect, request, url_for, flash, session, current_app, make_response
from flask_login import login_required, current_user, logout_user, login_user
from flask_babel import _
from shop import db, login_manager
from shop.customers import bp
from .forms import CustomerRegisterForm, CustomerLoginForm
from .models import Register, CustomerOrder
import secrets, os
import json
import pdfkit
import stripe


publishable_key = 'pk_test_51KafOcIqqq3Njx21tbV3TU2sfxaRxLYokHbyj9r2diALpF9JQISmyLIgbHPkTcH6TH8tZeoHlgoqMHmKICtvzVye00bup1vMp4'

stripe.api_key = 'sk_test_51KafOcIqqq3Njx21v9QT9530qJHgqgQSijSpeGI6RksWf5bgqfakAephyaPV2Q1bTzUy3PFHcDYWnd4pWf02nHyX00qAgi2yGP'


@bp.route('/payment', methods=['POST'])
@login_required
def payment():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        description='Myshop',
        amount=amount,
        currency='usd',
    )
    orders = CustomerOrder.query.filter_by(customer_id=current_user.id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
    orders.status = _('Paid')
    db.session.commit()
    return redirect(url_for('customers.thanks'))


@bp.route('/thanks')
def thanks():
    return render_template('customer/thank.html')


@bp.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        user = Register(name=form.name.data, username=form.username.data, email=form.email.data, password=form.password.data, country=form.country.data,
                        city=form.city.data, contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data, )
        db.session.add(user)
        flash(_('Welcome %(username)s. Thank you for registering', username=form.username.data,))
        db.session.commit()
        return redirect(url_for('customers.customerLogin'))
    return render_template('customer/register.html', title="Register", form=form)


@bp.route('/customer/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data, password=form.password.data).first()
        if user:
            login_user(user)
            flash(_('You are logedin!'))
            return redirect(url_for('products.index'))
        else:
            flash(_('Incorrect email or password'))
            return redirect(url_for('customers.customerLogin'))
    return render_template('customer/login.html', title="Login", form=form)



@bp.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('customers.customerLogin'))


def updateshopping():
    for _key, product in session['Shoppingcart'].items():
        session.modified = True
        del product['image']
        del product['colors']
    return updateshopping


@bp.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        updateshopping()
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash(_('Your order has been sent successfully'))
            return redirect(url_for('customers.orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash(_('Something went wrong while get order'))
            return redirect(url_for('customers.GetCart'))
        

@bp.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        subtotal = 0
        grandTotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            discount = (product['discount'] / 100) * float(product['price'])
            subtotal += float(product['price']) * int(product['quantity'])
            subtotal -= discount * int(product['quantity'])
            grandTotal = ("%.2f" % (1.00 * float(subtotal)))
    else:
        return redirect(url_for('customers.customerLogin'))
    return render_template('customer/order.html', title='Order place', invoice=invoice, subtotal=subtotal, grandTotal=grandTotal, customer=customer, orders=orders)



@bp.route('/get_pdf/<invoice>', methods=['GET', 'POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        subtotal = 0
        customer_id = current_user.id
        if request.method == 'POST':    
            customer = Register.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
            for _key, product in orders.orders.items():
                discount = (product['discount'] / 100) * float(product['price'])
                subtotal += float(product['price']) * int(product['quantity'])
                subtotal -= discount * int(product['quantity'])
            rendered = render_template('customer/pdf.html', title='Order place', invoice=invoice, subtotal=subtotal, customer=customer, orders=orders)
            pdf = pdfkit.from_string(rendered, False)
            response=make_response(pdf)
            response.headers['content-Type'] = 'application/pdf'
            response.headers['content-Disposition'] = 'atteched; filename'+invoice+'.pdf'
            return response
    return redirect(url_for('customers.orders'))


@bp.route('/language/<language>')
def set_language(language=None):
    session['language'] = language
    if language == 'en':
        language = 'en'
    else:
        language = 'ru'
    return redirect(request.referrer)