import datetime
import psycopg2


class Database:
    def __init__(self):
        self.con = psycopg2.connect(
            dbname="Online_store",
            user="postgres",
            password="pass",
            host="localhost",
            port=5432
        )
        self.cur = self.con.cursor()
        self.con.autocommit = True

    # ______________________________________USERS____________________________________________________________

    def create_table_user(self):
        self.cur.execute('CREATE TABLE users('
                         'id serial not null primary key,'
                         'name varchar(64) not null ,'
                         'password varchar(16) not null ,'
                         'email varchar(64) not null );')

    def add_user(self, user):
        self.cur.execute('INSERT INTO users VALUES(default, %s, %s, %s) RETURNING id',
                         (user['name'], user['password'], user['email']))
        return self.cur.fetchone()[0]

    def get_user(self, email, password):
        if not password:
            self.cur.execute('SELECT id FROM users WHERE email=%s', (email,))
        else:
            self.cur.execute('SELECT * FROM users WHERE email=%s AND password=%s', (email, password))
        line = self.cur.fetchone()
        return {'id': line[0], 'name': line[1], 'password': line[2], 'email': line[3]} if line else {}

    def edit_user(self, user_id, user):
        self.cur.execute('UPDATE users SET name=%s, password=%s, email=%s WHERE id = %s',
                         (user['name'], user['password'], user['email'], user_id))

    # ______________________________________PRODUCT____________________________________________________________

    def create_table_product(self):
        self.cur.execute('CREATE TABLE product('
                         'id serial not null primary key,'
                         'name varchar(128),'
                         'price float,'
                         'about varchar(2048));')

    def add_product(self, p):
        self.cur.execute('INSERT INTO product VALUES(default, %s, %s, %s, %s) RETURNING id',
                         (p['name'], p['price'], p['about'], p['category']))
        return self.cur.fetchone()[0]

    def get_product(self, product_id=None):
        self.cur.execute('SELECT * FROM product ORDER BY id')
        products = []
        for line in self.cur.fetchall():
            products.append({'id': line[0], 'name': line[1], 'price': line[2], 'about': line[3], 'category': line[4]})
            if line[0] == product_id:
                return products[-1]
        return products

    def edit_product(self, product_id, product):
        self.cur.execute('UPDATE product SET name=%s, price=%s, category=%s, about=%s WHERE id = %s',
                         (product['name'], product['price'], product['category'], product['about'], product_id))

    def delete_product(self, product_id):
        self.cur.execute('DELETE FROM product WHERE id = %s', (product_id,))

    # ______________________________________LIKES_BASKETS_ORDERS____________________________________________________________
    def add_to_favourites(self, user_id, product_id):
        self.cur.execute('INSERT INTO favourites VALUES(%s, %s)', (user_id, product_id))

    def get_from_favourites(self, user_id):
        self.cur.execute('SELECT * FROM favourites WHERE user_id=%s', (user_id,))
        return [e[1] for e in self.cur.fetchall()]

    def delete_from_favourites(self, user_id, product_id):
        self.cur.execute('DELETE FROM favourites WHERE user_id=%s AND product_id=%s', (user_id, product_id))

    def add_to_basket(self, user_id, product_id):
        self.cur.execute('INSERT INTO basket VALUES(%s, %s)', (user_id, product_id))

    def get_from_basket(self, user_id):
        self.cur.execute('SELECT * FROM basket WHERE user_id=%s', (user_id,))
        return [e[1] for e in self.cur.fetchall()]

    def delete_from_basket(self, user_id, product_id):
        self.cur.execute('DELETE FROM basket WHERE user_id=%s AND product_id=%s', (user_id, product_id))

    def make_order(self, user_id, products_id):
        price = sum([self.get_product(product_id)['price'] for product_id in products_id])
        date = datetime.datetime.now().strftime("%m.%d.%Y, %H:%M")
        self.cur.execute('INSERT INTO orders VALUES(default, %s, %s, %s) RETURNING order_id', (user_id, price, date))
        order_id = self.cur.fetchone()[0]
        for product_id in products_id:
            self.cur.execute('INSERT INTO order_products VALUES(%s, %s)', (order_id, product_id))

    def get_orders_id(self, user_id):
        self.cur.execute('SELECT order_id FROM orders WHERE user_id=%s', (user_id,))
        return self.cur.fetchall()

    def get_order(self, order_id):
        self.cur.execute('SELECT * FROM orders WHERE order_id=%s', (order_id,))
        line = self.cur.fetchone()
        order = {'order_id': line[0], 'user_id': line[1], 'price': line[2], 'date': line[3]}
        self.cur.execute('SELECT product_id FROM order_products WHERE order_id=%s', (order_id,))
        order['products'] = [self.get_product(line[0]) for line in self.cur.fetchall()]
        return order
