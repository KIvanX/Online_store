from config import *
from routes.order import *
from routes.index import *
from routes.basket import *
from routes.product import *
from routes.profile import *
from routes.favourites import *
from routes.registration import *
from routes.authorization import *


@app.errorhandler(Exception)
def handle_exception(error):
    return render_template("error.html", error=error)


if __name__ == "__main__":
    app.run(debug=False)
