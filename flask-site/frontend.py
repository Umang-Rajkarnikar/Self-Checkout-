from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello main page"

@app.route("/<name>")
def second(name):
    return f"Hello 2nd page {name}"

if __name__ == "__main__":
    app.run()

