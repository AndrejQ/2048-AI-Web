import os
from json import dumps, loads

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler

from game_solver import estimate_directions_win_probabilities


class ManualSocketHandler(WebSocketHandler):
    def check_origin(self, origin):
        print("check origin")
        return True

    def open(self):
        print('open socket')

    def write_message(self, *args, **kwargs):
        print("send server msg")
        super().write_message("catch server msg")

    def on_message(self, message):
        message = loads(message)
        grid = message['grid']['cells']
        score = message['score']
        tiles = [[cell['value'] if cell else 0 for cell in row] for row in zip(*grid)]
        estimation = estimate_directions_win_probabilities(tiles, number_of_games=min(int(score / 20) + 1, 200))
        super().write_message(dumps({
            'values': estimation,
            'go to': max(estimation, key=estimation.get)
        }))

    def on_close(self):
        print('close')


class TestHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("game_frontend/index.html")


class JsHandler(RequestHandler):
    def get(self, *args, **kwargs):
        print("get:", self.request.uri)
        self.set_header("Content-Type", 'text/css; charset="utf-8"')
        self.render("game_frontend" + self.request.uri)


class CssHandler(RequestHandler):
    def get(self, *args, **kwargs):
        print("get:", self.request.uri)
        self.set_header("Content-Type", 'text/css; charset="utf-8"')
        self.render("game_frontend" + self.request.uri)


class FontHandler(RequestHandler):
    def get(self, *args, **kwargs):
        print("get:", self.request.uri)
        # need to fix this
        self.set_header("Content-Type", 'font/woff; charset="utf-8"')
        self.write("game_frontend" + self.request.uri)
        # self.finish()


if __name__ == '__main__':
    app = Application(handlers=[
        (r'/websocket', ManualSocketHandler),
        (r'/', TestHandler),
        (r'/(.*).js', JsHandler),
        (r'/(.*).css', CssHandler),
        (r'/(.*).woff', FontHandler)
    ])

    address = '0.0.0.0'
    # address = '192.168.99.100'  # for docker toolbox
    port = 8888  # port for localhost
    # port = os.environ['PORT']  # heroku port (use for deploying)
    app.listen(port=port, address=address)

    print('App inited on {}:{}'.format(address, port))

    IOLoop.current().start()
