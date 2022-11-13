from config import *


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