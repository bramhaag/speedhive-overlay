import json

from flask import Flask, render_template

from scraper import Scraper

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='template')

scraper = Scraper()


@app.route("/standings")
def hello_world():
    return render_template('standings.html')


@app.route("/results")
def get_results():
    return scraper.get_results()
