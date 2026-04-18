from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import get_db
from mysql.connector import Error

branches = Blueprint("branches", __name__)

#GET all branches
@branches.route("/", methods=["GET"])
def get_all_branches():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /MuseumBranch")
        
        branch_name = request.args.get("branchName")
        contact_name = request.args.get("contactName")
        city = request.args.get("city")
        
        query = "SELECT * FROM MuseumBranch WHERE 1=1"
        params = []
        
        if branch_name:
            query += " AND branchName = %s"
            params.append(branch_name)
        if contact_name:
            query += " AND contactName = %s"
            params.append(contact_name)
        if city:
            query += " AND city = %s"
            params.append(city)

        cursor.execute(query, params)
        branches = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(branches)} museum branches')
        return jsonify(branches), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_branches: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        
# Get detailed information about a specific branch
@branches.route("/<int:branchID>", methods=["GET"])
def get_branch(branchID):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM MuseumBranch WHERE branchID = %s", (branchID))
        museum_branch = cursor.fetchone()

        if not museum_branch:
            return jsonify({"error": "Museum branch not found"}), 404

        # Reuse the same cursor for the follow-up queries
        cursor.execute("SELECT * FROM ExpansionProject WHERE projectID = %s", (branchID,))
        museum_branch["Artifact"] = cursor.fetchall()

        cursor.execute("SELECT * FROM Galleries WHERE branchID = %s", (branchID))
        museum_branch["Roles"] = cursor.fetchall()

        return jsonify(museum_branch), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        
# Get the exhibits being hosted at a branch
@branches.route("/<int:branchID>", methods=["GET"])
def get_branch_galleries(branchID):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM MuseumBranch WHERE branchID = %s", (branchID))
        museum_branch = cursor.fetchone()

        if not museum_branch:
            return jsonify({"error": "Museum branch not found"}), 404

        # Reuse the same cursor for the follow-up queries
        cursor.execute("SELECT * FROM Artifact WHERE archivedByEmployeeID = %s", (branchID,))
        museum_branch["Artifact"] = cursor.fetchall()

        cursor.execute("SELECT * FROM Roles WHERE roleID = %s", (museum_branch["roleID"],))
        museum_branch["Roles"] = cursor.fetchall()

        return jsonify(museum_branch), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()