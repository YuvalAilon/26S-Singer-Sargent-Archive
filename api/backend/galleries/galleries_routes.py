from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import get_db
from mysql.connector import Error

branches = Blueprint("galleries", __name__)