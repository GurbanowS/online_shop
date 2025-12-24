from flask_babel import lazy_gettext as _l
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, FloatField, validators

class Addproducts(Form):
    name = StringField(_l('Name'), [validators.DataRequired()])
    price = FloatField(_l('Price'), [validators.DataRequired()])
    discount = IntegerField(_l('Discount'), default=0)
    stock = IntegerField(_l('Stock'), [validators.DataRequired()])
    description = TextAreaField(_l('Description'), [validators.DataRequired()])
    colors = TextAreaField(_l('Colors'), [validators.DataRequired()])
    image_1 = FileField(_l('Image 1'), validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_2 = FileField(_l('Image 2'), validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_3 = FileField(_l('Image 3'), validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])





