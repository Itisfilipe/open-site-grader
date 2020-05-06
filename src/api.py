from flask import Flask, jsonify
from flask import request

from report import Report

app = Flask(__name__)


@app.route("/audit", methods=['POST'])
def hello():
    url = request.form['url']
    try:
        with Report('http://www.example.com') as report:
            report.generate_report()


    except:
        return 'fail'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
