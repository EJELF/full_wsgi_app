from wsgiref import simple_server
import string


def load_template(name):
    with open(name, "r") as template:
        source = string.Template(template.read())
        return source


class Request:
    def __init__(self, path, data):
        self.path = path
        self.data = data


def load_requests(environment):
    request = Request(
        path=environment["PATH_INFO"],
        data={},
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
        return handler()


def index():
    response = load_template("index.html")
    return [response.substitute().encode()]


routes = {
    "/": index,
}

application = Application(routes=routes)

HOST = "127.0.0.1"
PORT = 8000

with simple_server.make_server(
        host=HOST,
        port=PORT,
        app=application) as server:
    print(f"Server {HOST} run on port:{PORT}")

    server.serve_forever()
