from database.db import record_collection
from bson.objectid import ObjectId
from pymongo import DESCENDING # Import เพื่อใช้เรียงลำดับจากมากไปน้อย

class Record_Model:
    @staticmethod
    def create_record(record_data):
        return record_collection.insert_one(record_data)

    @staticmethod
    def get_history_data(limit=20):
        if record_collection is None:
            # ใช้ข้อมูลจำลองถ้า MongoDB เชื่อมต่อไม่ได้ (เพื่อป้องกัน Crash)
            return []

        try:

            # ใช้ sort เพื่อเรียงตาม timestamp (สมมติว่าคุณเพิ่ม timestamp ใน POST data แล้ว)
            # -1 หมายถึง Descending (ใหม่สุดอยู่บน)
            records_cursor = record_collection.find().sort('timestamp', -1).limit(limit)

            # แปลง Cursor เป็น List และกลับลำดับให้เก่าอยู่ก่อนใหม่ (Ascending)
            # เพื่อให้กราฟใน React แสดงผลตามลำดับเวลาที่ถูกต้อง (ซ้ายไปขวา)
            history_list = list(records_cursor)
            history_list.reverse()

            # แปลง ObjectId เป็น string เพื่อให้ jsonify ทำงานได้
            for record in history_list:
                if '_id' in record:
                    record['_id'] = str(record['_id'])

            return history_list

        except Exception as e:
            # ในสภาพแวดล้อมจริง ควรมีการจัดการ Error ที่ซับซ้อนกว่านี้
            print(f"Database error in get_history_data: {e}")
            return []