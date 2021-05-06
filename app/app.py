#!/usr/bin/env python3

# Flask
# pillow
# requests

from flask import (
    Flask,
    Blueprint,
    jsonify,
    request,
    send_file,
    send_from_directory,
    render_template,
)
from parrots import PARROTS, Parrot
import logging
import sys

API_PREFIX = "/api/v1"

app = Flask(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
app.logger.addHandler(handler)


# Web


@app.route("/")
def send_index():
    return render_template(
        "index.html",
        api_prefix=f"{request.url_root.rstrip('/')}{API_PREFIX}/parrots/",
        url_prefix=request.url_root,
    )


@app.route("/pyrrot.js")
def send_js():
    return render_template(
        "pyrrot.js",
        api_prefix=f"{request.url_root.rstrip('/')}{API_PREFIX}/parrots",
    )


@app.route("/<path:filename>")
def send_static(filename):
    return send_from_directory("static", filename)


@app.route("/favicon.ico")
def send_favicon():
    return send_file("static/images/left.gif", mimetype="image/gif")


# API

v1 = Blueprint("v1", "v1")


@v1.route("/", methods=["GET"])
def home():
    return "<h1>pyrrot</h1><p>API to generate Party Parrots.</p>"


@v1.route("/parrots", methods=["GET"])
def parrotlist():
    return jsonify(list(PARROTS.keys()))


@v1.route("/parrots/<string:name>", methods=["GET", "POST"])
def parrot(name):
    params = request.args

    if name not in PARROTS:
        return "Parrot flew away.", 404
    else:
        p = Parrot(name, **params)
        img = p.create_image()
        return send_file(img, mimetype="image/gif")


if __name__ == "__main__":
    app.register_blueprint(v1, url_prefix=API_PREFIX)
    app.run(host="0.0.0.0", debug=True)
