import time
from extensions import socketio
from flask_socketio import emit
from models.Record_model import Record_Model
from routes.control_route import gpio_state  # Import สถานะปั๊มมาใช้ร่วมกัน


# === จัดการ Event เมื่อมี Client (React หรือ ESP32) เชื่อมต่อ ===
@socketio.on('connect')
def handle_connect():
    print('Client connected!')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected!')


# === จัดการ Event เมื่อ ESP32 ส่งข้อมูลเซ็นเซอร์มา ===
# (นี่คือสิ่งที่มาแทน POST /record/create)
@socketio.on('sensor_data')
def handle_sensor_data(json_data):
    print('Received sensor data: ' + str(json_data))

    try:
        # (คุณอาจต้องตรวจสอบ Schema ที่นี่ถ้าต้องการ)
        record_data = json_data

        # เพิ่ม Timestamp
        timestamp_ms = int(time.time() * 1000)
        record_data['timestamp'] = timestamp_ms

        # บันทึกลง DB
        Record_Model.create_record(record_data)  #

        # แปลง _id เป็น str ก่อนส่งกลับ
        if '_id' in record_data:
            record_data['_id'] = str(record_data['_id'])

        # ส่งข้อมูลล่าสุดนี้ไปยัง Client "ทุกคน" (เช่น React)
        emit('new_sensor_data', record_data, broadcast=True)

    except Exception as e:
        print(f"Error processing sensor data: {e}")


# === จัดการ Event เมื่อ React สั่งควบคุม Relay ===
# (นี่คือสิ่งที่มาแทน POST /control/relay/<pin_id>)
@socketio.on('control_relay')
def handle_control_relay(json_data):
    # json_data จะมีหน้าตาประมาณ {'pin': 32, 'action': 'ON'}
    try:
        pin = int(json_data.get('pin'))
        action = json_data.get('action', '').upper()

        target_relay_key = None
        if pin == gpio_state["relay1"]["pin"]:
            target_relay_key = "relay1"
        elif pin == gpio_state["relay2"]["pin"]:
            target_relay_key = "relay2"

        if target_relay_key and action in ["ON", "OFF"]:
            # อัปเดตสถานะใน Server
            gpio_state[target_relay_key]["status"] = action
            print(f"Relay {pin} set to {action}")

            # ส่งสถานะใหม่นี้ไปยัง Client "ทุกคน" (ESP32 และ React จะได้รับ)
            response_data = {'pin': pin, 'status': action}
            emit('relay_update', response_data, broadcast=True)

    except Exception as e:
        print(f"Error processing control command: {e}")