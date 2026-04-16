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
        
        query = "SELECT * FROM MuseumWorker WHERE 1=1"
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
        current_app.logger.error(f'Database error in get_all_ngos: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()