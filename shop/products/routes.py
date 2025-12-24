from flask import jsonify, render_template, redirect, request, url_for, flash, session, current_app
from flask_babel import _
from shop import db, search
from shop.products import bp
from .forms import Addproducts
from .models import Category, Brand, Addproduct
import os


def barnds():
    barnds = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return barnds


def categories():
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return categories


@bp.route('/api/products', methods=['GET'])
def get_products():
    products = Addproduct.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price
        }
        for p in products
    ])


@bp.route('/result')
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword,fields=['name', 'description'], limit=8)
    return render_template('products/result.html', title="Result", products=products, barnds=barnds(), categories=categories())


@bp.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html',title="About product", product=product, barnds=barnds(), categories=categories())


@bp.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    get_b = Brand.query.filter_by(id=id).first_or_404()
    brand = Addproduct.query.filter_by(brand = get_b).paginate(page=page, per_page=8)
    return render_template('products/index.html', title="Brand page", brand=brand, barnds=barnds(), categories=categories(), get_b=get_b)


@bp.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduct.query.filter_by(category = get_cat).paginate(page=page, per_page=8)
    return render_template('products/index.html', title="Category page", get_cat_prod=get_cat_prod, barnds=barnds(), categories=categories(), get_cat=get_cat)


@bp.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash(_("Please login first", "danger"))
        return redirect(url_for('ADMIN.login'))
    if request.method == 'POST':
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash (_("The Brand %(getbrand)s was added", getbrand=getbrand))
        db.session.commit()
        return redirect(url_for('products.homebrand'))
    return render_template('products/addbrand.html',brands='brands', title = 'Add brand')


@bp.route('/updatebrand/<int:id>', methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(_("Please login first"))
        return redirect(url_for('ADMIN.login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        updatebrand.name = brand
        flash(_('Your brand have succesfully updated'))
        db.session.commit()
        return redirect(url_for('ADMIN.brands'))
    return render_template('products/updatebrand.html', title='Update brand page', updatebrand=updatebrand)


@bp.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    if 'email' not in session:
        flash(_("Please login first"))
        return redirect(url_for('ADMIN.login'))
    deletebrand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(deletebrand)
        flash(_('Brand %(deletebrand)s has been succesfully deleted', deletebrand=deletebrand.name))
        db.session.commit()
        return redirect(url_for('ADMIN.brands'))
    flash(_('Brand %(deletebrand)s can\'t be deleted', deletebrand=deletebrand.name))


@bp.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash(_("Please login first"))
        return redirect(url_for('ADMIN.login'))
    if request.method == 'POST':
        getcategory = request.form.get('category')
        cat = Category(name=getcategory)
        db.session.add(cat)
        flash(_("The Category %(getcategory)s was added", getcategory=getcategory))
        db.session.commit()
        return redirect(url_for('products.addcat'))
    return render_template('products/addbrand.html', title = 'Add category')


@bp.route('/updatecategory/<int:id>', methods=['GET','POST'])
def updatecategory(id):
    if 'email' not in session:
        flash(_("Please login first"))
        return redirect(url_for('ADMIN.login'))
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecategory.name = category
        flash(_('Your category have succesfully updated'))
        db.session.commit()
        return redirect(url_for('ADMIN.categories'))
    return render_template('products/updatebrand.html', title='Update category page', updatecategory=updatecategory)


@bp.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    if 'email' not in session:
        flash(_("Please login first"))
        return redirect(url_for('ADMIN.login'))
    deletecategory = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(deletecategory)
        flash(_('Category %(deletecategory)s has been succesfully deleted', deletecategory=deletecategory.name ))
        db.session.commit()
        return redirect(url_for('ADMIN.categories'))
    flash(_('Category %(deletecategory)s can\'t be deleted', deletecategory=deletecategory.name))


@bp.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if 'email' not in session:
        flash(_("Please login first"))
        return redirect(url_for('ADMIN.login'))
    form = Addproducts(request.form)
    brands = Brand.query.all()
    categories = Category.query.all()
    if request.method =="POST" and 'image_1' in request.files:
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        description = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        addpro = Addproduct(name=name, price=price, discount=discount, stock=stock, colors=colors, description=description, brand_id=brand, category_id=category)
        db.session.add(addpro)
        flash(_("The product %(name)s has been added to your database", name=name))
        db.session.commit()
        return redirect(url_for('ADMIN.home'))
    return render_template('products/addproduct.html', title='Add product', form=form, brands=brands, categories=categories)


@bp.route('/updateproduct/<int:id>', methods = ['GET','POST'])
def updateproduct(id):
    if 'email' not in session:
        flash(_("Please login first"))
        return redirect(url_for('ADMIN.login'))
    form = Addproducts(request.form)
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.all()
    categories = Category.query.all()
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.stock = form.stock.data
        product.colors = form.colors.data
        product.description = form.description.data
              
        flash(_('Your product has been updated'))
        db.session.commit()
        return redirect(url_for('ADMIN.home'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.description.data = product.description
    brand = product.brand.name
    category = product.category.name
    return render_template('products/updateproduct.html', title='Update product', form=form, brands=brands, categories=categories, product=product)


@bp.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    if 'email' not in session:
        flash(_("Please login first"))
        return redirect(url_for('ADMIN.login'))
    deleteproduct = Addproduct.query.get_or_404(id)
    if request.method == 'POST':
        try:    
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + deleteproduct.image_1))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + deleteproduct.image_2))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + deleteproduct.image_3))
        except Exception as e:
            print(e) 
        db.session.delete(deleteproduct)
        flash(_('Product %(deleteproduct)s has been successfully deleted', deleteproduct=deleteproduct.name))
        db.session.commit()
        return redirect(url_for('ADMIN.home'))
    flash(_('Product %(deleteproduct)s can\'t be deleted', deleteproduct=deleteproduct.name))
    return redirect(url_for('ADMIN.home'))