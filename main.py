from wsgiref import simple_server
import string
from urllib.parse import parse_qs


def load_template(name):
    with open(name, "r") as template:
        source = string.Template(template.read())
        return source


class Request:
    def __init__(self, path, data, method):
        self.path = path
        self.data = data
        self.method = method


def read_request_body(environment):
    try:
        request_body_size = int(environment.get("CONTENT_LENGTH", 0))
    except ValueError:
        request_body_size = 0
    request_body = environment["wsgi.input"].read(request_body_size)
    return request_body.decode()


def parse_request_body(request_body):
    parsed = parse_qs(request_body)
    return dict(parsed)


def load_requests(environment):
    request_body = read_request_body(environment=environment)
    parsed_body = parse_request_body(request_body=request_body)
    request = Request(
        path=environment["PATH_INFO"],
        data=parsed_body,
        method=environment["REQUEST_METHOD"]
    )
    return request


class Application:
    def __init__(self, routes):
        self.routes = routes
        self.request = None

    def __call__(self, environment, start_response):
        status = "200 OK"
        headers = [(
            "Content-type", "text/html"
        )]
        request = load_requests(environment=environment)
        handler = self.routes[request.path]
        start_response(status, headers)
        return handler(request=request)


def index(request):
    response = load_template("Templates/index.html")
    return [response.substitute().encode()]


def university(request):
    if request.method == "GET":
        response = load_template("Templates/university.html")
        return [response.substitute().encode()]
    elif request.method == "POST":
        name = request.data["full_name"][0]
        mathematic = int(request.data["mathematic"][0])
        latvian_language = int(request.data["latvian_language"][0])
        foreign_language = int(request.data["foreign_language"][0])

        if mathematic >= 40 and latvian_language >= 40 and foreign_language >= 40:
            result = name + " var pieteikties augstskolā"
        else:
            result = name + " nevar pieteikties augstskolā"

        response = load_template("Templates/university_response.html")

        return [response.substitute({"result": result}).encode()]


routes = {
    "/": index,
    "/university": university,
    "/favicon.ico": None
}

application = Application(routes=routes)

HOST = "127.0.0.1"
PORT = 5000

with simple_server.make_server(
        host=HOST,
        port=PORT,
        app=application) as server:
    print(f"Server {HOST} run on port:{PORT}")

    server.serve_forever()
