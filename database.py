import sqlite3
import hashlib

conn = sqlite3.connect('kerajaan.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS users')
cursor.execute('DROP TABLE IF EXISTS siswa')
cursor.execute('DROP TABLE IF EXISTS guru')
cursor.execute('DROP TABLE IF EXISTS kelas')
cursor.execute('DROP TABLE IF EXISTS absensi')
cursor.execute('DROP TABLE IF EXISTS lokasi')

cursor.execute('''
CREATE TABLE kelas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL UNIQUE
)''')

cursor.execute('''
CREATE TABLE siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    kelas_id INTEGER,
    FOREIGN KEY (kelas_id) REFERENCES kelas(id)
)''')

cursor.execute('''
CREATE TABLE guru (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    mapel TEXT
)''')

cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    nama TEXT NOT NULL,
    siswa_id INTEGER,
    guru_id INTEGER,
    FOREIGN KEY (siswa_id) REFERENCES siswa(id),
    FOREIGN KEY (guru_id) REFERENCES guru(id)
)''')

cursor.execute('''
CREATE TABLE absensi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    tanggal TEXT,
    jam TEXT,
    status TEXT,
    foto TEXT,
    lat REAL,
    lon REAL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)''')

cursor.execute('''
CREATE TABLE lokasi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lat REAL,
    lon REAL,
    radius INTEGER
)''')

# Lokasi sekolah
cursor.execute("INSERT INTO lokasi (lat, lon, radius) VALUES (-7.3905, 112.7267, 100)")

# SEMUA KELAS
kelas_list = [
    'X SIJA 1', 'X TKW 1', 'X DKV 1', 'X DKV 2',
    'X TKR 1', 'X TKR 2', 'X TKR 3',
    'X BOGA 1', 'X BOGA 2',
    'X AKUNTANSI 1', 'X AKUNTANSI 2',
    'X BUSANA 1',
    'XI SIJA 1', 'XI TKW 1', 'XI DKV 1', 'XI DKV 2',
    'XI TKR 1', 'XI TKR 2', 'XI TKR 3',
    'XI BOGA 1', 'XI BOGA 2',
    'XI AKUNTANSI 1', 'XI AKUNTANSI 2',
    'XI BUSANA 1', 'XI ANIMASI 1',
    'XII SIJA 1', 'XII TKW 1', 'XII DKV 1', 'XII DKV 2',
    'XII TKR 1', 'XII TKR 2', 'XII TKR 3',
    'XII BOGA 1', 'XII BOGA 2',
    'XII AKUNTANSI 1', 'XII AKUNTANSI 2',
    'XII BUSANA 1', 'XII ANIMASI 1'
]
for k in kelas_list:
    cursor.execute("INSERT OR IGNORE INTO kelas (nama) VALUES (?)", (k,))

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# ADMIN
cursor.execute("INSERT INTO users (username, password, role, nama) VALUES (?,?,?,?)",
               ('penguasa', hash_pw('penguasaNEGA666'), 'admin', 'Penguasa Kerajaan'))

# CONTOH GURU
cursor.execute("INSERT OR IGNORE INTO guru (nama, mapel) VALUES (?,?)", ('Drs. Supriyadi, M.Pd', 'Produktif RPL'))
cursor.execute("INSERT INTO users (username, password, role, nama, guru_id) VALUES (?,?,?,?,?)",
               ('supriyadi', hash_pw('guru123'), 'guru', 'Drs. Supriyadi, M.Pd', 1))

# CONTOH MURID
cursor.execute("SELECT id FROM kelas WHERE nama = 'X SIJA 1'")
kelas_id = cursor.fetchone()[0]
cursor.execute("INSERT INTO siswa (nama, kelas_id) VALUES (?,?)", ('Budi Santoso', kelas_id))
cursor.execute("INSERT INTO users (username, password, role, nama, siswa_id) VALUES (?,?,?,?,?)",
               ('budi', hash_pw('murid123'), 'murid', 'Budi Santoso', 1))

conn.commit()
conn.close()

print("✅ DATABASE BERHASIL!")
print("👑 ADMIN: penguasa / penguasaNEGA666")
print("👩‍🏫 GURU: supriyadi / guru123")
print("🧑‍🎓 MURID: budi / murid123")
