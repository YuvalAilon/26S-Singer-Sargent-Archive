from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import get_db, getDBQuery
from mysql.connector import Error

exhibits = Blueprint("exhibits", __name__)


# GET /exhibits/current[?city=<city>]
@exhibits.route("/current", methods=["GET"])
def get_current_exhibits():
    city = request.args.get("city")

    base_query = """
        SELECT mb.branchName,
               mb.street, mb.city, mb.zip,
               mb.contactPhone,
               e.name AS exhibit,
               e.dateStart, e.dateEnd, e.exhibitID
        FROM Exhibits e
        JOIN Galleries g ON e.galleryID = g.galleryID
        JOIN MuseumBranch mb ON g.branchID = mb.branchID
        WHERE (e.dateEnd >= CURDATE() OR e.dateEnd IS NULL)
    """

    cursor = get_db().cursor(dictionary=True)
    try:
        if city:
            current_app.logger.info(f"GET /exhibits/current?city={city}")
            query = base_query + " AND mb.city = %s ORDER BY mb.branchName, e.dateStart"
            cursor.execute(query, (city,))
        else:
            current_app.logger.info("GET /exhibits/current")
            query = base_query + " ORDER BY mb.branchName, e.dateStart"
            cursor.execute(query)
        rows = cursor.fetchall()
        current_app.logger.info(f"Retrieved {len(rows)} current exhibits")
        return jsonify(rows), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_current_exhibits: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /exhibits/branch-stats
@exhibits.route("/branch-stats", methods=["GET"])
def get_branch_exhibit_stats():
    query = """
        SELECT mb.branchName,
               COUNT(e.exhibitID) AS totalExhibits,
               MIN(e.dateStart)   AS earliestExhibit,
               MAX(e.dateStart)   AS mostRecentExhibit,
               (COUNT(e.exhibitID) /
                NULLIF(TIMESTAMPDIFF(MONTH, MIN(e.dateStart), CURDATE()), 0)
               ) AS exhibitsPerMonth
        FROM Exhibits e
        JOIN Galleries g ON e.galleryID = g.galleryID
        JOIN MuseumBranch mb ON g.branchID = mb.branchID
        GROUP BY mb.branchName
        ORDER BY exhibitsPerMonth DESC
    """
    return getDBQuery(query, "GET /exhibits/branch-stats")

# GET /exhibits/<int:exhibitID>/artifacts
@exhibits.route("/<int:exhibitID>/artifacts", methods=["GET"])
def get_artifacts_in_exhibit(exhibitID):
    query = f"SELECT * FROM Artifact WHERE displayedInExhibitID = {exhibitID}"
    
    return getDBQuery(query, f"GET /exhibits/{exhibitID}/artifacts")