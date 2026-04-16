from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import get_db
from backend.db_connection import getDBQuery


artifacts = Blueprint("artifacts", __name__)

@artifacts.route("/artifacts", methods=["GET"])
def get_all_artifacts():
    getDBQuery("SELECT * FROM Artifact", 'GET /artifacts')

#PUT /artifacts

#DELETE /artifacts