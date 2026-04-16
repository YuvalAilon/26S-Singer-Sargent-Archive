from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import get_db
from mysql.connector import Error

donors = Blueprint("donors", __name__)

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

# Gets the donor with a specific id
@donors.route("/donors/<int:donor_id>", methods=["GET"])
def get_donor(donor_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Donors WHERE donorID = %s", (donor_id,))
        donor = cursor.fetchone()

        if not donor:
            return jsonify({"error": "Donor not found"}), 404

        return jsonify(donor), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# /donors/top-monetary
@donors.route("/donors/top-monetary", methods=["GET"])
def get_top_monetary_donors():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /donors/top-monetary')

        count = request.args.get("count")
        if (count and int(count) <= 0):
            raise Error(msg=f"Provided count ({count}) was not positive")

        query = """
SELECT contactFirstName, contactLastName, email, SUM(MD.amount) AS total_donations
FROM Donors
JOIN `Singer-Sargent-Archive`.MonetaryDonation MD ON Donors.donorID = MD.donorID
GROUP BY Donors.donorID
ORDER BY total_donations DESC
"""
        params = []

        if count:
            query += " LIMIT %s"
            params.append(count)

        cursor.execute(query, params)
        top_donor_list = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(top_donor_list)} donors')
        return jsonify(top_donor_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_top_monetary_donors: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# /donors/top-artifact
@donors.route("/donors/top-artifact", methods=["GET"])
def get_top_artifact_donors():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /donors/top-artifact')

        count = request.args.get("count")
        if (count and int(count) <= 0):
            raise Error(msg=f"Provided count ({count}) was not positive")

        query = """
SELECT contactFirstName, contactLastName, email, SUM(MD.amount) AS total_donations
FROM Donors
JOIN `Singer-Sargent-Archive`.MonetaryDonation MD ON Donors.donorID = MD.donorID
GROUP BY Donors.donorID
ORDER BY total_donations DESC
"""
        params = []

        if count:
            query += " LIMIT %s"
            params.append(count)

        cursor.execute(query, params)
        top_donor_list = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(top_donor_list)} donors')
        return jsonify(top_donor_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_top_artifact_donors: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# Getting all individual donations
@donors.route("/donors/donations", methods=["GET"])
def get_all_donations():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /donors/donations')

        query = """
SELECT contactFirstName, contactLastName, amount, reason
FROM MonetaryDonation
JOIN `Singer-Sargent-Archive`.Donors D ON MonetaryDonation.donorID = D.donorID
ORDER BY d.donorID;
"""
        cursor.execute(query)
        donations = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(donations)} individual donations')
        return jsonify(donations), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_donations: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# Getting all individual donations
@donors.route("/donors/<int:donor_id>/donations", methods=["GET"])
def get_donations_by_donor(donor_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /donors/donations')

        query = """
SELECT contactFirstName, contactLastName, amount, reason
FROM MonetaryDonation
JOIN `Singer-Sargent-Archive`.Donors D ON MonetaryDonation.donorID = D.donorID
WHERE D.donorID = %s
ORDER BY d.donorID;
"""
        cursor.execute(query, (donor_id,))
        donations = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(donations)} individual donations')
        return jsonify(donations), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_donations_by_donor: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

#POST /donors

#PUT /donors

#DELETE /donors
