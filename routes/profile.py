from config import *


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
