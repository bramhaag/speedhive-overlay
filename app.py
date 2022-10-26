from flask import Flask, render_template

app = Flask(__name__, 
    static_url_path='',
    static_folder='static',
    template_folder='template')

@app.route("/standings")
def hello_world():
    return render_template('standings.html')
