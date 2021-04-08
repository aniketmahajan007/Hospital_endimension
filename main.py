from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

from routes.routers import *


if __name__ == "__main__":
    app.run(debug=True)