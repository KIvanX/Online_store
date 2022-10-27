from flask import Flask, render_template, request, redirect, make_response, session
from database import Database

app = Flask(__name__)
app.secret_key = 'fbRf43sRg4e3R3ke'
db = Database()


@app.route("/")
def films_list():
    if not session.get('logged'):
        return redirect("/authorization/")

    print(request.args)


@app.route("/authorization/", methods=['POST', 'GET'])
def new_film():
    if request.method == 'POST':
        print(request.args)

    return render_template("authorization.html")


if __name__ == "__main__":
    app.run(debug=True)
