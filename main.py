from flask import Flask
from flask import render_template
from flask import request
from flask_wtf import CSRFProtect
from flask import make_response
from flask import session,redirect,url_for
from flask import flash
from config import DevelopmentConfig
from flask import copy_current_request_context
from werkzeug.utils import secure_filename

from sqlalchemy.exc import SQLAlchemyError

from models import db
from models import User,Comment,Products

import os
from werkzeug.utils import secure_filename

import forms
import json

from helper import date_format

from flask_mail import Mail
from flask_mail import Message

import threading

def send_email(user_email,username):
    msg = Message('Ya te registraste Prro',
                    sender = app.config['MAIL_USERNAME'],
                    recipients = [user_email])

    msg.html = render_template('email.html',user=username)
    mail.send(msg)

app = Flask(__name__) #nuevo objeto
app.config.from_object(DevelopmentConfig)
# csrf = CSRFProtect(app)
mail=Mail()
# este pedo sirve para evitar ataques de servidores  bueno primera fase

@app.before_request
def before_request():
    if 'username' not in session:
        print("el usuario necesita login")
    else:
        print(session['username'])
        # print(session['id'])

@app.after_request
def after_request(response):
    return response

@app.route('/')#wrap o und ecorador
def index():
    title = "My Blog"
    return render_template('index.html',title=title)

@app.route('/admin')#wrap o und ecorador
def admin():
    title = "Admin"
    return render_template('admin.html',title=title)


@app.route('/product/',methods=['GET'])#wrap o und ecorador
@app.route('/product/<int:page>',methods=['GET'])
def product(page=1):
    per_page = 5
    title = "Product List"
    product = Products.query.add_columns(
                                        Products.id,
                                        Products.product_name,
                                        Products.regular_price,
                                        Products.offer_price,
                                        Products.on_offer,
                                        Products.imageURL).paginate(page=page,per_page=per_page,error_out=False)
    return render_template('product.html',title=title,product=product)

@app.route('/cart',methods=['GET','POST'])#wrap o und ecorador
def cart():
    title = "New  Product"
    return render_template('cart.html',title=title)

@app.route('/newProduct',methods=['GET','POST'])#wrap o und ecorador
def newProduct():
    title = "New  Product"
    form = forms.NewProduct()
    if form.validate_on_submit():
        
        product = Products.query.all()
        try:
            number = product[-1].id
        except:        
            number = 0


        file = form.file.data # First grab the file
        oldName=file.filename
        newName=oldName[:oldName.find(".")]+str(number)+oldName[oldName.find("."):]
        file.filename=newName

        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER_PRODUCT'],file.filename)) # Then save the file

        
        products=Products(product_name=form.Pname.data,
                        regular_price=form.regular_price.data,
                        offer_price=form.offer_price.data,
                        on_offer=form.on_offer.data,
                        imageURL=file.filename
                        )
        
        db.session.add(products)

        try:
            db.session.commit()
            flash("New Iteam has been created") 
            return redirect(url_for('product'))
            
        except  SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash (error)



    return render_template('newProduct.html',title=title,form=form)

@app.route('/newBlog',methods=['GET','POST'])
def newBlog():
    title='New Post'
    form=forms.UploadFileForm()
    if form.validate_on_submit():
        
        # comment_list = Comment.query.join(User).order_by(Comment.id.desc()).first()
        comment_list = Comment.query.filter_by(user_id=session['id']).all()


        file = form.file.data # First grab the file
        oldName=file.filename
        newName=oldName[:oldName.find(".")]+str(comment_list[-1].id)+oldName[oldName.find("."):]
        file.filename=newName

        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],file.filename)) # Then save the file
        
        user_id=session['id']
        comment=Comment(user_id=user_id,
                        text=form.comment.data,
                        imageURL=file.filename
                        )
        
        db.session.add(comment)

        try:
            db.session.commit()
            flash("New Blog have been created") 
            
        except  SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash (error)

        

    return render_template('newBlog.html',title=title,form=form)  

@app.route('/login',methods=['GET','POST'])#wrap o und ecorador
def login():
    login_form = forms.LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        
        username =login_form.username.data
        password =login_form.password.data
        
        user=User.query.filter_by(username = username).first()
        if user is not None and user.verify_password(password):
            success_message='bienvenido prro {}'.format(username)
            session['username'] = login_form.username.data
            session['id']=user.id
            session['admin']=user.admin
            flash(success_message)
            return redirect(url_for('index'))
        else:
            success_message='Usuario o contraseña no valida'
            flash(success_message)

        
    return render_template('login.html',form = login_form)

@app.route('/logout')#wrap o und ecorador
def logout():
    if 'username' in session:
        session.pop('username')#quita la sesion
    return redirect(url_for('login'))

@app.route('/reviews/',methods=['GET'])
@app.route('/reviews/<int:page>',methods=['GET'])
def reviews(page=1):
    per_page = 5
    comment_list = Comment.query.join(User).add_columns(
                                            Comment.id,
                                            User.username,
                                            Comment.create_date,
                                            Comment.text,
                                            Comment.imageURL).paginate(page=page,per_page=per_page,error_out=False)
    return render_template('reviews.html',comments=comment_list,date_format=date_format )

@app.route('/update/',methods=['GET','POST'])
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    # CommentUpdated= Comment.query.filter_by(id=id).first()
    title='Modify Post'
    form=forms.UploadFileForm()
    CommentUpdated = Comment.query.filter_by(id=id).first()
    form.comment.data = CommentUpdated.text


    if form.validate_on_submit():
        
        # comment_list = Comment.query.join(User).order_by(Comment.id.desc()).first()
        CommentUpdated.text=CommentUpdated.text
        file = form.file.data
        # print("--------------------------------------------------")
        # print(form.comment.data)
        # print(file.filename)
        # exit()
        if form.comment.data != None:
            CommentUpdated.text = form.comment.data

        if file.filename != None:
            file = form.file.data
            try:
                os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],CommentUpdated.imageURL))
            except:
                # print(error)
                print("File path can not be removed")
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],CommentUpdated.imageURL)) # Then save the file

        
        user_id=session['id']
        comment=Comment(user_id=user_id,
                        text=form.comment.data,
                        imageURL=file.filename
                        )
        

        db.session.add(comment)

        try:
            db.session.commit()
            flash("Blog has been modify") 
            
        except  SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash (error)

    return render_template('update.html',comments=CommentUpdated,form=form,title=title )


@app.route('/updateProduct/',methods=['GET','POST'])
@app.route('/updateProduct/<int:id>',methods=['GET','POST'])
def updateProduct(id):
    # CommentUpdated= Comment.query.filter_by(id=id).first()
    title='Modify Product'
    form=forms.UpdateProduct()
    ProductUpdated = Products.query.filter_by(id=id).first()


    if form.validate_on_submit():
        

        if form.Pname.data != None:
            ProductUpdated.product_name = form.Pname.data

        if form.regular_price.data != None:
            ProductUpdated.regular_price = form.regular_price.data

        if form.offer_price.data != None:
            ProductUpdated.offer_price = form.offer_price.data

        if form.on_offer.data != None:
            ProductUpdated.on_offer = form.on_offer.data

        if form.file.data != None:
            file = form.file.data
            try:
                os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER_PRODUCT'],ProductUpdated.imageURL))
            except:
                # print(error)
                print("File path can not be removed")
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER_PRODUCT'],ProductUpdated.imageURL)) # Then save the file
        

        

        db.session.add(ProductUpdated)

        try:
            db.session.commit()
            flash("Product has been modify") 
            
        except  SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash (error)


    
    form.Pname.data = ProductUpdated.product_name
    form.regular_price.data = ProductUpdated.regular_price
    form.offer_price.data = ProductUpdated.offer_price
    form.on_offer.data = ProductUpdated.on_offer
    return render_template('updateProduct.html',product=ProductUpdated,form=form,title=title )

@app.route('/create',methods=['GET','POST'])#wrap o und ecorador
def create():
    create_form = forms.CreateForm(request.form)
    if request.method == 'POST' and create_form.validate():
        
        user = User(create_form.username.data,
                    create_form.password.data,
                    create_form.email.data)
        db.session.add(user)#inicia la instancia para agregar
        db.session.commit()#ejecutra la instancia 
        
        @copy_current_request_context
        def send_message(email, username):
            send_email(email,username)

        sender = threading.Thread(name='mail_sender',
                                  target=send_message,
                                  args=(user.email,user.username))

        sender.start()

        username =create_form.username.data
        success_message='bienvenido usuario {}'.format(username)
        flash(success_message)

    return render_template('create.html',form = create_form)

@app.route('/client')#wrap o und ecorador
def client():
    list_name=['puto1','puto2','puto3']
    title = "curso flask"
    return render_template('client.html', list_name=list_name,title=title)

@app.route('/cookie')#wrap o und ecorador 
def cookie():
    response = make_response(render_template('cookie.html'))#este pedo sirve para poner las cookies
    response.set_cookie('custome_cookie','kike')
    return response

@app.route('/store/',methods=['GET'])#wrap o und ecorador
@app.route('/store/<int:page>',methods=['GET'])
def store(page=1):
    per_page = 5
    title = "Store"
    product = Products.query.add_columns(
                                        Products.id,
                                        Products.product_name,
                                        Products.regular_price,
                                        Products.offer_price,
                                        Products.on_offer,
                                        Products.imageURL).paginate(page=page,per_page=per_page,error_out=False)
    return render_template('store.html',title=title,product=product)

@app.route('/addCart',methods=["POST"])
def addCart():
    # https://stackoverflow.com/questions/33775017/flask-python-where-should-i-put-goods-that-go-to-cart-in-online-shop
    # print("**-----------------------------------------------------***")
    # print("entro al addcart")
    dictionary=request.form
    vote=dictionary['data']
    html=''
    if 'cart' in session:
        if session['cart'] is None:
            session['cart'] = [vote]
            for x in session['cart']:
                html+='<tr>'+x+'</tr>'

            response = {'status':200,'html':str(html)}
        elif  vote not in session['cart']:
            # print(session['cart'])
            # print("entro cuando no esta")
            session['cart'].append(vote)
            session['cart'] = session['cart'] 
            
            for x in session['cart']:
                html+='<tr>'+x+'</tr>'

            response = {'status':200,'html':str(html)}
        else:
            # print(session['cart'])
            # print("entro cuando esta")
            # for x in session['cart']:
            #     html+='<tr><td>'+x+'</td>'
            #     html+='<td><button type="button" class="btn btn-danger">Danger</button></td></tr>'
            response = {'status':200,'html':str(html)}
    else:
        print("entro cuando se inicializa")
        
        html=''
        # for x in session['cart']:
        #     html+='<tr>'+x+'</tr>'
        session['cart'] = [vote]
        response = {'status':200,'html':str(html)}

    # print(session['cart'])
    # print(html)
    return json.dumps(response)

@app.route('/displaycart',methods=["POST"])
def displaycart():
    html=''
    if 'cart' in session and session['cart'] is not None:
        # exit()
            queryproducts = Products.query.filter(Products.id.in_(session['cart']))
            for product in queryproducts:
                html+='<tr><td>'+product.product_name+'</td>'
                html+='<td><div class="btn btn-danger deleterow" data-badges="'+str(product.id)+'">Danger</div></td></tr>'
            response = {'status':200,'html':str(html)}
    
    else:
        html+='<tr><td>CART EMPTY</td>'
        html+='<td></tr>'
        response = {'status':400,'html':str(html)}

    return json.dumps(response)

@app.route('/deleteProduct',methods=["POST"])
def deleteProduct():
    dictionary=request.form
    id=dictionary['data']
    try:

        session['cart']=session['cart'].remove(id)
        response = {'status':200}
    except:
        response = {'status':400}

    return json.dumps(response)

@app.route('/ajax-login',methods=['POST'])
def ajax_login():
    print("entro a ajax_login")
    # print(request.form)
    # print(type(request.form))
    # dictionary=request.form
    # print(dictionary['username'])
    username=request.form['username']
    response ={'status':200,'username':username,'id':1}
    return json.dumps(response)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__ == '__main__':
    # csrf.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port = 8500)# se encarga de ejecutar el servidor