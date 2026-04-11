
import sqlite3
import os
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# ዳታቤዙን መፍጠሪያ
def init_db():
    try:
        conn = sqlite3.connect('student_personal_data.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS students 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, student_id TEXT UNIQUE, 
                      access_code TEXT, step1 TEXT, step2 TEXT, step3 TEXT, 
                      step4 TEXT, step5 TEXT, step6 TEXT, step7 TEXT)''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database Error: {e}")

HTML_LAYOUT = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #eef2f3; padding: 15px; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .container { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 100%; max-width: 400px; }
        .step { display: none; }
        .active { display: block; }
        h2 { color: #2c3e50; text-align: center; margin-bottom: 20px; }
        input, textarea { width: 100%; padding: 14px; margin: 10px 0; border: 1px solid #cfd8dc; border-radius: 10px; box-sizing: border-box; font-size: 16px; outline: none; }
        input:focus { border-color: #3498db; }
        .btn-group { display: flex; justify-content: space-between; gap: 10px; margin-top: 15px; }
        button { padding: 12px 20px; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; transition: 0.3s; }
        .next { background: #3498db; color: white; width: 100%; }
        .next:hover { background: #2980b9; }
        .prev { background: #bdc3c7; color: white; }
        .save { background: #2ecc71; color: white; flex-grow: 1; }
        .link-btn { display: block; text-align: center; margin-top: 20px; color: #3498db; text-decoration: none; font-size: 15px; font-weight: 500; }
    </style>
</head>
<body><div class="container">{{content}}</div></body>
</html>
'''

@app.route('/')
def home():
    content = '''
    <h2 style="color: #3498db;">@work.stu.com</h2>
    <a href="/register"><button class="next">አዲስ ምዝገባ</button></a>
    <a href="/login" class="link-btn">የግል መረጃን ለማስቀመጥ ግባ</a>
    '''
    return render_template_string(HTML_LAYOUT.replace('{{content}}', content))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name, s_id, code = request.form.get('name'), request.form.get('student_id'), request.form.get('access_code')
        try:
            conn = sqlite3.connect('student_personal_data.db')
            c = conn.cursor()
            c.execute("INSERT INTO students (name, student_id, access_code, step1, step2, step3, step4, step5, step6, step7) VALUES (?, ?, ?, '', '', '', '', '', '', '')", (name, s_id, code))
            conn.commit()
            conn.close()
            return 'ምዝገባ ተሳክቷል! <a href="/login">ግባ</a>'
        except:
            return 'ስህተት፡ ይህ ID ተመዝግቧል። <a href="/register">ተመለስ</a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>አዲስ ምዝገባ</h2><form method="POST"><input name="name" placeholder="ሙሉ ስም" required><input name="student_id" placeholder="መታወቂያ (ID)" required><input name="access_code" placeholder="ሚስጥራዊ ኮድ" required><button class="next">ተመዝገብ</button></form><a href="/" class="link-btn">ተመለስ</a>'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        s_id, code = request.form.get('student_id'), request.form.get('access_code')
        conn = sqlite3.connect('student_personal_data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE student_id = ? AND access_code = ?", (s_id, code))
        user = c.fetchone()
        conn.close()
        if user:
            steps_html = f'<h2>ሰላም {user[1]}</h2><p style="text-align:center; color:gray; font-size:12px;">የግል መረጃዎን እዚህ ያስቀምጡ</p><form action="/save_data/{user[2]}" method="POST">'
            for i in range(1, 8):
                active_class = "active" if i == 1 else ""
                val = user[i+3] if user[i+3] else ""
                steps_html += f'''<div class="step {active_class}" id="step{i}">
                    <h3 style="font-size:16px;">ማህደር {i}</h3>
                    <textarea name="step{i}" rows="5" placeholder="መረጃ እዚህ ይጻፉ...">{val}</textarea>
                    <div class="btn-group">
                        {"<button type='button' class='prev' onclick='move("+str(i)+","+str(i-1)+")'>Back</button>" if i > 1 else "<span></span>"}
                        {"<button type='button' class='next' onclick='move("+str(i)+","+str(i+1)+")' style='width:auto;'>ቀጣይ</button>" if i < 7 else "<button type='submit' class='save'>ሁሉንም አስቀምጥ</button>"}
                    </div>
                </div>'''
            steps_html += '</form><script>function move(n,x){document.getElementById("step"+n).classList.remove("active");document.getElementById("step"+x).classList.add("active");}</script>'
            return render_template_string(HTML_LAYOUT.replace('{{content}}', steps_html))
        return 'የተሳሳተ መረጃ። <a href="/login">እንደገና ሞክር</a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>ግባ</h2><form method="POST"><input name="student_id" placeholder="ID"><input name="access_code" type="password" placeholder="Code"><button class="next">ግባ</button></form><a href="/" class="link-btn">ተመለስ</a>'))

@app.route('/save_data/<s_id>', methods=['POST'])
def save_data(s_id):
    conn = sqlite3.connect('student_personal_data.db')
    c = conn.cursor()
    c.execute("UPDATE students SET step1=?, step2=?, step3=?, step4=?, step5=?, step6=?, step7=? WHERE student_id=?", 
              (request.form.get('step1'), request.form.get('step2'), request.form.get('step3'), request.form.get('step4'), request.form.get('step5'), request.form.get('step6'), request.form.get('step7'), s_id))
    conn.commit()
    conn.close()
    return 'መረጃው በሚስጥር ተቀምጧል! <a href="/">ወደ ዋና ገጽ</a>'

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


