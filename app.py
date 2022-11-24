from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def start():
    return render_template("title.html")


@app.route("/enroll")
def subscribe():
    return render_template("subscribe.html")


@app.route("/unsubscribe")
def unsubscribe():
    return render_template("unsubscribe.html")


if __name__ == "__main__":
    app.run(debug=True)
