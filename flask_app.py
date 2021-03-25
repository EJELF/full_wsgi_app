from flask import Flask, render_template, request

application = Flask(__name__)


@application.route("/")
def index():
    return render_template("index.html")


@application.route("/university/", methods=["GET", "POST"])
def university():
    if request.method == "GET":
        return render_template("university.html")
    else:
        name = request.form["full_name"]
        math = request.form["mathematic"]
        latv = request.form["latvian_language"]
        foreign = request.form["foreign_language"]
        if int(math) >= 40 and int(latv) >= 40 and int(foreign) >= 40:
            result = name + " var iesniegt dokumentus augstskolā"
        else:
            result = name + " nevar sniegt dokumentus augstskolā, jo nav nepieciešamais punktu skaits"

        return result


application.run(host="localhost", port=5000, debug=True)

