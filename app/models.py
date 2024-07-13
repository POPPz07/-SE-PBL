from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login,app
import csv

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))


    def repr(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(128), nullable=False)
    image_url = db.Column(db.String(256))  # Field for storing image URL
    price = sa.Column(sa.Float, nullable=False)
    buy_link = db.Column(db.String(256))  # Field for storing buy link

    def repr(self):
        return f'<Product {self.name}>'

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

def insert_product(name, image_url, price, buy_link):
    with app.app_context():
        existing_product = Product.query.filter_by(name=name, price=price).first()
        if existing_product:
            # Product with the same name and price already exists
            print(f"Product '{name}' with price {price} already exists in the database.")
            return

        new_product = Product(
            name=name,
            image_url=image_url,
            price=price,
            buy_link=buy_link
        )
        db.session.add(new_product)
        db.session.commit()

'''
insert_product("(Refurbished) Samsung Galaxy Z Flip5 5G (Cream, 8GB RAM, 256GB Storage)",
                "https://m.media-amazon.com/images/I/71rMdsTWkmL.AC_UY218.jpg",
                86864,
                "https://www.amazon.in/sspa/click?ie=UTF8&spc=MToxNDUwMzgwNzY4ODM4MDkyOjE3MTIwNTEzODk6c3BfYXRmOjMwMDE1NTQ5ODU2MTQzMjo6MDo6&url=%2FRefurbished-Samsung-Galaxy-Flip5-Storage%2Fdp%2FB0CJPJ8ZH7%2Fref%3Dsr_1_1_sspa%3Fcrid%3DWTDJI4DAOHOJ%26dib%3DeyJ2IjoiMSJ9.urohL2km_b63T36Wq3YoqcXWRZdGqLatJ-CrmP0jueQSG6mGv6COA96WQO1p19vhN0q7upElwwNUDq3bcpyFzTa8JrO1CXNAlFqwxZyUqdyLzEIlJ9aqJsn42tVGvfZSVuh_JoCS-zawQGSoAbjymMp150GKDLteS2tRTTOFu7yeHhFL3Nv-XxlaiDM1pUiWr0E7bnlCY2noiLf4oQ7PQ3ZaeMDrddyTbMQLFSMurG0.hsxadK2Xc_lSmd9DXqA4F-eNLVIL1emKuBFTRjjvZsY%26dib_tag%3Dse%26keywords%3Dsamsung%2Bmobiles%26qid%3D1712051389%26sprefix%3Dsamsung%2Bmobile%252Caps%252C215%26sr%3D8-1-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1")
insert_product("HP",
                "https://m.media-amazon.com/images/I/71rMdsTWkmL.AC_UY218.jpg",
                86864,
                "https://www.amazon.in/sspa/click?ie=UTF8&spc=MToxNDUwMzgwNzY4ODM4MDkyOjE3MTIwNTEzODk6c3BfYXRmOjMwMDE1NTQ5ODU2MTQzMjo6MDo6&url=%2FRefurbished-Samsung-Galaxy-Flip5-Storage%2Fdp%2FB0CJPJ8ZH7%2Fref%3Dsr_1_1_sspa%3Fcrid%3DWTDJI4DAOHOJ%26dib%3DeyJ2IjoiMSJ9.urohL2km_b63T36Wq3YoqcXWRZdGqLatJ-CrmP0jueQSG6mGv6COA96WQO1p19vhN0q7upElwwNUDq3bcpyFzTa8JrO1CXNAlFqwxZyUqdyLzEIlJ9aqJsn42tVGvfZSVuh_JoCS-zawQGSoAbjymMp150GKDLteS2tRTTOFu7yeHhFL3Nv-XxlaiDM1pUiWr0E7bnlCY2noiLf4oQ7PQ3ZaeMDrddyTbMQLFSMurG0.hsxadK2Xc_lSmd9DXqA4F-eNLVIL1emKuBFTRjjvZsY%26dib_tag%3Dse%26keywords%3Dsamsung%2Bmobiles%26qid%3D1712051389%26sprefix%3Dsamsung%2Bmobile%252Caps%252C215%26sr%3D8-1-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1")
insert_product("apple",
                "https://m.media-amazon.com/images/I/71rMdsTWkmL.AC_UY218.jpg",
                86864,
                "https://www.amazon.in/sspa/click?ie=UTF8&spc=MToxNDUwMzgwNzY4ODM4MDkyOjE3MTIwNTEzODk6c3BfYXRmOjMwMDE1NTQ5ODU2MTQzMjo6MDo6&url=%2FRefurbished-Samsung-Galaxy-Flip5-Storage%2Fdp%2FB0CJPJ8ZH7%2Fref%3Dsr_1_1_sspa%3Fcrid%3DWTDJI4DAOHOJ%26dib%3DeyJ2IjoiMSJ9.urohL2km_b63T36Wq3YoqcXWRZdGqLatJ-CrmP0jueQSG6mGv6COA96WQO1p19vhN0q7upElwwNUDq3bcpyFzTa8JrO1CXNAlFqwxZyUqdyLzEIlJ9aqJsn42tVGvfZSVuh_JoCS-zawQGSoAbjymMp150GKDLteS2tRTTOFu7yeHhFL3Nv-XxlaiDM1pUiWr0E7bnlCY2noiLf4oQ7PQ3ZaeMDrddyTbMQLFSMurG0.hsxadK2Xc_lSmd9DXqA4F-eNLVIL1emKuBFTRjjvZsY%26dib_tag%3Dse%26keywords%3Dsamsung%2Bmobiles%26qid%3D1712051389%26sprefix%3Dsamsung%2Bmobile%252Caps%252C215%26sr%3D8-1-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1")
insert_product("momo",
                "https://m.media-amazon.com/images/I/71rMdsTWkmL.AC_UY218.jpg",
                86864,
                "https://www.amazon.in/sspa/click?ie=UTF8&spc=MToxNDUwMzgwNzY4ODM4MDkyOjE3MTIwNTEzODk6c3BfYXRmOjMwMDE1NTQ5ODU2MTQzMjo6MDo6&url=%2FRefurbished-Samsung-Galaxy-Flip5-Storage%2Fdp%2FB0CJPJ8ZH7%2Fref%3Dsr_1_1_sspa%3Fcrid%3DWTDJI4DAOHOJ%26dib%3DeyJ2IjoiMSJ9.urohL2km_b63T36Wq3YoqcXWRZdGqLatJ-CrmP0jueQSG6mGv6COA96WQO1p19vhN0q7upElwwNUDq3bcpyFzTa8JrO1CXNAlFqwxZyUqdyLzEIlJ9aqJsn42tVGvfZSVuh_JoCS-zawQGSoAbjymMp150GKDLteS2tRTTOFu7yeHhFL3Nv-XxlaiDM1pUiWr0E7bnlCY2noiLf4oQ7PQ3ZaeMDrddyTbMQLFSMurG0.hsxadK2Xc_lSmd9DXqA4F-eNLVIL1emKuBFTRjjvZsY%26dib_tag%3Dse%26keywords%3Dsamsung%2Bmobiles%26qid%3D1712051389%26sprefix%3Dsamsung%2Bmobile%252Caps%252C215%26sr%3D8-1-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1")
'''
"""
insert_product('POCO C55 Cool Blue', 'Description of POCO C55 Cool Blue', 199.99, 50, 'https://www.amazon.in/POCO-C55-Cool-Blue-128/dp/B0BX9WNP7W/?encoding=UTF8&ref=dlx_gate_sd_dcl_tlt_88cdcaa6_dt_pd_gw_unk&pd_rd_w=Dm4QT&content-id=amzn1.sym.9e4ae409-2145-4395-aa6e-45d7f3e95c3e&pf_rd_p=9e4ae409-2145-4395-aa6e-45d7f3e95c3e&pf_rd_r=EBGNCYQP11R0ZWTA9C5D&pd_rd_wg=G81ec&pd_rd_r=fd976c3e-8e98-4c41-846c-a41afd6be398&th=1')

insert_product('Realme Smartphone', 'Description of realme', 199.99, 50,'https://www.amazon.in/realme-Display-Premium-Leather-SUPERVOOC/dp/B0C788SHHC/?encoding=UTF8&ref=dlx_gate_sd_dcl_tlt_6f147dbb_dt_pd_gw_unk&pd_rd_w=Dm4QT&content-id=amzn1.sym.9e4ae409-2145-4395-aa6e-45d7f3e95c3e&pf_rd_p=9e4ae409-2145-4395-aa6e-45d7f3e95c3e&pf_rd_r=EBGNCYQP11R0ZWTA9C5D&pd_rd_wg=G81ec&pd_rd_r=fd976c3e-8e98-4c41-846c-a41afd6be398&th=1')

# Usage example:
insert_product('Product 1', 'Description of Product 1', 10.99, 50)
insert_product('Product 2', 'Description of Product 2', 19.99, 100)
insert_product('Product 3', 'Description of Product 3', 29.99, 200)
"""
def delete_all_products():
    with app.app_context():
        with db.session.begin():
            db.session.query(Product).delete()
delete_all_products()

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    user = db.relationship("User", backref=db.backref("wishlist", lazy="dynamic"))
    product = db.relationship("Product", backref=db.backref("wishlist", lazy="dynamic"))

def add_products_from_csv(csv_file):
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Check if product_price is empty
            if row['product_price']:
                try:
                    name = row['product_name']
                    price = float(row['product_price'])
                    image_url = row['product_images']
                    buy_link = row['product_hyperlinks']
                    insert_product(name, image_url, price, buy_link)

                    # Process the rest of the code here
                except ValueError:
                    print(f"Could not convert '{row['product_price']}' to float")
            else:
                print("Product price is empty for this row")


add_products_from_csv(r'C:\Users\Virendra\PycharmProjects\flaskPBL\app\amazon_products_nike.csv')
add_products_from_csv(r'C:\Users\Virendra\PycharmProjects\flaskPBL\app\amazon_products.csv')
add_products_from_csv(r'C:\Users\Virendra\PycharmProjects\flaskPBL\app\products.csv')
add_products_from_csv(r'C:\Users\Virendra\PycharmProjects\flaskPBL\app\myntra_products.csv')
add_products_from_csv(r'C:\Users\Virendra\PycharmProjects\flaskPBL\app\flipkart_nike.csv')
add_products_from_csv(r'C:\Users\Virendra\PycharmProjects\flaskPBL\app\flipkart_smartwatches.csv')
add_products_from_csv(r'C:\Users\Virendra\PycharmProjects\flaskPBL\app\amazon_iphone.csv')
add_products_from_csv(r'C:\Users\Virendra\PycharmProjects\flaskPBL\app\amazon_smartwatches.csv')
add_products_from_csv(r'C:\Users\Virendra\PycharmProjects\flaskPBL\app\flipkart_smartwatches.csv')