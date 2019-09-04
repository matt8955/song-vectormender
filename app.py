from flask import Flask, render_template, request

app = Flask(__name__)

#app looks for request flask
@app.route("/")
def index():
    return render_template("lda.html")
