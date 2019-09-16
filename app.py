from flask import Flask, render_template

app = Flask(__name__)

posts = [1,2,3,4,5]

#app looks for request flask
@app.route("/lda")
def lda():
    return render_template("lda.html")

@app.route("/tsne/")
def tsne():
    return render_template("tsne.html")

@app.route("/")
def recomender():
    return render_template('recommender.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
