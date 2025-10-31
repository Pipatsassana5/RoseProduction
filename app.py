# app.py

import os
from flask import Config, Flask, send_from_directory
from flask_cors import CORS
from routes.control_route import control_bp
from routes.record_route import record_bp

# --- *** แก้ไขส่วนนี้ *** ---
# ชี้ Static Folder ไปยังโฟลเดอร์ 'dist' ที่ React Build เสร็จ
# (ซึ่งจะอยู่ที่ 'frontend/dist')
static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'frontend/dist'))

app = Flask(__name__,
            static_folder=static_folder_path,
            static_url_path='')  # ให้ URL path ของ static files เริ่มที่ root (/)

CORS(app)

# -------------------------

# Register API blueprints (เหมือนเดิม)
app.register_blueprint(record_bp)
app.register_blueprint(control_bp)


# --- *** เพิ่มส่วนนี้: Route สำหรับ Serve React App *** ---
# Route นี้จะจับคู่กับ URL ทั้งหมดที่ *ไม่ใช่* API (ที่ลงทะเบียนไว้ด้านบน)
# และส่ง index.html กลับไปให้ React ทำงาน
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    # ถ้า path ที่ร้องขอเป็นไฟล์ที่มีอยู่จริงใน static_folder (เช่น assets/index-123.js)
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        # ถ้าไม่ใช่ไฟล์ (เช่น /dashboard, /about) ให้ส่ง index.html
        # เพื่อให้ React Router (ถ้ามี) ทำงาน
        return send_from_directory(app.static_folder, 'index.html')


# ----------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)