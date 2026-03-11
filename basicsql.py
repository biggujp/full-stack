import sqlite3

#สร้างการเชื่อมต่อกับฐานข้อมูล
conn =sqlite3.connect('tjdatabase.sqlite3')

#สร้าง cursor เพื่อใช้ในการดำเนินการกับฐานข้อมูล
c = conn.cursor()

#สร้างตารางในฐานข้อมูล
c.execute("""CREATE TABLE IF NOT EXISTS users
           (id INTEGER PRIMARY KEY AUTOINCREMENT, 
          name TEXT, 
          surname TEXT, 
          mobile TEXT, 
          email TEXT)""")    