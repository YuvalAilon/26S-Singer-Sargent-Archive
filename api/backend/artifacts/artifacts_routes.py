from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import get_db
from backend.db_connection import getDBQuery


artifacts = Blueprint("artifacts", __name__)

@artifacts.route("", methods=["GET"])
def get_all_artifacts():
    # Added 'return' so the data actually goes to Chrome
    return getDBQuery("SELECT * FROM Artifact", 'GET /artifacts')

@artifacts.route("/<int:artifact_id>")
def get_artifact(artifact_id):
    return getDBQuery(f"SELECT * FROM Artifact WHERE artifactID = {artifact_id}", 'GET /artifacts/id')

# Note the change to /gallery to avoid the conflict with /artifact_group
@artifacts.route("/<int:artifact_id>/gallery")
def get_artifact_gallery(artifact_id):
    query = f"SELECT * FROM Galleries WHERE galleryID in (SELECT galleryID from Artifact JOIN Exhibits ON exhibitID = displayedInExhibitID WHERE artifactID = {artifact_id});"
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