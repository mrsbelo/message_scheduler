from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from .logs import get_logger

logger = get_logger(__name__)
app = Flask(__name__)
app.config.from_object("app.config.Config")
db = SQLAlchemy(app)


@app.route("/healthcheck")
def hello_world():
    logger.info("healthcheck")
    return jsonify({"status": "ok"})
