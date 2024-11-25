from datetime import datetime

from sqlalchemy.orm import backref
from unwrap import db, login_manager,app
from flask_login import UserMixin
from flask import flash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20),unique=False, nullable=False)
    lastname = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    cart= db.relationship('Cart',backref='buyer',lazy=True)

    def add_to_cart(self,product_id):
        row_to_add=Cart(product_id=product_id,user_id=self.id)
        db.session.add(row_to_add)
        db.session.commit()
        flash("Your item has been added","success")


    def __repr__(self):
        return (f"User>'{self.firstname}',"f"'{self.lastname}','{self.email}'<")


class Products(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return (f"Product('{self.name}',"
                f"'{self.price}')")


class Cart(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    product_id=db.Column(db.Integer, db.ForeignKey('products.id'),nullable=False)
    quantity=db.Column(db.Integer, nullable=False,default=1)

    def __repr__(self):
        return (f"Cart('Product id:{self.product_id}',"
                f"'User id{self.user_id}')")







if __name__ == '__main__':
    pass