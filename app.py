import os
from dotenv import load_dotenv
load_dotenv() # <-- TAMBAHKAN INI

import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
from sqlalchemy.exc import IntegrityError


# -----------------------------------------------------------------------------
# Inisialisasi Aplikasi Flask & Konfigurasi Database
# -----------------------------------------------------------------------------
app = Flask(__name__)

# --- Ganti blok CORS Anda dengan ini ---
# Dapatkan URL frontend dari environment variable (untuk produksi)
frontend_prod_url = os.environ.get('FRONTEND_URL')

# Daftar asal (origin) yang diizinkan
# Secara default, izinkan localhost untuk pengembangan
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

# Jika ada URL produksi, tambahkan ke daftar
if frontend_prod_url:
    origins.append(frontend_prod_url)

CORS(app, resources={
    r"/v1/*": {
        "origins": origins, # Gunakan daftar dinamis
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
# --- Akhir dari blok CORS ---

# Konfigurasi koneksi ke database MySQL
# Format: 'mysql+mysqlconnector://<user>:<password>@<host>/<database_name>'
DB_USER = 'doctor_app_user'
DB_PASS = 'PasswordSuperAman123!'
DB_HOST = 'localhost'
DB_NAME = 'doctor_booking_db'

# Baris ini sekarang akan mendapatkan DATABASE_URL dari file .env saat dijalankan di lokal
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi SQLAlchemy
db = SQLAlchemy(app)

# -----------------------------------------------------------------------------
# Models (Representasi Tabel Database)
# -----------------------------------------------------------------------------

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(150))
    schedule_summary = db.Column(db.String(255), comment="Teks ringkasan jadwal, cth: Senin - Jumat, 08:00-16:00")
    rating = db.Column(db.Float, default=0.0)
    price = db.Column(db.Integer, nullable=False)
    specialty = db.Column(db.String(100))
    experience = db.Column(db.Integer)
    image = db.Column(db.String(255))
    description = db.Column(db.Text)
    education = db.Column(db.Text) # Bisa disimpan sebagai JSON string atau dipisah dengan '; '
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self, detail=False):
        data = {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "location": self.location,
            "schedule": self.schedule_summary,
            "rating": self.rating,
            "price": f"Rp {self.price:,}".replace(',', '.'),
            "image": self.image,
            "specialty": self.specialty,
            "experience": self.experience,
            "createdAt": self.created_at.isoformat() + "Z",
            "updatedAt": self.updated_at.isoformat() + "Z"
        }
        if detail:
            data.update({
                "description": self.description,
                "education": self.education.split(';') if self.education else []
            })
        return data

class TimeSlot(db.Model):
    id = db.Column(db.String(50), primary_key=True, default=lambda: f"slot_{uuid.uuid4().hex[:10]}")
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    slot_time = db.Column(db.DateTime, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    price = db.Column(db.Integer, nullable=False)
    
    # Relasi ke booking
    booking_id = db.Column(db.String(50), db.ForeignKey('booking.booking_id'), nullable=True, unique=True)
    doctor = db.relationship('Doctor', backref=db.backref('time_slots', lazy='dynamic'))

    def to_dict(self):
        return {
            "slotId": self.id,
            "time": self.slot_time.strftime('%H:%M'),
            "available": self.is_available,
            "price": f"Rp {self.price:,}".replace(',', '.'),
        }

class Booking(db.Model):
    booking_id = db.Column(db.String(50), primary_key=True, default=lambda: f"BK{uuid.uuid4().hex[:8].upper()}")
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_name = db.Column(db.String(100), nullable=False)
    patient_phone = db.Column(db.String(20), nullable=False)
    patient_email = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='CONFIRMED') # CONFIRMED, CANCELLED, COMPLETED
    payment_status = db.Column(db.String(20), default='PENDING') # PENDING, PAID, REFUNDED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relasi
    slot = db.relationship('TimeSlot', backref='booking', uselist=False, foreign_keys='TimeSlot.booking_id')
    doctor = db.relationship('Doctor')

    def to_dict(self):
        return {
            "bookingId": self.booking_id,
            "doctorId": self.doctor_id,
            "doctorName": self.doctor.name,
            "date": self.slot.slot_time.strftime('%Y-%m-%d'),
            "time": self.slot.slot_time.strftime('%H:%M'),
            "price": f"Rp {self.slot.price:,}".replace(',', '.'),
            "patientName": self.patient_name,
            "patientPhone": self.patient_phone,
            "patientEmail": self.patient_email,
            "notes": self.notes,
            "status": self.status,
            "paymentStatus": self.payment_status,
            "createdAt": self.created_at.isoformat() + "Z",
            "updatedAt": self.updated_at.isoformat() + "Z"
        }

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
def make_error_response(code, message, status_code):
    return jsonify({"success": False, "error": {"code": code, "message": message}}), status_code

# -----------------------------------------------------------------------------
# API Endpoints (Sudah dimodifikasi untuk menggunakan Database)
# -----------------------------------------------------------------------------

# Tag: System
@app.route('/v1/health', methods=['GET'])
def health_check():
    try:
        # Cek koneksi database dengan query sederhana
        db.session.execute(db.text('SELECT 1'))
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {e}"

    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0",
        "database": db_status
    })

# Tag: Doctors
@app.route('/v1/doctors', methods=['GET'])
def get_doctors():
    args = request.args
    query = Doctor.query

    # Filtering
    if 'category' in args:
        query = query.filter(Doctor.category == args['category'])
    if 'location' in args:
        query = query.filter(Doctor.location.ilike(f"%{args['location']}%"))
    if 'search' in args:
        search_term = f"%{args['search']}%"
        query = query.filter(db.or_(Doctor.name.ilike(search_term), Doctor.specialty.ilike(search_term)))

    # Sorting
    sort_map = {
        'rating_desc': Doctor.rating.desc(),
        'rating_asc': Doctor.rating.asc(),
        'price_desc': Doctor.price.desc(),
        'price_asc': Doctor.price.asc(),
        'name_desc': Doctor.name.desc(),
        'name_asc': Doctor.name.asc(),
    }
    sort_by = sort_map.get(args.get('sort', 'rating_desc'), Doctor.rating.desc())
    query = query.order_by(sort_by)

    # Pagination
    page = args.get('page', 1, type=int)
    limit = args.get('limit', 20, type=int)
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    
    doctors_data = [doc.to_dict() for doc in pagination.items]

    return jsonify({
        "success": True,
        "data": doctors_data,
        "pagination": {
            "currentPage": pagination.page,
            "totalPages": pagination.pages,
            "totalItems": pagination.total,
            "itemsPerPage": pagination.per_page
        }
    })

@app.route('/v1/doctors/<int:id>', methods=['GET'])
def get_doctor_detail(id):
    doctor = Doctor.query.get_or_404(id)
    return jsonify({"success": True, "data": doctor.to_dict(detail=True)})

# Tag: Schedules
@app.route('/v1/doctors/<int:id>/schedule', methods=['GET'])
def get_doctor_schedule(id):
    doctor = Doctor.query.get_or_404(id, description="Dokter tidak ditemukan")

    start_date_str = request.args.get('date', date.today().strftime('%Y-%m-%d'))
    days_to_show = request.args.get('days', 7, type=int)
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = start_date + timedelta(days=days_to_show)

    slots = TimeSlot.query.filter(
        TimeSlot.doctor_id == id,
        TimeSlot.slot_time >= start_date,
        TimeSlot.slot_time < end_date
    ).order_by(TimeSlot.slot_time).all()

    # Kelompokkan slot berdasarkan tanggal
    schedule_data = {}
    for slot in slots:
        slot_date_str = slot.slot_time.strftime('%Y-%m-%d')
        if slot_date_str not in schedule_data:
            schedule_data[slot_date_str] = {
                "date": slot_date_str,
                "dayName": slot.slot_time.strftime('%A'),
                "timeSlots": []
            }
        schedule_data[slot_date_str]["timeSlots"].append(slot.to_dict())

    doctor_info = { "id": doctor.id, "name": doctor.name, "category": doctor.category, "specialty": doctor.specialty }

    return jsonify({
        "success": True,
        "data": list(schedule_data.values()),
        "doctorInfo": doctor_info
    })

# Tag: Bookings
@app.route('/v1/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    if not data or 'slotId' not in data or 'patientName' not in data:
        return make_error_response("VALIDATION_ERROR", "Data tidak lengkap", 400)

    slot = TimeSlot.query.get(data['slotId'])
    if not slot:
        return make_error_response("NOT_FOUND", "Slot jadwal tidak ditemukan", 404)
    if not slot.is_available:
        return make_error_response("SLOT_UNAVAILABLE", "Slot waktu sudah tidak tersedia", 409)

    try:
        new_booking = Booking(
            doctor_id=slot.doctor_id,
            patient_name=data['patientName'],
            patient_phone=data['patientPhone'],
            patient_email=data['patientEmail'],
            notes=data.get('notes')
        )
        
        # Hubungkan booking dan slot
        slot.is_available = False
        slot.booking = new_booking
        
        db.session.add(new_booking)
        db.session.add(slot)
        db.session.commit()

        return jsonify({"success": True, "data": new_booking.to_dict()}), 201

    except IntegrityError:
        db.session.rollback()
        return make_error_response("SERVER_ERROR", "Gagal menyimpan booking karena error integritas", 500)
    except Exception as e:
        db.session.rollback()
        return make_error_response("SERVER_ERROR", str(e), 500)

# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)