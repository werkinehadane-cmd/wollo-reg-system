
import sqlite3
import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Render ላይ ዳታቤዙን በትክክል እንዲያገኘው
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'student_personal_data.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS students 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, student_id TEXT UNIQUE, 
                  access_code TEXT, step1 TEXT, step2 TEXT, step3 TEXT, 
                  step4 TEXT, step5 TEXT, step6 TEXT, step7 TEXT)''')
    return conn

HTML_LAYOUT = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .box { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 90%; max-width: 380px; text-align: center; }
        input, textarea { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; margin-top: 10px; }
        .blue { background: #3498db; color: white; }
        .green { background: #2ecc71; color: white; }
    </style>
</head>
<body><div class="box">{{content}}</div></body>
</html>
'''

@app.route('/')
def home():
    content = '<h2>@work.com</h2><a href="/register"><button class="blue">አዲስ ምዝገባ</button></a><a href="/login"><button class="green">ፕሮፋይል ለማስገባት ግባ</button></a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', content))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name, s_id, code = request.form.get('name'), request.form.get('student_id'), request.form.get('access_code')
        try:
            conn = get_db_connection()
            conn.execute("INSERT INTO students (name, student_id, access_code, step1, step2, step3, step4, step5, step6, step7) VALUES (?, ?, ?, '', '', '', '', '', '', '')", (name, s_id, code))
            conn.commit()
            conn.close()
            return 'ምዝገባ ተሳክቷል! <a href="/login">አሁን ፕሮፋይል አስገባ</a>'
        except sqlite3.IntegrityError:
            return 'ስህተት፡ ይህ ID ተመዝግቧል። <a href="/register">ተመለስ</a>'
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>አዲስ ምዝገባ</h2><form method="POST"><input name="name" placeholder="ሙሉ ስም" required><input name="student_id" placeholder="ID" required><input name="access_code" placeholder="Password/Code" required><button class="blue">ተመዝገብ</button></form><a href="/">ተመለስ</a>'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        s_id, code = request.form.get('student_id'), request.form.get('access_code')
        try:
            conn = get_db_connection()
            user = conn.execute("SELECT * FROM students WHERE student_id = ? AND access_code = ?", (s_id, code)).fetchone()
            conn.close()
            if user:
                steps_html = f'<h2>ሰላም {user[1]}</h2><p>ፕሮፋይልህን እዚህ አስገባ</p><form action="/save/{user[2]}" method="POST">'
                labels = ["የግል መረጃ", "ትምህርት ደረጃ", "ልምድ", "ክህሎት", "ፍላጎት", "አድራሻ", "ተጨማሪ"]
                for i in range(1, 8):
                    steps_html += f'<textarea name="step{i}" placeholder="{labels[i-1]}">{user[i+3]}</textarea>'
                steps_html += '<button type="submit" class="green">ሁሉንም አስቀምጥ</button></form>'
                return render_template_string(HTML_LAYOUT.replace('{{content}}', steps_html))
            return 'የተሳሳተ መረጃ! <a href="/login">እንደገና ሞክር</a>'
        except Exception as e:
            return f"Login Error: {str(e)}"
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>ግባ</h2><form method="POST"><input name="student_id" placeholder="ID" required><input name="access_code" type="password" placeholder="Code" required><button class="blue">ግባ</button></form>'))

@app.route('/save/<s_id>', methods=['POST'])
def save(s_id):
    try:
        conn = get_db_connection()
        conn.execute("UPDATE students SET step1=?, step2=?, step3=?, step4=?, step5=?, step6=?, step7=? WHERE student_id=?", 
                  (request.form.get('step1'), request.form.get('step2'), request.form.get('step3'), request.form.get('step4'), request.form.get('step5'), request.form.get('step6'), request.form.get('step7'), s_id))
        conn.commit()
        conn.close()
        return 'መረጃው ተቀምጧል! <a href="/">ተመለስ</a>'
    except Exception as e:
        return f"Save Error: {str(e)}"

if __name__ == '__main__':
    app.run()



