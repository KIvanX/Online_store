from flask import Flask, render_template, request, redirect, make_response, session, flash
from database import Database
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'fbRf43sRg4e3R3ke'
db = Database()


@app.route("/")
def index():
    if 'OE_user' in session:
        return render_template("index.html", products=db.get_product(), user=session['OE_user'])
    else:
        return redirect("authorization")


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
        return redirect("/")

    return render_template("profile.html", user=session.get('OE_user'))


@app.route("/add_product", methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        product = {'name': request.form.get('name'),
                   'price': request.form.get('price'),
                   'about': request.form.get('about')}
        product_id = db.add_product(product)
        request.files.get('photo').save(f'static/product{product_id}.jpg')
        
        return redirect('/')

    return render_template("add_product.html")


@app.route("/edit_product/<int:product_id>", methods=['POST', 'GET'])
def edit_product(product_id):
    if request.method == 'POST':
        product = {'id': product_id,
                   'name': request.form.get('name'),
                   'price': request.form.get('price'),
                   'about': request.form.get('about')}
        db.edit_product(product_id, product)
        if request.files['photo']:
            request.files.get('photo').save(f'static/product{product_id}.jpg')

        return redirect('/')

    return render_template("edit_product.html", product=db.get_product(product_id=product_id))


@app.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    db.delete_product(product_id)
    return redirect('/')


@app.route("/buy_product/<int:product_id>", methods=['POST', 'GET'])
def buy_product(product_id):
    return render_template("edit_product.html", product=db.get_product(product_id=product_id))


@app.route("/like_product/<int:product_id>", methods=['POST', 'GET'])
def like_product(product_id):
    return render_template("edit_product.html", product=db.get_product(product_id=product_id))


if __name__ == "__main__":
    app.run(debug=True)
