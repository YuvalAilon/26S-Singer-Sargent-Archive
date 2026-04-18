from flask import Blueprint, request, jsonify
from backend.db_connection import get_db
from backend.db_connection import getDBQuery
from mysql.connector import Error

projects = Blueprint("projects", __name__)

# GET /projects
@projects.route("/", methods=["GET"])
def get_all_projects():
    return getDBQuery("SELECT * FROM ExpansionProject", "GET /projects")

# POST /projects
@projects.route("/", methods=["POST"])
def create_project():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        required = ["projectID", "headedByBranchID", "status"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        query = """
            INSERT INTO ExpansionProject 
            (projectID, headedByBranchID, description, status, costDollarAmount, 
             contactFirstName, contactMiddleName, contactLastName, contactPhone, contactEmail)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data["projectID"], data["headedByBranchID"], data.get("description"),
            data["status"], data.get("costDollarAmount"), data.get("contactFirstName"),
            data.get("contactMiddleName"), data.get("contactLastName"),
            data.get("contactPhone"), data.get("contactEmail")
        )
        cursor.execute(query, params)
        get_db().commit()
        return jsonify({"message": "Project created", "projectID": data["projectID"]}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# GET /projects/{id}
@projects.route("/<int:projectID>", methods=["GET"])
def get_project_by_id(projectID):
    return getDBQuery(
        f"SELECT * FROM ExpansionProject WHERE projectID = {projectID}", 
        f"GET /projects/{projectID}"
    )

# PUT /projects/{id}
@projects.route("/<int:projectID>", methods=["PUT"])
def update_project(projectID):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        fields = [
            "headedByBranchID", "description", "status", "costDollarAmount",
            "contactFirstName", "contactMiddleName", "contactLastName", 
            "contactPhone", "contactEmail"
        ]
        
        update_parts = [f"{f} = %s" for f in fields if f in data]
        params = [data[f] for f in fields if f in data]
        
        if not update_parts:
            return jsonify({"error": "No fields to update"}), 400
            
        params.append(projectID)
        query = f"UPDATE ExpansionProject SET {', '.join(update_parts)} WHERE projectID = %s"
        cursor.execute(query, params)
        get_db().commit()
        return jsonify({"message": "Project updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# GET /projects/by-branch/{branch-id}
@projects.route("/by-branch/<int:branchID>", methods=["GET"])
def get_projects_by_branch(branchID):
    return getDBQuery(
        f"SELECT * FROM ExpansionProject WHERE headedByBranchID = {branchID}", 
        f"GET /projects/by-branch/{branchID}"
    )