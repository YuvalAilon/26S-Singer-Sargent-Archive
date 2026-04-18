from flask import Blueprint, request, jsonify
from backend.db_connection import getDBQuery

artists = Blueprint("artists", __name__)

@artists.route("/", methods=["GET"])
def get_all_artists():
    """Fetches all artists from the database"""
    return getDBQuery("SELECT * FROM Artist", "GET /artists")

@artists.route("/<int:artistID>", methods=["GET"])
def get_artist_by_id(artistID):
    """Fetches a single artist by their unique ID"""
    query = f"SELECT * FROM Artist WHERE artistID = {artistID}"
    return getDBQuery(query, f"GET /artists/{artistID}")