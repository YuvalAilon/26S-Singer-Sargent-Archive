from flask import Blueprint, request, jsonify
from backend.db_connection import get_db
from backend.db_connection import getDBQuery
from mysql.connector import Error

requests = Blueprint("requests", __name__)

#GET /requests
@requests.route("", methods=["GET"])
def get_all_requests():
    return getDBQuery("SELECT * FROM ArtifactRequest", 'GET ')

@requests.route("/<int:request_id>", methods=["GET"])
def get_request_by_id(request_id):
    return getDBQuery("SELECT * FROM ArtifactRequest WHERE requestID = " + str(request_id) , 'GET /<int:artifact_id>')

@requests.route("/<int:requestID>/artifacts", methods=["GET"])
def get_artifacts_in_request(requestID):
    """
    Fetches all artifacts associated with a specific artifact request.
    """
    query = f"""
        SELECT a.* FROM Artifact a
        JOIN ArtifactRequestRelations arr ON a.artifactID = arr.artifactID
        WHERE arr.requestID = {requestID}
    """
    # Using your existing getDBQuery helper
    return getDBQuery(query, f"GET /requests/{requestID}/artifacts")

@requests.route("/future-returns", methods=["GET"])
def future_returns():
    return getDBQuery("SELECT * FROM ArtifactRequest WHERE loanDateEnd > CURDATE()", 'GET /future-returns')

@requests.route("/before/<string:before_date>", methods=["GET"])
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

#POST /requests

#PUT /requests
@requests.route("/<int:request_id>", methods=["PUT"])
def update_donor(request_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        cursor.execute("SELECT * FROM ArtifactRequest WHERE requestID = %s", (request_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Request not found"}), 404

        # Build update query dynamically based on provided fields
        allowed_fields = ["loanDateStart", "loanDateEnd", "status"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(request_id)
        query = f"UPDATE ArtifactRequest SET {', '.join(update_fields)} WHERE requestID = %s"
        cursor.execute(query, params)
        get_db().commit()

        return jsonify({"message": "Artifact request updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

#DELETE /requests
