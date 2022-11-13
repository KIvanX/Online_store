from config import *


@app.route("/favourites")
def favourites():
    products_id = db.get_from_favourites(session['OE_user']['id'])
    user_products = [p for p in db.get_product() if p['id'] in products_id]
    return render_template("favourites.html", user_products=user_products, user=session['OE_user'])


@app.route("/delete_from_favourites/<int:product_id>")
def delete_from_favourites(product_id):
    db.delete_from_favourites(session['OE_user']['id'], product_id)
    return redirect('/favourites')


@app.route("/add_to_favourites")
def add_to_favourites():
    if 'OE_user' not in session:
        return {'status': 'warning', 'message': 'Необходимо авторизоваться, чтобы добавить в Избранное этот товар'}
    if int(request.args['product_id']) in db.get_from_favourites(session['OE_user']['id']):
        return {'status': 'warning', 'message': 'Этот товар уже в Избранном'}

    db.add_to_favourites(session['OE_user']['id'], request.args['product_id'])
    return {'status': 'success', 'message': 'Добавлено в Избранное'}
