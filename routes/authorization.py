from config import *


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
