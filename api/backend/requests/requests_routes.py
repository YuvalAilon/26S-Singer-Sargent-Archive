from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import get_db
from backend.db_connection import getDBQuery

requests = Blueprint("requests", __name__)

@requests.route("/<int:artifact_id>", methods=["GET"])
def get_all_requests(artifact_id):
    return getDBQuery("SELECT * FROM ArtifactRequest WHERE requestID = " + str(artifact_id) , 'GET /<int:artifact_id>')

@requests.route("/future-returns", methods=["GET"])
def future_returns():
    return getDBQuery("SELECT * FROM ArtifactRequest WHERE loanDateEnd > CURDATE()", 'GET /future-returns')

@requests.route("/<str:before_date>", methods=["GET"])
def future_returns_before(before_date):
    return getDBQuery(
        "SELECT * FROM ArtifactRequest WHERE loanDateEnd <= " + before_date,
        "GET /<str:before_date>"
        )

@requests.route("/by-exhibit/<int:exhibit_id>", methods=["GET"])
def get_by_exhibit(exhibit_id):
    return getDBQuery(
        "SELECT * FROM ArtifactRequest WHERE exhibitID = " + str(exhibit_id),
        "GET /by-exhibit/<int:exhibit_id>"
    )


#GET /requests

#POST /requests

#PUT /requests

#DELETE /requests