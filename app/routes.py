from flask import Flask

def setup_routes(app: Flask):
    @app.route("/")
    def index():
        return "Welcome to the Mini Strategy Analysis Project!"
