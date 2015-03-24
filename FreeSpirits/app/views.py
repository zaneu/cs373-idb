from app import app
from flask import Flask, render_template

@app.route('/')
@app.route('/index')
def index():
  return render_template("index.html")


@app.route('/builder')
@app.route('/builer.html')
def builder():
  return render_template("builder.html")

