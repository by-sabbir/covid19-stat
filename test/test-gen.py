import numpy as np
from flask import Flask, Response

app = Flask(__name__)


def gen():
    itter = np.random.randint(97, 123)
    yield bytes(chr(itter), 'utf-8')


@app.route("/")
def index():
    c = Response(gen())
    return c.get_data().decode('utf-8')


if __name__ == "__main__":
    app.run(debug=True)
