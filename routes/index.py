from config import *


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
