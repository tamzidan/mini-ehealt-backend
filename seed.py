from dotenv import load_dotenv
load_dotenv() # Memuat environment variables dari file .env

from app import app, db, Doctor, TimeSlot
from datetime import datetime, time, timedelta
import random

def seed_data():
    with app.app_context():
        # Hapus data lama agar tidak duplikat
        print("Menghapus data lama...")
        db.session.query(TimeSlot).delete()
        db.session.query(Doctor).delete()
        db.session.commit()

        print("Membuat data dokter baru...")
        
        # Data dokter yang lebih lengkap
        doctors_data = [
            # Dokter Umum
            {
                "name": "Dr. Ahmad Wijaya, Sp.PD",
                "category": "UMUM",
                "location": "RS Siloam Jakarta",
                "schedule_summary": "Senin - Jumat, 08:00-16:00",
                "rating": 4.8,
                "price": 150000,
                "specialty": "Penyakit Dalam",
                "experience": 8,
                "description": "Dokter spesialis penyakit dalam dengan pengalaman 8 tahun dalam menangani berbagai penyakit internal. Ahli dalam diagnosis dan pengobatan diabetes, hipertensi, dan penyakit jantung.",
                "education": "S1 Kedokteran - Universitas Indonesia;Sp.PD - Universitas Indonesia;Fellowship Endokrinologi - RSCM",
                "work_days": [0, 1, 2, 3, 4],  # Senin-Jumat
                "work_hours": (8, 16)
            },
            {
                "name": "Dr. Andi Prasetyo, Sp.PD",
                "category": "UMUM", 
                "location": "RS Permata Hijau",
                "schedule_summary": "Selasa - Sabtu, 09:00-15:00",
                "rating": 4.7,
                "price": 175000,
                "specialty": "Penyakit Dalam & Geriatri",
                "experience": 10,
                "description": "Spesialis penyakit dalam dengan fokus pada geriatri dan penanganan lansia. Berpengalaman menangani penyakit degeneratif dan komplikasi diabetes.",
                "education": "S1 Kedokteran - Universitas Gadjah Mada;Sp.PD - Universitas Gadjah Mada",
                "work_days": [1, 2, 3, 4, 5],  # Selasa-Sabtu
                "work_hours": (9, 15)
            },
            
            # Dokter Gigi
            {
                "name": "Dr. Sarah Putri, Sp.KG",
                "category": "GIGI",
                "location": "Klinik Smile Dental Center",
                "schedule_summary": "Selasa - Sabtu, 09:00-17:00",
                "rating": 4.9,
                "price": 200000,
                "specialty": "Konservasi Gigi & Estetika",
                "experience": 6,
                "description": "Spesialis konservasi gigi dengan keahlian dalam bidang estetika dental. Menangani perawatan saluran akar, tambal gigi estetik, dan veneer.",
                "education": "S1 Kedokteran Gigi - Universitas Gadjah Mada;Sp.KG - Universitas Gadjah Mada",
                "work_days": [1, 2, 3, 4, 5],  # Selasa-Sabtu
                "work_hours": (9, 17)
            },
            {
                "name": "Dr. Sinta Dewi, Sp.KG",
                "category": "GIGI",
                "location": "Dental Care Center Menteng",
                "schedule_summary": "Senin - Jumat, 10:00-18:00",
                "rating": 4.8,
                "price": 225000,
                "specialty": "Ortodonti & Bedah Mulut",
                "experience": 8,
                "description": "Spesialis ortodonti dengan keahlian dalam pemasangan behel dan koreksi maloklusi. Juga menangani bedah mulut minor.",
                "education": "S1 Kedokteran Gigi - Universitas Indonesia;Sp.KG - Universitas Indonesia;Fellowship Ortodonti - Singapura",
                "work_days": [0, 1, 2, 3, 4],  # Senin-Jumat
                "work_hours": (10, 18)
            },
            
            # Dokter Mata
            {
                "name": "Dr. Budi Santoso, Sp.M",
                "category": "MATA",
                "location": "Jakarta Eye Center",
                "schedule_summary": "Senin - Kamis, 10:00-15:00",
                "rating": 4.7,
                "price": 300000,
                "specialty": "Retina & Vitreus",
                "experience": 12,
                "description": "Ahli retina dan vitreus dengan pengalaman lebih dari 10 tahun. Menangani penyakit retina diabetik, degenerasi makula, dan bedah vitreoretinal.",
                "education": "S1 Kedokteran - Universitas Airlangga;Sp.M - Universitas Airlangga;Fellowship Retina - Melbourne Eye Institute",
                "work_days": [0, 1, 2, 3],  # Senin-Kamis
                "work_hours": (10, 15)
            },
            {
                "name": "Dr. Maya Indira, Sp.M",
                "category": "MATA",
                "location": "RS Mata Cicendo",
                "schedule_summary": "Rabu - Minggu, 08:00-14:00",
                "rating": 4.6,
                "price": 280000,
                "specialty": "Katarak & Refraksi",
                "experience": 9,
                "description": "Spesialis mata dengan fokus pada bedah katarak dan koreksi refraksi. Berpengalaman dalam teknik fakoemulsifikasi dan implantasi IOL premium.",
                "education": "S1 Kedokteran - Universitas Padjadjaran;Sp.M - Universitas Padjadjaran",
                "work_days": [2, 3, 4, 5, 6],  # Rabu-Minggu
                "work_hours": (8, 14)
            },
            
            # Dokter Kulit
            {
                "name": "Dr. Lisa Indira, Sp.KK",
                "category": "KULIT",
                "location": "Klinik Dermatologi Estetika",
                "schedule_summary": "Rabu - Minggu, 11:00-18:00",
                "rating": 4.6,
                "price": 250000,
                "specialty": "Dermatologi Kosmetik & Estetika",
                "experience": 7,
                "description": "Spesialis kulit dan kelamin dengan fokus pada dermatologi kosmetik. Ahli dalam perawatan anti-aging, laser treatment, dan chemical peeling.",
                "education": "S1 Kedokteran - Universitas Indonesia;Sp.KK - Universitas Indonesia;Fellowship Dermatologi Estetika - Korea",
                "work_days": [2, 3, 4, 5, 6],  # Rabu-Minggu
                "work_hours": (11, 18)
            },
            {
                "name": "Dr. Ratna Sari, Sp.KK",
                "category": "KULIT",
                "location": "RS Kulit Jakarta",
                "schedule_summary": "Senin - Jumat, 09:00-16:00",
                "rating": 4.5,
                "price": 230000,
                "specialty": "Dermatologi Medis",
                "experience": 11,
                "description": "Spesialis dermatologi medis dengan fokus pada pengobatan penyakit kulit seperti eksim, psoriasis, dan infeksi kulit. Berpengalaman dalam dermatologi pediatrik.",
                "education": "S1 Kedokteran - Universitas Gadjah Mada;Sp.KK - Universitas Gadjah Mada",
                "work_days": [0, 1, 2, 3, 4],  # Senin-Jumat
                "work_hours": (9, 16)
            },
            
            # Dokter Jantung
            {
                "name": "Dr. Rahman Hakim, Sp.JP",
                "category": "JANTUNG",
                "location": "RS Jantung Harapan Kita",
                "schedule_summary": "Senin - Sabtu, 07:00-14:00",
                "rating": 4.5,
                "price": 400000,
                "specialty": "Kardiologi Intervensi",
                "experience": 15,
                "description": "Spesialis jantung dan pembuluh darah dengan keahlian dalam kardiologi intervensi. Berpengalaman dalam tindakan kateterisasi jantung dan pemasangan stent.",
                "education": "S1 Kedokteran - Universitas Indonesia;Sp.JP - Universitas Indonesia;Fellowship Interventional Cardiology - National Heart Centre Singapore",
                "work_days": [0, 1, 2, 3, 4, 5],  # Senin-Sabtu
                "work_hours": (7, 14)
            },
            {
                "name": "Dr. Dian Permata, Sp.JP",
                "category": "JANTUNG",
                "location": "RS Premier Jatinegara",
                "schedule_summary": "Selasa - Sabtu, 08:00-15:00",
                "rating": 4.4,
                "price": 380000,
                "specialty": "Kardiologi Anak",
                "experience": 12,
                "description": "Spesialis jantung anak dengan fokus pada diagnosis dan penanganan penyakit jantung kongenital. Ahli dalam ekokardiografi pediatri.",
                "education": "S1 Kedokteran - Universitas Airlangga;Sp.JP - Universitas Airlangga;Fellowship Pediatric Cardiology - Boston Children Hospital",
                "work_days": [1, 2, 3, 4, 5],  # Selasa-Sabtu
                "work_hours": (8, 15)
            },
            
            # Dokter Anak
            {
                "name": "Dr. Citra Lestari, Sp.A",
                "category": "ANAK",
                "location": "RSIA Bunda Jakarta",
                "schedule_summary": "Senin - Jumat, 09:00-16:00",
                "rating": 4.8,
                "price": 180000,
                "specialty": "Tumbuh Kembang Anak",
                "experience": 7,
                "description": "Pediatri dengan fokus pada tumbuh kembang anak. Menangani gangguan perkembangan, vaksinasi, dan konsultasi nutrisi anak.",
                "education": "S1 Kedokteran - Universitas Padjadjaran;Sp.A - Universitas Padjadjaran;Fellowship Tumbuh Kembang - RSCM",
                "work_days": [0, 1, 2, 3, 4],  # Senin-Jumat
                "work_hours": (9, 16)
            },
            {
                "name": "Dr. Maya Sari, Sp.A",
                "category": "ANAK",
                "location": "RS Anak Bunda",
                "schedule_summary": "Senin - Sabtu, 08:00-15:00",
                "rating": 4.7,
                "price": 165000,
                "specialty": "Pediatri Umum & Neonatologi",
                "experience": 9,
                "description": "Spesialis anak dengan keahlian dalam neonatologi. Menangani bayi baru lahir, perawatan NICU, dan penyakit anak umum.",
                "education": "S1 Kedokteran - Universitas Indonesia;Sp.A - Universitas Indonesia;Fellowship Neonatologi - RSCM",
                "work_days": [0, 1, 2, 3, 4, 5],  # Senin-Sabtu
                "work_hours": (8, 15)
            },
            {
                "name": "Dr. Indra Pratama, Sp.A",
                "category": "ANAK",
                "location": "Klinik Anak Sehat",
                "schedule_summary": "Selasa - Minggu, 10:00-17:00",
                "rating": 4.6,
                "price": 170000,
                "specialty": "Alergi & Imunologi Anak",
                "experience": 8,
                "description": "Spesialis anak dengan fokus pada alergi dan imunologi. Menangani asma anak, alergi makanan, dan gangguan sistem imun pada anak.",
                "education": "S1 Kedokteran - Universitas Gadjah Mada;Sp.A - Universitas Gadjah Mada;Fellowship Alergi Imunologi - National University Hospital Singapore",
                "work_days": [1, 2, 3, 4, 5, 6],  # Selasa-Minggu
                "work_hours": (10, 17)
            }
        ]

        # Buat objek Doctor dan simpan ke database
        doctors = []
        for i, doc_data in enumerate(doctors_data, 1):
            # Generate image URL menggunakan different methods
            image_options = [
                f"https://images.unsplash.com/photo-{1559757148294 + i}?w=300&h=300&fit=crop&crop=face",  # Unsplash
                f"https://randomuser.me/api/portraits/{'men' if i % 2 == 0 else 'women'}/{(i * 7) % 50 + 1}.jpg",  # Random User
                f"https://robohash.org/doctor{i}?set=set4&size=300x300",  # RoboHash
                f"https://api.dicebear.com/7.x/physician/svg?seed=doctor{i}",  # DiceBear physician
                f"http://127.0.0.1:5000/static/images/doctor{i}.jpg"  # Local images (if you have them)
            ]
            
            doctor = Doctor(
                name=doc_data["name"],
                category=doc_data["category"],
                location=doc_data["location"],
                schedule_summary=doc_data["schedule_summary"],
                rating=doc_data["rating"],
                price=doc_data["price"],
                specialty=doc_data["specialty"],
                experience=doc_data["experience"],
                image=image_options[1],  # Menggunakan Random User API (paling reliable)
                description=doc_data["description"],
                education=doc_data["education"]
            )
            doctors.append(doctor)
            db.session.add(doctor)

        # Commit doctors first to get their IDs
        db.session.commit()
        print(f"✅ {len(doctors)} dokter berhasil ditambahkan!")

        # Generate jadwal untuk setiap dokter
        print("Membuat jadwal untuk setiap dokter...")
        total_slots = 0
        
        for doctor, doc_data in zip(doctors, doctors_data):
            work_days = doc_data["work_days"]
            work_start, work_end = doc_data["work_hours"]
            
            # Generate jadwal untuk 14 hari ke depan
            for i in range(14):
                current_date = datetime.now().date() + timedelta(days=i)
                
                # Cek apakah hari ini termasuk hari kerja dokter
                if current_date.weekday() in work_days:
                    # Buat slot untuk setiap jam kerja
                    for hour in range(work_start, work_end):
                        # Skip jam istirahat (12:00-13:00)
                        if hour == 12:
                            continue
                            
                        # Kadang-kadang buat slot tidak tersedia (simulasi booking existing)
                        is_available = random.random() > 0.2  # 80% chance available
                        
                        slot_dt = datetime.combine(current_date, time(hour, 0))
                        slot = TimeSlot(
                            doctor_id=doctor.id,
                            slot_time=slot_dt,
                            price=doctor.price,
                            is_available=is_available
                        )
                        db.session.add(slot)
                        total_slots += 1

        # Commit all time slots
        db.session.commit()
        print(f"✅ {total_slots} slot jadwal berhasil dibuat!")
        
        # Print summary
        print("\n" + "="*50)
        print("SUMMARY SEEDING DATA:")
        print("="*50)
        for category in ["UMUM", "GIGI", "MATA", "KULIT", "JANTUNG", "ANAK"]:
            count = len([d for d in doctors_data if d["category"] == category])
            doctors_in_category = [d["name"] for d in doctors_data if d["category"] == category]
            print(f"Dokter {category}: {count} dokter")
            for name in doctors_in_category:
                print(f"  - {name}")
            print()
            
        print(f"Total Dokter: {len(doctors)}")
        print(f"Total Slot Jadwal: {total_slots}")
        print(f"Periode Jadwal: {datetime.now().date()} - {(datetime.now().date() + timedelta(days=13))}")
        print("\n🎉 Seeding data berhasil selesai!")

if __name__ == '__main__':
    seed_data()