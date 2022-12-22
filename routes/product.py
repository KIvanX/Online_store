from config import *


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
        print(request.files)
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
