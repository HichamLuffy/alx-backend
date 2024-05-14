#!/usr/bin/env python3
"""Flask app"""
from flask import Flask
from flask import render_template as template


app = Flask(__name__)


@app.route("/")
def index():
    title = "Welcome to Holberton"
    return template("0-index.html", title=title)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
