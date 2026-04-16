from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import get_db
from mysql.connector import Error

artifacts = Blueprint("museum_workers", __name__)

#GET /museum_workers
@artifacts.route("/museum_workers", methods=["GET"])
def get_museum_workers():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /museum_workers")
        
        first_name = request.args.get("firstName")
        last_name = request.args.get("lastName")
        role_id = request.args.get("roleID")
        
        query = "SELECT * FROM museum_workers WHERE 1=1"
        params = []
        
        if first_name:
            query += " AND firstName = %s"
            params.append(first_name)
        if last_name:
            query += " AND lastName = %s"
            params.append(last_name)
        if role_id:
            query += " AND roleID = %s"
            params.append(role_id)

        cursor.execute(query, params)
        workers = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(workers)} museum workers')
        return jsonify(workers), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_ngos: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

#POST /museum_workers
@artifacts.route("/museum_workers", methods=["POST"])
def create_museum_worker():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO museum_workers (firstName, middleName, lastName, email, roleID) VALUES (%s, %s, %s, %s, %s)",
        (data["firstName"], )
        )
    rows = cursor.fetchall()
    db.commit()
    return jsonify(rows), 201

#PUT /museum_workers
@artifacts.route("/museum_workers", methods=["PUT"])
def get_museum_workers():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("")
    rows = cursor.fetchall()
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({"error": "Not found"}), 404
    return jsonify(rows), 200

#DELETE /museum_workers
@artifacts.route("/museum_workers", methods=["DELETE"])
def get_museum_workers():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("")
    rows = cursor.fetchall()
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({"error": "Not found"}), 404
    return jsonify(rows), 200