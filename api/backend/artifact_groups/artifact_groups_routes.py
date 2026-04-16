from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import get_db
from backend.db_connection import getDBQuery
from mysql.connector import Error

artifact_groups = Blueprint("artifact_groups", __name__)

# GET /artifact_groups
@artifact_groups.route("/", methods=["GET"])
def get_all_groups():
    return getDBQuery("SELECT * FROM ArtifactSet", "GET /artifact_groups")

@artifact_groups.route("/<int:groupID>", methods=["GET"])
def get_group_by_id(groupID):
    # Using an f-string because the original getDBQuery only accepts two strings
    return getDBQuery(
        f"SELECT * FROM ArtifactSet WHERE artifactSetID = {groupID}", 
        f"GET /artifact_groups/{groupID}"
    )

# GET /artifact_groups/{id}/artifacts
@artifact_groups.route("/<int:groupID>/artifacts", methods=["GET"])
def get_artifacts_in_group(groupID):
    query = f"""
        SELECT a.* FROM Artifact a
        JOIN ArtifactSetRelations asr ON a.artifactID = asr.artifactID
        WHERE asr.artifactSetID = {groupID}
    """
    return getDBQuery(query, f"GET /artifact_groups/{groupID}/artifacts")

# POST /artifact_groups
@artifact_groups.route("/", methods=["POST"])
def create_group():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        if "name" not in data:
            return jsonify({"error": "Missing group name"}), 400

        query = "INSERT INTO ArtifactSet (artifactSetID, name, description) VALUES (%s, %s, %s)"
        cursor.execute(query, (data.get("artifactSetID"), data["name"], data.get("description")))
        get_db().commit()
        return jsonify({"message": "Artifact group created"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# PUT /artifact_groups/{id}
@artifact_groups.route("/<int:groupID>", methods=["PUT"])
def update_group(groupID):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        update_parts = []
        params = []

        if "name" in data:
            update_parts.append("name = %s")
            params.append(data["name"])
        if "description" in data:
            update_parts.append("description = %s")
            params.append(data["description"])

        if not update_parts:
            return jsonify({"error": "No fields to update"}), 400

        params.append(groupID)
        query = f"UPDATE ArtifactSet SET {', '.join(update_parts)} WHERE artifactSetID = %s"
        cursor.execute(query, params)
        get_db().commit()
        return jsonify({"message": "Artifact group updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# DELETE /artifact_groups/{id}
@artifact_groups.route("/<int:groupID>", methods=["DELETE"])
def delete_group(groupID):
    cursor = get_db().cursor(dictionary=True)
    try:
        # Note: Foreign key constraints in your schema will prevent deletion 
        # if artifacts are still linked to this group in ArtifactSetRelations.
        cursor.execute("DELETE FROM ArtifactSet WHERE artifactSetID = %s", (groupID,))
        get_db().commit()
        return jsonify({"message": "Artifact group deleted"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()