from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import get_db
from backend.db_connection import getDBQuery
from mysql.connector import Error


artifacts = Blueprint("artifacts", __name__)

@artifacts.route("", methods=["GET"])
def get_all_artifacts():
    # Added 'return' so the data actually goes to Chrome
    return getDBQuery("SELECT * FROM Artifact", 'GET /artifacts')

@artifacts.route("/<int:artifact_id>")
def get_artifact(artifact_id):
    return getDBQuery(f"SELECT * FROM Artifact WHERE artifactID = {artifact_id}", 'GET /artifacts/id')

@artifacts.route("/<int:artifact_id>/gallery")
def get_artifact_gallery(artifact_id):
    query = f"SELECT * FROM Galleries WHERE galleryID in (SELECT galleryID from Artifact JOIN Exhibits ON exhibitID = displayedInExhibitID WHERE artifactID = {artifact_id});"
    return getDBQuery(query, "GET /artifacts/id/gallery")

@artifacts.route("/<int:artifactID>/artifact_groups", methods=["GET"])
def get_artifact_groups(artifactID):
    query = """
            SELECT s.artifactSetID, s.name, s.description
            FROM ArtifactSet s
            JOIN ArtifactSetRelations r ON s.artifactSetID = r.artifactSetID
            WHERE r.artifactID = 
        """ + str(artifactID)
    return getDBQuery(query, "GET /artifacts/id/gallery")

@artifacts.route("/<int:artifact_id>/artist")
def get_artifact_artist(artifact_id): # Unique name
    query = f"SELECT * from Artist WHERE artistID = (SELECT artistID FROM Artifact WHERE artifactID = {artifact_id});"
    return getDBQuery(query, "GET /artifacts/id/artist")

@artifacts.route("/<int:artifact_id>/archived-by")
def get_artifact_worker(artifact_id): # Unique name
    query = f"SELECT * from MuseumWorker WHERE employeeID = (SELECT archivedByEmployeeID FROM Artifact WHERE artifactID = {artifact_id});"
    return getDBQuery(query, "GET /artifacts/id/archived-by")

@artifacts.route("/<int:artifact_id>/exhibit")
def get_artifact_exhibit(artifact_id): # Unique name
    query = f"SELECT * from Exhibits WHERE exhibitID = (SELECT displayedInExhibitID FROM Artifact WHERE artifactID = {artifact_id});"
    return getDBQuery(query, "GET /artifacts/id/exhibit")

@artifacts.route("/", methods=["POST"])
def create_artifact():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        required = ["artifactID", "name", "archivedByEmployeeID"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        query = """
            INSERT INTO Artifact (artifactID, artistID, name, description, imageURL, 
            artifactCondition, style, createdYear, medium, archivedByEmployeeID, displayedInExhibitID)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data["artifactID"], data.get("artistID"), data["name"], data.get("description"),
            data.get("imageURL"), data.get("artifactCondition"), data.get("style"),
            data.get("createdYear"), data.get("medium"), data["archivedByEmployeeID"],
            data.get("displayedInExhibitID")
        )
        cursor.execute(query, params)
        get_db().commit()
        return jsonify({"message": "Artifact created", "artifactID": data["artifactID"]}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE /artifacts/{id}
# Removes the artifact from the database entirely
@artifacts.route("/<int:artifactID>", methods=["DELETE"])
def delete_artifact(artifactID):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"DELETE /artifacts/{artifactID}")
        
        # Check if exists first
        cursor.execute("SELECT artifactID FROM Artifact WHERE artifactID = %s", (artifactID,))
        if not cursor.fetchone():
            return jsonify({"error": "Artifact not found"}), 404

        cursor.execute("DELETE FROM Artifact WHERE artifactID = %s", (artifactID,))
        get_db().commit()
        return jsonify({"message": f"Artifact {artifactID} deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# POST /artifacts/{id}/artifact_group
# Adds the artifact to a specific group
@artifacts.route("/<int:artifactID>/artifact_group", methods=["POST"])
def add_artifact_to_group(artifactID):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        group_id = data.get("artifactSetID")
        
        if not group_id:
            return jsonify({"error": "Missing artifactSetID"}), 400

        query = "INSERT INTO ArtifactSetRelations (artifactSetID, artifactID) VALUES (%s, %s)"
        cursor.execute(query, (group_id, artifactID))
        get_db().commit()
        
        return jsonify({"message": f"Artifact {artifactID} added to group {group_id}"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# DELETE /artifacts/{id}/artifact_group
# Removes the artifact from a specific group
@artifacts.route("/<int:artifactID>/artifact_group", methods=["DELETE"])
def remove_artifact_from_group(artifactID):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        group_id = data.get("artifactSetID")

        if not group_id:
            return jsonify({"error": "Missing artifactSetID"}), 400

        query = "DELETE FROM ArtifactSetRelations WHERE artifactID = %s AND artifactSetID = %s"
        cursor.execute(query, (artifactID, group_id))
        get_db().commit()
        
        return jsonify({"message": f"Artifact {artifactID} removed from group {group_id}"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        new_set_id = data.get("artifactSetID")
        
        if not new_set_id:
            return jsonify({"error": "Missing artifactSetID"}), 400

        # 1. Remove any existing group associations for this artifact
        cursor.execute("DELETE FROM ArtifactSetRelations WHERE artifactID = %s", (artifactID,))
        
        # 2. Add the new association
        query = "INSERT INTO ArtifactSetRelations (artifactSetID, artifactID) VALUES (%s, %s)"
        cursor.execute(query, (new_set_id, artifactID))
        
        get_db().commit()
        return jsonify({"message": f"Artifact {artifactID} moved to group {new_set_id}"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# PUT /artifacts/{id}
# This one handles Artist, Exhibit, and Archivist updates in one go 
# because they are all just columns in the Artifact table.
@artifacts.route("/<int:artifactID>", methods=["PUT"])
def update_artifact_general(artifactID):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        
        # Map of JSON keys to Database Columns
        field_map = {
            "artistID": "artistID",
            "exhibitID": "displayedInExhibitID",
            "employeeID": "archivedByEmployeeID",
            "name": "name",
            "condition": "artifactCondition"
        }

        update_parts = []
        params = []

        for json_key, db_col in field_map.items():
            if json_key in data:
                update_parts.append(f"{db_col} = %s")
                params.append(data[json_key])

        if not update_parts:
            return jsonify({"error": "No valid fields provided"}), 400

        params.append(artifactID)
        query = f"UPDATE Artifact SET {', '.join(update_parts)} WHERE artifactID = %s"
        
        cursor.execute(query, params)
        get_db().commit()
        
        return jsonify({"message": "Artifact updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()