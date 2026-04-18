from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import get_db
from mysql.connector import Error

galleries = Blueprint("galleries", __name__)

#GET all galleries
@galleries.route("/", methods=["GET"])
def get_all_galleries():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /Galleries")
        
        branchID = request.args.get("branchID")
        wing = request.args.get("wing")
        name = request.args.get("name")
        is_in_use = request.args("isInUse")
        artwork_capacity = request.args("artworkCapacity")
        
        query = "SELECT * FROM Galleries WHERE 1=1"
        params = []
        
        if branchID:
            query += " AND branchID = %s"
            params.append(branchID)
        if wing:
            query += " AND wing = %s"
            params.append(wing)
        if name:
            query += " AND name = %s"
            params.append(name)
        if is_in_use:
            query += " AND isInUse = %s"
            params.append(is_in_use)
        if artwork_capacity:
            query += " AND artworkCapacity = %s"
            params.append(artwork_capacity)

        cursor.execute(query, params)
        branches = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(branches)} galleries')
        return jsonify(branches), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_galleries: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()