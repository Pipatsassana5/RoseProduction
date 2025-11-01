# app.py
# ไฟล์นี้จะทำหน้าที่ "Import" และ "รัน"

import os
from flask import send_from_directory

# 1. Import 'app' และ 'socketio' จากไฟล์ใหม่ของเรา
from extensions import app, socketio

# 2. Import routes และ events
from routes.control_route import control_bp
from routes.record_route import record_bp
import socket_events  # (ตอนนี้บรรทัดนี้ปลอดภัยแล้ว)

# 3. Register Blueprints (เหมือนเดิม)
app.register_blueprint(record_bp)
app.register_blueprint(control_bp)

# 4. สร้าง Route (เหมือนเดิม)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# 5. รันเซิร์ฟเวอร์ (เหมือนเดิม)
if __name__ == '__main__':
    print("Starting Flask-SocketIO server with Eventlet...")
    socketio.run(app, host='0.0.0.0', port=3000, debug=True, allow_unsafe_werkzeug=True)