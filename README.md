﻿# CRUD_Operations_using_Flask_with_MySQL

#You can test it using postman.

1. GET : Fetch all products (/products).
2. GET : Fetch product with specific id  (/products/1).
3. POST : Create a new product. ( /products ). Send data in JSON format like this { "name": "iphone", "price" : 500 }.

4. GET : Fetch from cart items (/cart).
5. POST : Add product to cart (/cart). Send data in JSON format like this { "product_id": "4", "quantity": "76"}.
6. DELETE : Delete product from cart with specific id (/cart/2).
