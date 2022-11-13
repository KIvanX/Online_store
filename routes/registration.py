from config import *


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
