from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import get_db
from backend.db_connection import getDBQuery


artifacts = Blueprint("artifacts", __name__)

@artifacts.route("/artifacts", methods=["GET"])
def get_all_artifacts():
    getDBQuery("SELECT * FROM Artifact", 'GET /artifacts')

@artifacts.route("/artifacts/<int:artifact_id>")
def get_artifact(artifact_id):
    getDBQuery("SELECT * FROM Artifact WHERE artifactID = " + str(artifact_id), 'GET /artifacts<int:artifact_id>')

@artifacts.route("/artifacts/<int:artifact_id>/artifact_group")
def get_artifact_group(artifact_id):
    getDBQuery(
        "SELECT * FROM ArtifactSet WHERE artifactSetID in (SELECT a.artifactSetID FROM ArtifactSet AS a JOIN ArtifactSetRelations AS asr ON a.artifactSetID = asr.artifactSetIDWHERE artifactID = " + str(artifact_id) + ");",
        'GET /artifacts/<int:artifact_id>/artifact_group'\
    )

@artifacts.route("/artifacts/<int:artifact_id>/artifact_group")
def get_artifact_gallery(artifact_id):
    getDBQuery(
        "SELECT * FROM Galleries WHERE galleryID in (SELECT galleryID from Artifact JOIN Exhibits ON exhibitID = displayedInExhibitID WHERE artifactID = 3000039) AND branchID in (SELECT Exhibits.branchID from Artifact JOIN Exhibits ON exhibitID = displayedInExhibitID WHERE artifactID =" + str(artifact_id) + ");",
        "GET /artifacts/<int:artifact_id>/artifact_group"
    )

@artifacts.route("/artifacts/<int:artifact_id>/artist")
def get_artifact_artist(artifact_id):
    getDBQuery(
        "SELECT * from Artist WHERE artistID = (SELECT artistID FROM Artifact WHERE artifactID = "+ artifact_id + ");",
        "GET /artifacts/<int:artifact_id>/artist"
        )
    
@artifacts.route("/artifacts/<int:artifact_id>/archived-by")
def get_artifact_artist(artifact_id):
    getDBQuery(
        "SELECT * from MuseumWorker WHERE employeeID = (SELECT archivedByEmployeeID FROM Artifact WHERE artifactID ="+ artifact_id + ");",
        "GET /artifacts/<int:artifact_id>/archived-by"
        )
    
@artifacts.route("/artifacts/<int:artifact_id>/exhibit")
def get_artifact_artist(artifact_id):
    getDBQuery(
        "SELECT * from Exhibits WHERE exhibitID = (SELECT displayedInExhibitID FROM Artifact WHERE artifactID ="+ artifact_id + ");",
        "GET /artifacts/<int:artifact_id>/archived-by"
        )
#PUT /artifacts

#DELETE /artifacts