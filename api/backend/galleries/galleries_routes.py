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
        artwork_capacity = request.args.get("artworkCapacity")
        
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
        
#Get galleries not in use
@galleries.route("/", methods=["GET"])
def get_available_galleries():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /Galleries")
        
        cursor.execute("SELECT * FROM Galleries INNER JOIN Exhibits ON Exhibits.galleryID = Gallery.galleryID")
        
    except Error as e:
        current_app.logger.error(f'Database error in get_all_galleries: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        
# Get detailed information about a specific gallery
@galleries.route("/<int:galleryID>", methods=["GET"])
def get_branch(galleryID):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Galleries WHERE galleryID = %s", (galleryID,))
        gallery = cursor.fetchone()

        if not gallery:
            return jsonify({"error": "Museum branch not found"}), 404

        cursor.execute("SELECT * FROM Exhibits WHERE galleryID = %s", (galleryID,))
        gallery["Exhibits"] = cursor.fetchall()

        return jsonify(gallery), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
           
# PUT /galleries/<galleryID>
@galleries.route("/<int:galleryID>", methods=["PUT"])
def update_gallery(galleryID):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'PUT /gallaries/{galleryID}')
        data = request.get_json()

        cursor.execute("SELECT galleryID FROM Galleries WHERE galleryID = %s", (galleryID,))
        if not cursor.fetchone():
            return jsonify({"error": "Gallery not found"}), 404

        allowed_fields = ["branchID", "isInUse", "name", "wing", "artworkCapacity"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(galleryID)
        query = f"UPDATE Galleries SET {', '.join(update_fields)} WHERE galleryID = %s"
        cursor.execute(query, params)
        get_db().commit()

        return jsonify({"message": "Gallery updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in update_gallery: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

#DELETE /gallaries
@galleries.route("/<int:galleryID>", methods=["DELETE"])
def delete_gallery(galleryID):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'DELETE /galleries/{galleryID}')

        cursor.execute("SELECT galleryID FROM Galleries WHERE galleryID = %s", (galleryID,))
        if not cursor.fetchone():
            return jsonify({"error": "Gallery not found"}), 404

        cursor.execute("DELETE FROM Galleries WHERE galleryID = %s", (galleryID,))
        get_db().commit()

        return jsonify({"message": "Gallery deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in delete_gallery: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close() 
