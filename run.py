from shop import create_app, db
from shop.products.models import Addproduct, Category, Brand
from shop.customers.models import Register, CustomerOrder
from shop.admin.models import User


app = create_app()


@app.shell_context_processor
def make_shell_processor():
    return {'db':db, 'Addproduct':Addproduct, 'Category':Category, 'Brand':Brand, 'Register': Register, 'CustomerOrder':CustomerOrder, 'User': User}

