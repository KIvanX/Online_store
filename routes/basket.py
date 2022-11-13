from config import *


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


@app.route("/add_to_basket")
def add_to_basket():
    if 'OE_user' not in session:
        return {'status': 'warning', 'message': 'Необходимо авторизоваться, чтобы купить этот товар'}
    if int(request.args['product_id']) in db.get_from_basket(session['OE_user']['id']):
        return {'status': 'warning', 'message': 'Этот товар уже в корзине'}

    db.add_to_basket(session['OE_user']['id'], request.args['product_id'])
    return {'status': 'success', 'message': 'Добавлено в корзину'}
