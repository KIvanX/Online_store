from flask import Flask, render_template, request, redirect, make_response, session, flash
from database import Database
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'fbRf43sRg4e3R3ke'
db = Database()


def index_by_filter(product_type=''):
    my_filter = {'min_price': int(request.form['min_price']) if request.form.get('min_price') else 0,
                 'max_price': int(request.form['max_price']) if request.form.get('max_price') else 0,
                 'find_word': request.form.get('find_word', ''),
                 'category': product_type}

    user = session['OE_user'] if 'OE_user' in session else {'id': 0, 'name': 'Гость', 'email': ''}
    return render_template("index.html", products=db.get_product(), user=user, filter=my_filter,
                           basket=db.get_from_basket(user['id']), favourites=db.get_from_favourites(user['id']))


@app.route("/", methods=['POST', 'GET'])
def index():
    return index_by_filter()


@app.route("/category/<string:product_type>", methods=['POST', 'GET'])
def category(product_type):
    return index_by_filter(product_type)


@app.route("/basket")
def basket():
    products_id = db.get_from_basket(session['OE_user']['id'])
    user_products = [p for p in db.get_product() if p['id'] in products_id]
    full_price = sum([p['price'] for p in user_products])
    return render_template("basket.html", user_products=user_products, user=session['OE_user'], full_price=full_price)


@app.route("/delete_from_basket/<int:product_id>")
def delete_from_basket(product_id):
    db.delete_from_basket(session['OE_user']['id'], product_id)
    return redirect('/basket')


@app.route("/favourites")
def favourites():
    products_id = db.get_from_favourites(session['OE_user']['id'])
    user_products = [p for p in db.get_product() if p['id'] in products_id]
    return render_template("favourites.html", user_products=user_products, user=session['OE_user'])


@app.route("/delete_from_favourites/<int:product_id>")
def delete_from_favourites(product_id):
    db.delete_from_favourites(session['OE_user']['id'], product_id)
    return redirect('/favourites')


@app.route("/authorization", methods=['POST', 'GET'])
def authorization():
    if request.method == 'POST':
        user = db.get_user(request.form['email'], request.form['password'])
        if user:
            session['OE_user'] = user
        return redirect("/")
    elif request.args:
        if not request.args['email']:
            return {'status': 'error', 'message': 'Введите email'}
        if not request.args['password']:
            return {'status': 'error', 'message': 'Ведите пароль'}

        user = db.get_user(request.args['email'], request.args['password'])
        return {'status': 'ok'} if user else {'status': 'error', 'message': 'Пользователь не найден'}
    return render_template("authorization.html")


@app.route("/registration", methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        user = {'name': request.form.get('name'),
                'password': request.form.get('password'),
                'email': request.form.get('email')}
        user['id'] = db.add_user(user)
        session['OE_user'] = user
        flash('Добро пожаловать на сайт OzonExpress')
        return redirect("/")
    elif request.args:
        if not request.args['name']:
            return {'status': 'error', 'message': 'Введите своё имя'}
        if not request.args['email'] or request.args['email'].count('@') != 1 or request.args['email'].count('.') != 1:
            return {'status': 'error', 'message': 'Некорректный email'}
        if db.get_user(request.args['email'], ''):
            return {'status': 'error', 'message': 'Пользователь с таким email уже существует'}
        if len(request.args['password']) < 6:
            return {'status': 'error', 'message': 'Пароль слишком короткий'}
        if request.args['password'] != request.args['password2']:
            return {'status': 'error', 'message': 'Пароли не совпадают'}
        if request.args['checkbox'] == 'false':
            return {'status': 'error', 'message': 'Необходимо принять правила сайта'}
        return {'status': 'ok'}
    return render_template("registration.html")


@app.route("/profile", methods=['POST', 'GET'])
def profile():
    if request.method == 'POST':
        user = {'id': session['OE_user']['id'],
                'name': request.form.get('name'),
                'password': request.form.get('password'),
                'email': request.form.get('email')}
        db.edit_user(session['OE_user']['id'], user)
        session['OE_user'] = user
        flash('Профиль изменен')
        return redirect("/")

    orders = [db.get_order(order_id) for order_id in db.get_orders_id(session['OE_user']['id'])]
    return render_template("profile.html", user=session.get('OE_user'), orders=orders)


@app.route("/product/<int:product_id>")
def product(product_id):
    return render_template('product.html', user=session.get('OE_user'), product=db.get_product(product_id))


@app.route("/add_product", methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        product = {'name': request.form.get('name'),
                   'price': request.form.get('price'),
                   'category': request.form.get('category'),
                   'about': request.form.get('about')}
        product_id = db.add_product(product)
        request.files.get('photo').save(f'static/product{product_id}.jpg')

        flash('Товар добавлен')
        return redirect('/')

    return render_template("add_product.html")


@app.route("/edit_product/<int:product_id>", methods=['POST', 'GET'])
def edit_product(product_id):
    global message
    if request.method == 'POST':
        product = {'id': product_id,
                   'name': request.form.get('name'),
                   'price': request.form.get('price'),
                   'category': request.form.get('category'),
                   'about': request.form.get('about')}
        db.edit_product(product_id, product)
        if request.files['photo']:
            request.files.get('photo').save(f'static/product{product_id}.jpg')

        flash('Товар успешно изменен')
        return redirect('/')

    return render_template("edit_product.html", product=db.get_product(product_id=product_id))


@app.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    db.delete_product(product_id)
    flash('Товар удален')
    return redirect('/')


@app.route("/add_to_basket")
def add_to_basket():
    if 'OE_user' not in session:
        return {'status': 'warning', 'message': 'Необходимо авторизоваться, чтобы купить этот товар'}
    if int(request.args['product_id']) in db.get_from_basket(session['OE_user']['id']):
        return {'status': 'warning', 'message': 'Этот товар уже в корзине'}

    db.add_to_basket(session['OE_user']['id'], request.args['product_id'])
    return {'status': 'success', 'message': 'Добавлено в корзину'}


@app.route("/add_to_favourites")
def add_to_favourites():
    if 'OE_user' not in session:
        return {'status': 'warning', 'message': 'Необходимо авторизоваться, чтобы добавить в Избранное этот товар'}
    if int(request.args['product_id']) in db.get_from_favourites(session['OE_user']['id']):
        return {'status': 'warning', 'message': 'Этот товар уже в Избранном'}

    db.add_to_favourites(session['OE_user']['id'], request.args['product_id'])
    return {'status': 'success', 'message': 'Добавлено в Избранное'}


@app.route("/make_order")
def make_order():
    products_id = db.get_from_basket(session['OE_user']['id'])
    db.make_order(session['OE_user']['id'], products_id)
    for product_id in products_id:
        db.delete_from_basket(session['OE_user']['id'], product_id)
    flash('Заказ принят')
    return redirect('/')


@app.route("/order/<int:order_id>")
def order(order_id):
    order_data = db.get_order(order_id)
    return render_template("order.html", user=session['OE_user'], order=order_data)


# @app.errorhandler(Exception)
# def handle_exception(error):
#     return render_template("error.html", error=error)


if __name__ == "__main__":
    app.run(debug=True)
