import csv

from unwrap import db, app
from my51eshop_class1111.unwrap.user.models import Products


def main():
    with open("products.csv",encoding="utf-16") as f:
        reader=csv.reader(f)
        for name,price,description in reader:
            product=Products(name=name,price=price,
                             description=description)
            db.session.add(product)
            print(product)
        db.session.commit()





if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        main()
