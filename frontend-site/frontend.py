from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<name>")
def second(name):
    return f"Hello 2nd page {name}"

if __name__ == "__main__":
    app.run()

