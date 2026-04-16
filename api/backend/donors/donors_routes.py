from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import get_db

artifacts = Blueprint("donors", __name__)

#GET /donors

# Get all donors in the system

@donors.route("/donors", methods=["GET"])
def get_all_donors():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /donors')
        query = "SELECT * FROM Donors"

        cursor.execute(query)
        donor_list = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(donor_list)} donors')
        return jsonify(donor_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_ngos: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@donors.route("/donors/<int:donor_id>", methods=["GET"])
def get_all_donors():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /donors')
        query = "SELECT * FROM Donors where donorID = %s"

        cursor.execute(query, ())
        donor_list = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(donor_list)} donors')
        return jsonify(donor_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_ngos: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

/donors/top-monetary
/donors/top-monetary/{count}
/donors/top-artifact
/donors/top-artifact/{count}


#POST /donors

#PUT /donors

#DELETE /donors
