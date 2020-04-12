from flask import Flask, jsonify

from utils import LightHouse

app = Flask(__name__)


@app.route("/")
def hello():
    try:
        with LightHouse('http://www.example.com') as lh:
            return jsonify(lh.read_report_file())
    except:
        return 'fail'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
