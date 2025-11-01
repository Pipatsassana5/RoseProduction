from flask import Blueprint, jsonify
from marshmallow import ValidationError
from models.Record_model import Record_Model
from schemas.record_schema import Record_Schema
import time

record_bp = Blueprint('record_bp', __name__,url_prefix='/record')
record_schema = Record_Schema()


@record_bp.route('/history', methods=['GET'])
def get_history_data():
    try:
        history_data = Record_Model.get_history_data(limit=20)
        latest_data = history_data[-1] if history_data else None

        return jsonify({
            "latestData": latest_data,
            "history": history_data
        }), 200

    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({"error": "Failed to fetch data from model/DB"}), 500


# Endpoint สุขภาพ (Health Check)
@record_bp.route('/status', methods=['GET'])
def api_status():
    return jsonify({"status": "OK", "service": "Flask IoT API"}), 200

