from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import get_db
from mysql.connector import Error

donors = Blueprint("donors", __name__)

#GET /donors

# Get all donors in the system
@donors.route("", methods=["GET"])
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
@donors.route("/<int:donor_id>", methods=["GET"])
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
@donors.route("/top-monetary", methods=["GET"])
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
            params.append(int(count))

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
@donors.route("/top-artifact", methods=["GET"])
def get_top_artifact_donors():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /donors/top-artifact')

        count = request.args.get("count")
        if (count and int(count) <= 0):
            raise Error(msg=f"Provided count ({count}) was not positive")

        query = """
SELECT contactFirstName, contactLastName, email, COUNT(*) AS pieces_donated
FROM Donors
JOIN `Singer-Sargent-Archive`.ArtifactRequest AR ON Donors.donorID = AR.loaningDonorID
GROUP BY Donors.donorID
ORDER BY pieces_donated DESC
"""
        params = []

        if count:
            query += " LIMIT %s"
            params.append(int(count))

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
@donors.route("/donations", methods=["GET"])
def get_all_donations():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /donors/donations')

        query = """
SELECT contactFirstName, contactLastName, amount, reason
FROM MonetaryDonation
JOIN `Singer-Sargent-Archive`.Donors D ON MonetaryDonation.donorID = D.donorID
ORDER BY D.donorID;
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
@donors.route("/<int:donor_id>/donations/monetary", methods=["GET"])
def get_monetary_donations_by_donor(donor_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /donors/donations')

        query = """
SELECT contactFirstName, contactLastName, amount, reason
FROM MonetaryDonation
JOIN `Singer-Sargent-Archive`.Donors D ON MonetaryDonation.donorID = D.donorID
WHERE D.donorID = %s
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

# Getting all individual donations
@donors.route("/<int:donor_id>/donations/artifact", methods=["GET"])
def get_artifact_donations_by_donor(donor_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /donors/donations')

        query = """
SELECT contactFirstName, contactLastName, Artifact.name as artifactName, loanDateStart, loanDateEnd, Artifact.ArtifactID, ArtifactRequest.RequestID
FROM Donors
JOIN ArtifactRequest ON Donors.donorID = ArtifactRequest.loaningDonorID
JOIN ArtifactRequestRelations ON ArtifactRequest.requestID = ArtifactRequestRelations.requestID
JOIN Artifact ON ArtifactRequestRelations.artifactID = Artifact.artifactID
WHERE Donors.donorID = %s
ORDER BY contactFirstName, contactLastName, loanDateEnd;
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
@donors.route("", methods=["POST"])
def add_donor():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        required_fields = ["organizationName", "email", "contactTitle", "contactFirstName", "contactMiddleName", "contactLastName", "street", "city", "zip"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        query = """
            INSERT INTO Donors (organizationName, email, contactTitle, contactFirstName, contactMiddleName, contactLastName, street, city, zip)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["organizationName"],
            data["email"],
            data["contactTitle"],
            data["contactFirstName"],
            data["contactMiddleName"],
            data["contactLastName"],
            data["street"],
            data["city"],
            data["zip"]
            ))

        get_db().commit()
        return jsonify({"message": "Donor entered successfully", "donorID": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@donors.route("/<int:donor_id>/donations/monetary", methods=["POST"])
def create_ngo():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        required_fields = ["amount", "reason", "donorID", "branchID"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        query = """
            INSERT INTO MonetaryDonation (amount, reason, donorID, branchID)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["amount"],
            data["reason"],
            data["donorID"],
            data["branchID"]
            ))

        get_db().commit()
        return jsonify({"message": "Donation entered successfully", "monetaryDonationID": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
#PUT /donors
@donors.route("/<int:donor_id>", methods=["PUT"])
def update_donor(donor_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        cursor.execute("SELECT * FROM Donors WHERE DonorID = %s", (donor_id,))
        if not cursor.fetchone():
            return jsonify({"error": "NGO not found"}), 404

        # Build update query dynamically based on provided fields
        allowed_fields = ["organizationName", "email", "contactTitle", "contactFirstName", "contactMiddleName", "contactLastName", "street", "city", "zip"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(donor_id)
        query = f"UPDATE Donors SET {', '.join(update_fields)} WHERE DonorID = %s"
        cursor.execute(query, params)
        get_db().commit()

        return jsonify({"message": "Donor updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# No DELETE for donors
