# extensions.py
# ไฟล์นี้จะทำหน้าที่ "สร้าง" instance หลัก

import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

# 1. กำหนดค่า Static Folder
static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'frontend/dist'))

# 2. สร้าง app
app = Flask(__name__,
            static_folder=static_folder_path,
            static_url_path='')

# 3. สร้าง CORS
CORS(app)

# 4. สร้าง socketio
socketio = SocketIO(app, cors_allowed_origins="*")