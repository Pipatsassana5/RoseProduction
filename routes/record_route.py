from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models.Record_model import Record_Model
from schemas.record_schema import Record_Schema
import time

record_bp = Blueprint('record_bp', __name__,url_prefix='/record')
record_schema = Record_Schema()

latest_sensor_data_cache = None

@record_bp.route('/create', methods=['POST'])
def create_record():
    global latest_sensor_data_cache

    try:
        record_data = record_schema.load(request.json)
    except ValidationError as err:
        return jsonify("error", err.messages), 400

    timestamp_ms = int(time.time() * 1000)
    record_data['timestamp'] = timestamp_ms

    Record_Model.create_record(record_data)

    if '_id' in record_data:
        record_data['_id'] = str(record_data['_id'])

    latest_sensor_data_cache = record_data
    return jsonify({"message": "Record created successfully", "timestamp": timestamp_ms}), 201


@record_bp.route('/history', methods=['GET'])
def get_history_data():
    """
    Endpoint สำหรับให้ React Dashboard ดึงข้อมูลล่าสุดและประวัติ
    """
    try:

        # ดึงข้อมูลย้อนหลัง 20 รายการจาก MongoDB
        history_data = Record_Model.get_history_data(limit=20)

        latest_data = history_data[-1] if history_data else None

        global latest_sensor_data_cache
        # ส่งข้อมูลล่าสุดและประวัติกลับไป
        if latest_data and latest_sensor_data_cache is None:
            latest_sensor_data_cache = latest_data

        return jsonify({
            "latestData": latest_data,  # ยังส่ง latest ไปด้วยเผื่อใช้ตอนโหลดครั้งแรก
            "history": history_data
        }), 200

    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({"error": "Failed to fetch data from model/DB"}), 500


# Endpoint สุขภาพ (Health Check)
@record_bp.route('/status', methods=['GET'])
def api_status():
    return jsonify({"status": "OK", "service": "Flask IoT API"}), 200


@record_bp.route('/current', methods=['GET'])
def get_current_data_from_cache():
    """
    Endpoint สำหรับให้ React Dashboard ดึงข้อมูล "ล่าสุด" (จาก Cache)
    Endpoint นี้จะทำงานเร็วมาก เพราะอ่านจาก Memory
    """
    global latest_sensor_data_cache

    if latest_sensor_data_cache is None:
        # กรณี Server เพิ่งเริ่มทำงาน และยังไม่มีข้อมูลส่งมา
        return jsonify({"latestData": None}), 200

    return jsonify({"latestData": latest_sensor_data_cache}), 200