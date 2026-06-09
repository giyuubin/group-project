from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

from predictor import predict

app=Flask(__name__)

@app.route("/")

def home():

    return render_template(
        "index.html"
    )


@app.route(
"/upload",
methods=["POST"]
)

def upload():

    file=request.files["file"]

    result=predict(file.read())

    return jsonify(result)


if __name__=="__main__":

    from wsgiref.simple_server import make_server
    print(" * Running on http://127.0.0.1:5000")
    make_server("127.0.0.1", 5000, app).serve_forever()