import app
from wsgiref import simple_server

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app.app)
    print("Serving on http://127.0.0.1:8000")
    httpd.serve_forever()
