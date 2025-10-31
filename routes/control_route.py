from flask import Blueprint, request, jsonify

# สถานะ GPIO ที่จะถูกเก็บใน Server (เพื่อติดตามสถานะปัจจุบัน)
# ในโปรเจกต์จริง ควรเก็บใน Redis หรือ Database เพื่อให้สถานะคงอยู่หลังรีสตาร์ท
# เราจะใช้ Dict ชั่วคราวในที่นี้
gpio_state = {
    "relay1": {
        "pin": 32,  # GPIO Pin ที่ ESP32 ใช้นำไปต่อ Relay
        "status": "OFF",  # สถานะปัจจุบัน: "ON" หรือ "OFF"
        "name": "Pump Relay 1" # (อัปเดตชื่อเล็กน้อย)
    },
    # เพิ่ม Pin 33
    "relay2": {
        "pin": 33,  # GPIO Pin ที่ ESP32 ใช้นำไปต่อ Relay
        "status": "OFF",  # สถานะปัจจุบัน: "ON" หรือ "OFF"
        "name": "Light Relay"
    }
}
control_bp = Blueprint('control_bp', __name__, url_prefix='/control')


@control_bp.route('/relay/<int:pin_id>', methods=['POST'])
def set_relay_state(pin_id):
    """
    Endpoint สำหรับรับคําสั่งจาก Web App เพื่อตั้งค่าสถานะ Relay
    รับ JSON: {"action": "ON" / "OFF"}
    """
    try:
        data = request.json
        action = data.get('action', '').upper()

        target_relay_key = None
        if pin_id == gpio_state["relay1"]["pin"]:
            target_relay_key = "relay1"
        elif pin_id == gpio_state["relay2"]["pin"]:
            target_relay_key = "relay2"

        if target_relay_key is None:
            return jsonify({"error": f"Invalid pin ID: {pin_id}"}), 404

        # ตรวจสอบ Action ที่ถูกต้อง
        if action in ["ON", "OFF"]:
            gpio_state[target_relay_key]["status"] = action
            return jsonify({
                "message": f"Relay on Pin {pin_id} set to {action}",
                "status": action
            }), 200
        else:
            return jsonify({"error": "Invalid action. Use 'ON' or 'OFF'"}), 400

    except Exception as e:
        print(f"Error setting relay state: {e}")
        return jsonify({"error": "Internal server error"}), 500


@control_bp.route('/relay/<int:pin_id>', methods=['GET'])
def get_relay_state(pin_id):
    """
    Endpoint สำหรับ ESP32 ดึงสถานะปัจจุบันที่ถูกตั้งค่าโดย Web App
    """
    if pin_id == gpio_state["relay1"]["pin"]:
        return jsonify({
            "pin": pin_id,
            "status": gpio_state["relay1"]["status"]
        }), 200
        # ตรวจสอบ Pin 33
    elif pin_id == gpio_state["relay2"]["pin"]:
        return jsonify({
            "pin": pin_id,
            "status": gpio_state["relay2"]["status"]
        }), 200
        # ถ้าไม่ตรงเลย
    else:
        return jsonify({"error": f"Invalid pin ID: {pin_id}"}), 404
