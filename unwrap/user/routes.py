import os
import secrets
from itertools import product



from flask import render_template, url_for, flash, redirect, request, Blueprint
from unwrap import app, db, bcrypt
from unwrap.user.models import Products,User,Cart
from unwrap.user.forms import RegistrationForm, LoginForm,UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func, update

user_bp=Blueprint('user',__name__,template_folder='templates',static_folder='static',static_url_path="/user/static")


def getLoginDetails():
   if current_user.is_authenticated:
       noOfItems=Cart.query.filter_by(buyer=current_user).count()
   else:
       noOfItems=0
   return noOfItems



@user_bp.route("/")
@user_bp.route("/home")
def home():
    return render_template("home.html")

@user_bp.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
      return redirect(url_for("user.home"))
  form=RegistrationForm()
  if form.validate_on_submit():
      try:
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user=User(firstname=form.firstname.data,lastname=form.lastname.data,password=hashed_password,
                email=form.email.data)
        #ic(user)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created","success")
        return redirect(url_for("user.login"))

      except Exception as e:
          print(e)
          flash("Something wrong!", "danger")
          db.session.rollback()
          return redirect(url_for("user.register"))

      finally:
          db.session.close()

  return render_template("register.html",form=form)

@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("user.home"))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for("user.home"))
        else:
            flash("Please check your username and password","danger")

    return render_template("login.html",form=form,noOfItems=getLoginDetails())


@user_bp.route("/logout")
@login_required
def logout():
   logout_user()
   return redirect(url_for("user.home"))

@user_bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
  form=UpdateAccountForm()
  if form.validate_on_submit():
      current_user.firstname=form.firstname.data
      current_user.lastname = form.lastname.data
      current_user.email = form.email.data
      db.session.commit()
      flash("Update success!!","success")
      return redirect(url_for("account"))
  elif request.method == "GET":
      form.firstname.data=current_user.firstname
      form.lastname.data=current_user.lastname
      form.email.data=current_user.email

  return render_template("account.html",form=form,noOfItems=getLoginDetails())


@user_bp.route("/unwrap-project")
def unwrap_project():
   return render_template("unwrap-project.html")


@user_bp.route("/how-it-works")
def how_it_works():
     pass


@user_bp.route("/select_products", methods=['GET', 'POST'])
def select_products():
    products=Products.query.all()
    return render_template("select_products.html",products=products,noOfItems=getLoginDetails())



@user_bp.route("/addToCart/<int:product_id>")
@login_required
def addToCart(product_id):
  #商品已经在购物车内了，商品数量+1
  row=Cart.query.filter_by(product_id=product_id,buyer=current_user).first()

  if row:
      row.quantity +=1
      db.session.commit()
      flash("This item is already in the cart! Qyt+1!","success")
  # 商品不在购物车内，添加该商品
  else:
      user=User.query.get(current_user.id)
      user.add_to_cart(product_id)

  return redirect(url_for("user.select_products"))





@user_bp.route("/cart", methods=["GET", "POST"])
@login_required
def cart():

     #Products.id, Cart.quantity, Products.price ,Products.name
    cart= (Products.query.join(Cart)
           .add_columns(Cart.quantity,
                        Products.price, Products.name,
                        Products.id).filter_by(buyer=current_user).all())
    subtotal=0
    for item in cart:
        subtotal+= int(item.price)*int(item.quantity)

    if request.method== "POST":
        qty=request.form.get("qty")
        idpd=request.form.get("idpd")
        cartitem=Cart.query.filter_by(product_id=idpd).first()
        cartitem.quantity=qty
        db.session.commit()
        cart = (Products.query.join(Cart)
                .add_columns(Cart.quantity,
                             Products.price, Products.name,
                             Products.id).filter_by(buyer=current_user).all())
        subtotal = 0
        for item in cart:
            subtotal += int(item.price) * int(item.quantity)


    return render_template("cart.html",cart=cart,subtotal=subtotal,noOfItems=getLoginDetails())



@user_bp.route("/removeFromCart/<int:product_id>")
@login_required
def removeFromCart(product_id):
    item_to_remove=Cart.query.filter_by(product_id=product_id).first()
    db.session.delete(item_to_remove)
    db.session.commit()
    flash("Your item has been removed","success")
    return redirect(url_for("user.cart"))
