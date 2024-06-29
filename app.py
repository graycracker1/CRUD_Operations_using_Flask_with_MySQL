from flask import Flask, jsonify, request, abort
import mysql.connector

app = Flask(__name__)

# database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'test_db'
}

# mysql connection
conn = mysql.connector.connect(**db_config)

# create product table if not exists
create_products_table_query = """
create table if not exists products (
    id int auto_increment primary key,
    name varchar(255) not null,
    description text not null,
    price decimal(10, 2) not null,
    image_url varchar(255) not null
)
"""
cursor = conn.cursor()
cursor.execute(create_products_table_query)
cursor.close()

# create cart_items table if not exists
create_cart_items_table_query = """
create table if not exists cart_items (
    id int auto_increment primary key,
    product_id int not null,
    quantity int not null,
    foreign key (product_id) references products(id)
)
"""
cursor = conn.cursor()
cursor.execute(create_cart_items_table_query)
cursor.close()

# all routes

# fetch all products
@app.route('/products', methods=['GET'])
def get_products():
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from products")
    products = cursor.fetchall()
    cursor.close()
    return jsonify(products)

# fetch product with given id
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from products where id = %s", (id,))
    product = cursor.fetchone()
    cursor.close()
    if not product:
        abort(404, 'product not found.')
    return jsonify(product)

# add products into table
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    image_url = data.get('image_url')

    if not name or not description or not price or not image_url:
        abort(400, 'Missing fields in request.')

    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, description, price, image_url) VALUES (%s, %s, %s, %s)", 
                   (name, description, price, image_url))
    conn.commit()
    cursor.close()

    return jsonify({'message': 'Product added successfully.'}), 201

# fetch from cart
@app.route('/cart', methods=['GET'])
def get_cart():
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from cart_items")
    cart_items = cursor.fetchall()
    cursor.close()
    return jsonify(cart_items)

# add into cart
@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not product_id or not quantity:
        abort(400, 'product id and quantity are required.')

    # Check if the item is already in the cart
    cursor = conn.cursor()
    cursor.execute("select id from cart_items where product_id = %s", (product_id,))
    existing_item = cursor.fetchone()
    cursor.close()

    if existing_item:
        abort(400, 'Product is already in the cart.')

    # check if the product exists in the products table(this is to make sure so that invalid data doesn't get inserted.)
    cursor = conn.cursor()
    cursor.execute("select id from products where id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()

    if not product:
        abort(404, 'product not found.')


    # Product exists, so insert into the cart_items table
    cursor = conn.cursor()
    cursor.execute("insert into cart_items (product_id, quantity) values (%s, %s)", (product_id, quantity))
    conn.commit()
    cursor.close()

    return jsonify({'message': 'product added to cart successfully.'}), 201

# delete from cart
@app.route('/cart/<int:id>', methods=['DELETE'])
def remove_from_cart(id):

    # check if the item exists in the cart
    cursor = conn.cursor()
    cursor.execute("select id from cart_items where id = %s", (id,))
    existing_item = cursor.fetchone()
    cursor.close()

    if not existing_item:
        abort(404, 'Item not found in the cart.')

    # delete the item from the cart_items table
    cursor = conn.cursor()
    cursor.execute("delete from cart_items where id = %s", (id,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Item removed from cart successfully.'})

if __name__ == '__main__':
    app.run(debug=True)
