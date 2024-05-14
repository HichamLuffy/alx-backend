#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    """Index route"""
    title = "Welcome to Holberton"
    return render_template("0-index.html", title=title)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
