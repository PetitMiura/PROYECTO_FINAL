from miCartera import app
from flask import render_template, request, redirect, flash, url_for

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/compra")
def compra():
    return render_template("compra.html")

@app.route("/status")
def status():
    return render_template("status.html")