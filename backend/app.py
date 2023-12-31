from ariadne import graphql_sync
#from ariadne.constants import PLAYGROUND_HTML
import datetime as dt
from flask import Flask, request, jsonify, render_template, send_from_directory
from loguru import logger
import os
from typing import List, Dict, Tuple

# internal imports
from backend.extensions import db, migrate
from backend.resolvers import schema


def create_app(config_object="backend.settings") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_routes(app)
    return app


def register_extensions(app) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    import backend.models


def register_routes(app) -> None:
    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")

    #@app.route("/graphql", methods=["GET"])
    #def graphql_playground():
    #    return PLAYGROUND_HTML, 200

    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()
        success, result = graphql_sync(
            schema, data, context_value=request, debug=app.debug
        )
        status_code = 200 if success else 400
        return jsonify(result), status_code

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def cathall(path):
        return render_template("index.html")
