
from wtforms import Form
from wtforms import StringField,EmailField,TextAreaField,FileField, SubmitField,FloatField,BooleanField
from wtforms import validators
from wtforms import PasswordField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm
# http://wtforms.simplecodes.com/docs/0.6.1/fields.html#basic-fields
# from wtfroms import EmailField
from models import User

def length_honeypot(form, field):
    if len(field.data)>0:
        raise validators.ValidationError('el campo eesta vacio')

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")
    comment = TextAreaField('Comment',[
        validators.DataRequired(message='Text for the blog is rquired')])

class ModifyFile(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")
    comment = TextAreaField('Comment')

class NewProduct(FlaskForm):
    Pname = StringField('Product Name',[
        validators.DataRequired(message='the product name is required')])
    regular_price = FloatField('Price',[
        validators.DataRequired(message='the price is required')
    ])
    offer_price = FloatField('Price Offert',[
        validators.DataRequired(message='the Offert price is required')
    ])
    on_offer =BooleanField('On Offer?')
    file = FileField("Image")
    submit = SubmitField("Upload File")


class UpdateProduct(FlaskForm):
    Pname = StringField('Product Name')
    regular_price = FloatField('Price')
    offer_price = FloatField('Price Offert')
    on_offer =BooleanField('On Offer?')
    file = FileField("Image")
    submit = SubmitField("Upload File")

# class CommentForm(FlaskForm):
#     comment = TextAreaField('Comment',[
#         validators.DataRequired(message='Text for the blog is rquired')])
    
#     photfile = FileField("File", validators=[InputRequired()])
#     submit = SubmitField("Upload File")
    # submit = SubmitField("Upload File")

    # honeypot = StringField('',[length_honeypot])

class LoginForm(Form):
    username = StringField('Username',[
        validators.DataRequired(message='el username is rquired'),
        validators.length(min=4,max=25,message='ingrese un username valido')
    ])
    password= PasswordField('Password',[
        validators.DataRequired(message='el email is rquired')
    ])

class CreateForm(Form):
    username = StringField('Username',
        [
        validators.DataRequired(message='el username is rquired'),
        validators.length(min=4,max=25,message='ingrese un username valido')
        ])
    email = EmailField('Email',[
        validators.DataRequired(message='el email is rquired'),
        validators.Email(message='ingrese un email valido')
    ])
    password= PasswordField('Password',[
        validators.DataRequired(message='el Password is rquired')
    ])

    def validate_username(form, field):
        username=field.data
        user = User.query.filter_by(username=username).first()
        if user is not None:
            raise validators.ValidationError('Usuario ya registrado')
