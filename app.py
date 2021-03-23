import flask

application = flask.Flask(__name__)


@application.route("/")
def index():
    return "Hello Edgars"

