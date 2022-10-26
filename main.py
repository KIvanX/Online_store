
import json
from flask import Flask, render_template, request, redirect, make_response, session
from lesson4_5.db_util import Database

app = Flask(__name__)
app.secret_key = 'fbRf43sRe3R3ke'
db = Database()


@app.route("/something", methods=['POST', 'GET'])
def something():
    if request.method == 'POST':
        request.form.get('username')

    context = {
        'lesson': 'math',
        'person': {
            'name': 'Vasya',
            'age': 20
        }
    }

    return render_template("new.html", **context)


@app.route("/session")
def choose_session():
    num1 = int(session.get('num1') or '0')
    num2 = int(request.cookies.get("num2") or '0')

    resp = make_response(f'session: {num1 + 1} cookie: {num2 + 1}')

    session['num1'] = str(num1 + 1)
    resp.set_cookie("num2", str(num2 + 1))

    return resp


@app.route("/change_mode")
def add_cookie():
    resp = redirect("/")
    mode = request.cookies.get("Mode")
    if mode is None or mode == 'light':
        resp.set_cookie("Mode", "dark")
    else:
        resp.set_cookie("Mode", "light")
    return resp


@app.route("/")
@app.route("/films")
def films_list():
    theme = request.cookies.get("Mode") if request.cookies.get("Mode") is not None else 'light'
    country = request.args.get("country")
    min_rating = float(request.args.get("min_rating")) if "min_rating" in request.args else 0.0

    films = db.select(country=country, min_rating=min_rating)

    context = {
        'films': films,
        'title': "FILMS",
        'theme': theme,
    }

    return render_template("films.html", **context)


@app.route("/film/<int:film_id>")
def get_film(film_id):
    theme = request.cookies.get("Mode") if request.cookies.get("Mode") is not None else 'light'
    films = db.select(film_id=film_id)

    if films:
        return render_template("film.html", title=films[0]['name'], film=films[0], theme=theme)

    return render_template("error.html", error="Такого фильма не существует в системе", theme=theme)


@app.route("/new_film/")
def new_film():
    theme = request.cookies.get("Mode") if request.cookies.get("Mode") is not None else 'light'
    if request.args:
        new_film = {
            "id": len(db.select()),
            "name": request.args['name'],
            "rating": float(request.args['rating']),
            "country": str(request.args['country'])
        }

        db.insert(new_film)
        return redirect("/")

    return render_template("new_film.html", title="Добавить новый фильм", theme=theme)


if __name__ == "__main__":
    app.run(debug=True)