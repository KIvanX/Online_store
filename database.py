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
        self.cur.execute('INSERT INTO product VALUES(default, %s, %s, %s) RETURNING id',
                         (p['name'], p['price'], p['about']))
        return self.cur.fetchone()[0]

    def get_product(self, product_id=None):
        self.cur.execute('SELECT * FROM product ORDER BY id')
        products = []
        for line in self.cur.fetchall():
            products.append({'id': line[0], 'name': line[1], 'price': line[2], 'about': line[3]})
            if line[0] == product_id:
                return products[-1]
        return products

    def edit_product(self, product_id, product):
        self.cur.execute('UPDATE product SET name=%s, price=%s, about=%s WHERE id = %s',
                         (product['name'], product['price'], product['about'], product_id))

    def delete_product(self, product_id):
        self.cur.execute('DELETE FROM product WHERE id = %s', (product_id,))
