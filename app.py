from flask import Flask, render_template, request

app = Flask(__name__)

#app looks for request flask
@app.route("/lda")
def lda():
    return render_template("lda.html")

@app.route("/tsne/")
def tsne():
    return render_template("temp-plot.html")
