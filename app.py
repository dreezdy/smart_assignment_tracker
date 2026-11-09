from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# Member 2 (assignment routes) and Member 5 (AI chat) here.


if __name__ == "__main__":
    app.run(debug=True)