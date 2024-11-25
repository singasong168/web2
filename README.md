# E-Commerce Web App Using Python Flask and SQLAlchemy.
Once logged in, users can:
- Add products to their shopping cart
- Update the quantity, or Remove items
- See the total cost

The database includes 3 models: User, Products and Cart. When a user add a product to his cart, a new "cart item" will be added
to the Cart model with the user id and product id.

## How to run this application locally

To install all the packages, run:

```
pip install -r requirements.txt
```
Create DB and imports data

```

python imports.py

```
Then run:

```
python run.py
```


## Resources
