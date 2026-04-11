
import sqlite3
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('wollo_full_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, student_id TEXT UNIQUE, 
                  access_code TEXT, step1 TEXT, step2 TEXT, step3 TEXT, step4 TEXT, step5 TEXT, step6 TEXT, step7 TEXT)''')
    conn.commit()
    conn.close()

HTML_LAYOUT = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #f4f7f6; padding: 20px; }
        .container { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); max-width: 500px; margin: auto; }
        .step { display: none; }
        .active { display: block; }
        input, textarea { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .btn-next { background: #007bff; color: white; }
        .btn-prev { background: #6c757d; color: white; }
        .btn-save { background: #28a745; color: white; width: 100%; }
    </style>
</head>
<body><div class="container">{{content}}</div></body>
</html>
'''

@app.route('/')
def home():
    content = '<h2>ወሎ ዩኒቨርሲቲ</h2><a href="/register"><button class="btn-next" style="width:100%">አዲስ ተማሪ ምዝገባ</button></a><br><a href="/login"><button class="btn-next" style="width:100%; background:#28a745;">መረጃ ለመሙላት ግባ (Login)</button></a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', content))

@app.route('/admin_wollo')
def admin():
    conn = sqlite3.connect('wollo_full_system.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM students")
    total = c.fetchone()[0]
    conn.close()
    return f"<h2>ጠቅላላ ተመዝጋቢ ተማሪዎች፡ {total}</h2><a href='/'>ተመለስ</a>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name, s_id, code = request.form.get('name'), request.form.get('student_id'), request.form.get('access_code')
        conn = sqlite3.connect('wollo_full_system.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO students (name, student_id, access_code) VALUES (?, ?, ?)", (name, s_id, code))
            conn.commit()
            return 'ምዝገባ ተሳክቷል! <a href="/login">ግባ</a>'
        except: return 'ይህ ID ተመዝግቧል። <a href="/register">ተመለስ</a>'
        finally: conn.close()
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>አዲስ ምዝገባ</h2><form method="POST"><input name="name" placeholder="ሙሉ ስም" required><input name="student_id" placeholder="ID" required><input name="access_code" placeholder="Code" required><button class="btn-next">ተመዝገብ</button></form>'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        s_id, code = request.form.get('student_id'), request.form.get('access_code')
        conn = sqlite3.connect('wollo_full_system.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE student_id = ? AND access_code = ?", (s_id, code))
        user = c.fetchone()
        conn.close()
        if user:
            steps_html = f'<h2>ሰላም {user[1]}</h2><form id="multiStepForm">'
            for i in range(1, 8):
                active_class = "active" if i == 1 else ""
                steps_html += f'''<div class="step {active_class}" id="step{i}">
                    <h3>ደረጃ {i}</h3>
                    <textarea name="s{i}" placeholder="መረጃ እዚህ ይጻፉ..."></textarea>
                    {"<button type='button' class='btn-prev' onclick='prevStep("+str(i)+")'>Back</button>" if i > 1 else ""}
                    {"<button type='button' class='btn-next' onclick='nextStep("+str(i)+")'>Next</button>" if i < 7 else "<button type='submit' class='btn-save'>ሁሉንም መረጃ መዝግብ</button>"}
                </div>'''
            steps_html += '</form><script>function nextStep(s){document.getElementById("step"+s).classList.remove("active");document.getElementById("step"+(s+1)).classList.add("active");} function prevStep(s){document.getElementById("step"+s).classList.remove("active");document.getElementById("step"+(s-1)).classList.add("active");}</script>'
            return render_template_string(HTML_LAYOUT.replace('{{content}}', steps_html))
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>ግባ</h2><form method="POST"><input name="student_id" placeholder="ID"><input name="access_code" type="password" placeholder="Code"><button class="btn-next">ግባ</button></form>'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

