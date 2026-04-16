from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import get_db
from mysql.connector import Error

museum_workers = Blueprint("museum_workers", __name__)

#GET /museum_workers
@museum_workers.route("/", methods=["GET"])
def get_all_museum_workers():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /museum_workers")
        
        first_name = request.args.get("firstName")
        last_name = request.args.get("lastName")
        role_id = request.args.get("roleID")
        
        query = "SELECT * FROM MuseumWorker WHERE 1=1"
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
        
# Get detailed information about a specific museum worker
@museum_workers.route("/<int:employeeID>", methods=["GET"])
def get_museum_worker(employeeID):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM MuseumWorker WHERE employeeID = %s", (employeeID,))
        museum_worker = cursor.fetchone()

        if not museum_worker:
            return jsonify({"error": "Museum worker not found"}), 404

        # Reuse the same cursor for the follow-up queries
        cursor.execute("SELECT * FROM Artifact WHERE archivedByEmployeeID = %s", (employeeID,))
        museum_worker["Artifact"] = cursor.fetchall()

        cursor.execute("SELECT * FROM Roles WHERE roleID = %s", (museum_worker["roleID"],))
        museum_worker["Roles"] = cursor.fetchall()

        return jsonify(museum_worker), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# POST /museum_workers
@museum_workers.route("/", methods=["POST"])
def create_museum_worker():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('POST /museum_workers')
        data = request.get_json()

        required_fields = ["firstName", "lastName", "email", "roleID"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        query = """
            INSERT INTO MuseumWorker (firstName, middleName, lastName, email, roleID)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (
            data["firstName"],
            data.get("middleName"),
            data["lastName"],
            data["email"],
            data["roleID"],
        ))
        
        get_db().commit()
        return jsonify({"message": "Museum worker created successfully", "employeeID": cursor.lastrowid}), 201
    except Error as e:
        current_app.logger.error(f'Database error in create_museum_worker: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# PUT /museum_workers/<museumWorkerID>
@museum_workers.route("/<int:employeeID>", methods=["PUT"])
def update_museum_worker(employeeID):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'PUT /museum_workers/{employeeID}')
        data = request.get_json()

        cursor.execute("SELECT employeeID FROM MuseumWorker WHERE employeeID = %s", (employeeID,))
        if not cursor.fetchone():
            return jsonify({"error": "Museum worker not found"}), 404

        allowed_fields = ["firstName", "middleName", "lastName", "email", "roleID"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(employeeID)
        query = f"UPDATE MuseumWorker SET {', '.join(update_fields)} WHERE employeeID = %s"
        cursor.execute(query, params)
        get_db().commit()

        return jsonify({"message": "Museum worker updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in update_museum_worker: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

#DELETE /museum_workers
@museum_workers.route("/<int:employeeID>", methods=["DELETE"])
def delete_museum_worker(employeeID):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'DELETE /museum_workers/{employeeID}')

        cursor.execute("SELECT employeeID FROM MuseumWorker WHERE employeeID = %s", (employeeID,))
        if not cursor.fetchone():
            return jsonify({"error": "Museum worker not found"}), 404

        cursor.execute("DELETE FROM MuseumWorker WHERE employeeID = %s", (employeeID,))
        get_db().commit()

        return jsonify({"message": "Museum worker deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in delete_museum_worker: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        
#GET all artifacts archived by a museum worker
@museum_workers.route("/<int:employeeID>/artifacts", methods=["GET"])
def get_museum_worker_artifacts(employeeID):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT employeeID FROM MuseumWorker WHERE employeeID = %s", (employeeID,))
        if not cursor.fetchone():
            return jsonify({"error": "Museum worker not found"}), 404

        cursor.execute("SELECT * FROM Artifact WHERE archivedByEmployeeID = %s", (employeeID,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()