import sqlite3
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# ዳታቤዙን በትክክል መፍጠሪያ
def init_db():
    conn = sqlite3.connect('wollo_full_final.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, student_id TEXT UNIQUE, 
                  access_code TEXT, step1 TEXT, step2 TEXT, step3 TEXT, 
                  step4 TEXT, step5 TEXT, step6 TEXT, step7 TEXT)''')
    conn.commit()
    conn.close()

HTML_LAYOUT = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #f0f2f5; padding: 15px; }
        .container { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 500px; margin: auto; }
        .step { display: none; }
        .active { display: block; }
        input, textarea { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
        .btn-group { display: flex; justify-content: space-between; }
        button { padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
        .next { background: #1a73e8; color: white; }
        .prev { background: #6c757d; color: white; }
        .save { background: #28a745; color: white; width: 100%; margin-top: 10px; }
    </style>
</head>
<body><div class="container">{{content}}</div></body>
</html>
'''

@app.route('/')
def home():
    content = '<h2>ወሎ ዩኒቨርሲቲ</h2><a href="/register"><button class="next" style="width:100%">አዲስ ምዝገባ</button></a><br><a href="/login"><button class="save">መረጃ ለመሙላት/ለማስተካከል ግባ</button></a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', content))

# --- ተማሪዎችን መቁጠሪያ (ለቢንያም ብቻ) ---
@app.route('/admin_wollo')
def admin():
    conn = sqlite3.connect('wollo_full_final.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM students")
    total = c.fetchone()[0]
    conn.close()
    return f"<div style='text-align:center;'><h2>ጠቅላላ የተመዘገቡ ተማሪዎች፡ {total}</h2><a href='/'>ተመለስ</a></div>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name, s_id, code = request.form.get('name'), request.form.get('student_id'), request.form.get('access_code')
        conn = sqlite3.connect('wollo_full_final.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO students (name, student_id, access_code) VALUES (?, ?, ?)", (name, s_id, code))
            conn.commit()
            return 'ምዝገባ ተሳክቷል! <a href="/login">ለመግባት እዚህ ይጫኑ</a>'
        except: return 'ይህ ID ተመዝግቧል። <a href="/register">ተመለስ</a>'
        finally: conn.close()
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>አዲስ ምዝገባ</h2><form method="POST"><input name="name" placeholder="ሙሉ ስም" required><input name="student_id" placeholder="ID" required><input name="access_code" placeholder="Code" required><button class="next">ተመዝገብ</button></form>'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        s_id, code = request.form.get('student_id'), request.form.get('access_code')
        conn = sqlite3.connect('wollo_full_final.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE student_id = ? AND access_code = ?", (s_id, code))
        user = c.fetchone()
        conn.close()
        if user:
            steps_html = f'<h2>ሰላም {user[1]}</h2><form action="/save_data/{user[2]}" method="POST">'
            for i in range(1, 8):
                active_class = "active" if i == 1 else ""
                val = user[i+3] if user[i+3] else ""
                steps_html += f'''<div class="step {active_class}" id="step{i}">
                    <h3>ደረጃ {i}</h3>
                    <textarea name="step{i}" placeholder="ደረጃ {i} መረጃ...">{val}</textarea>
                    <div class="btn-group">
                        {"<button type='button' class='prev' onclick='move("+str(i)+","+str(i-1)+")'>Back</button>" if i > 1 else "<span></span>"}
                        {"<button type='button' class='next' onclick='move("+str(i)+","+str(i+1)+")'>Next</button>" if i < 7 else "<button type='submit' class='save'>ሁሉንም መረጃ መዝግብ</button>"}
                    </div>
                </div>'''
            steps_html += '</form><script>function move(n,x){document.getElementById("step"+n).classList.remove("active");document.getElementById("step"+x).classList.add("active");}</script>'
            return render_template_string(HTML_LAYOUT.replace('{{content}}', steps_html))
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>ግባ</h2><form method="POST"><input name="student_id" placeholder="ID"><input name="access_code" type="password" placeholder="Code"><button class="next">ግባ</button></form>'))

@app.route('/save_data/<s_id>', methods=['POST'])
def save_data(s_id):
    conn = sqlite3.connect('wollo_full_final.db')
    c = conn.cursor()
    c.execute("UPDATE students SET step1=?, step2=?, step3=?, step4=?, step5=?, step6=?, step7=? WHERE student_id=?", 
              (request.form.get('step1'), request.form.get('step2'), request.form.get('step3'), request.form.get('step4'), request.form.get('step5'), request.form.get('step6'), request.form.get('step7'), s_id))
    conn.commit()
    conn.close()
    return 'መረጃው በትክክል ተቀምጧል! <a href="/">ተመለስ</a>'

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


