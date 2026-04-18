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
        cursor.execute("SELECT * FROM MuseumBranch WHERE branchID = %s", (branchID,))
        museum_branch = cursor.fetchone()

        if not museum_branch:
            return jsonify({"error": "Museum branch not found"}), 404

        cursor.execute("SELECT * FROM ExpansionProject WHERE headedByBranchID = %s", (branchID,))
        museum_branch["ExpansionProject"] = cursor.fetchall()

        cursor.execute("SELECT * FROM Galleries WHERE branchID = %s", (branchID,))
        museum_branch["Galleries"] = cursor.fetchall()

        return jsonify(museum_branch), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        
# POST /branches
@branches.route("/", methods=["POST"])
def create_branch():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('POST /branches')
        data = request.get_json()

        required_fields = ["branchName", "contactName", "contactPhone", "contactEmail", "street", "city", "state", "zip"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        query = """
            INSERT INTO MuseumBranch (branchName, contactName, contactPhone, contactEmail, street, city, state, zip)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (
            data["branchName"],
            data["contactName"],
            data["contactPhone"],
            data["contactEmail"],
            data["street"],
            data["city"],
            data["state"],
            data["zip"]
        ))
        
        get_db().commit()
        return jsonify({"message": "Branch created successfully", "branchID": cursor.lastrowid}), 201
    except Error as e:
        current_app.logger.error(f'Database error in create_branch: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        
# PUT /branches/<branchID>
@branches.route("/<int:branchID>", methods=["PUT"])
def update_branch(branchID):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'PUT /branches/{branchID}')
        data = request.get_json()

        cursor.execute("SELECT branchID FROM MuseumBranch WHERE branchID = %s", (branchID,))
        if not cursor.fetchone():
            return jsonify({"error": "Branch not found"}), 404

        allowed_fields = ["branchName", "contactName", "contactPhone", "contactEmail", "street", "city", "state", "zip"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(branchID)
        query = f"UPDATE MuseumBranch SET {', '.join(update_fields)} WHERE branchID = %s"
        cursor.execute(query, params)
        get_db().commit()

        return jsonify({"message": "Branch updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in update_branch: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        
#DELETE /branches
@branches.route("/<int:branchID>", methods=["DELETE"])
def delete_branch(branchID):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'DELETE /branch/{branchID}')

        cursor.execute("SELECT branchID FROM MuseumBranch WHERE branchID = %s", (branchID,))
        if not cursor.fetchone():
            return jsonify({"error": "Branch not found"}), 404

        cursor.execute("DELETE FROM MuseumBranch WHERE branchID = %s", (branchID,))
        get_db().commit()

        return jsonify({"message": "Branch deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in delete_branch: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()       

# Get the exhibits being hosted at a branch
@branches.route("/<int:branchID>/exhibits", methods=["GET"])
def get_branch_exhibits(branchID):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM MuseumBranch WHERE branchID = %s", (branchID,))
        museum_branch = cursor.fetchone()

        if not museum_branch:
            return jsonify({"error": "Museum branch not found"}), 404

        # Reuse the same cursor for the follow-up queries
        cursor.execute("SELECT * FROM Galleries WHERE branchID = %s", (branchID,))
        galleries = cursor.fetchall()

        for gallery in galleries:
            cursor.execute("SELECT * FROM Exhibits WHERE galleryID = %s", (gallery["galleryID"],))
            gallery["exhibits"] = cursor.fetchall()

        museum_branch["galleries"] = galleries
        return jsonify(museum_branch), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()