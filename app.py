import sqlite3
import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'permanent_data.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS students 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, student_id TEXT UNIQUE, 
                  access_code TEXT, profile_pic TEXT, step1 TEXT, step2 TEXT, step3 TEXT, 
                  step4 TEXT, step5 TEXT, step6 TEXT, step7 TEXT)''')
    conn.row_factory = sqlite3.Row
    return conn

HTML_LAYOUT = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #f0f2f5; margin: 0; padding: 15px; display: flex; justify-content: center; }
        .box { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 100%; max-width: 450px; text-align: center; }
        .step { display: none; }
        .active { display: block; }
        
        .info-header { text-align: left; font-weight: bold; margin-bottom: 8px; color: #1a73e8; font-size: 16px; }
        
        /* የሠንጠረዥ ዲዛይን - ገደብ የሌለው ቁመት */
        .table-style { width: 100%; border-collapse: collapse; margin-bottom: 15px; border: 2.5px solid #000; }
        .table-style td { padding: 0; vertical-align: top; }
        
        /* የኖት ዲዛይን - ገደብ የሌለው ቁመት */
        .note-style { width: 100%; min-height: 150px; border: 1px solid #ccc; border-radius: 8px; padding: 12px; font-size: 15px; resize: none; outline: none; background: #fffbe6; box-sizing: border-box; margin-bottom: 15px; overflow: hidden; }

        textarea.auto-grow { width: 100%; min-height: 150px; border: none; padding: 10px; box-sizing: border-box; font-size: 15px; resize: none; outline: none; background: transparent; overflow: hidden; display: block; }
        
        .btn-container { display: flex; justify-content: space-between; gap: 10px; margin-top: 15px; }
        button { padding: 12px; border-radius: 6px; border: 1px solid #ccc; cursor: pointer; font-weight: bold; }
        .main-btn { background: #1a73e8; color: white; width: 100%; border: none; }
        .nav-btn { background: #f8f9fa; color: #333; flex: 1; }
        .save-btn { background: #28a745; color: white; flex: 2; border: none; }
        
        input { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }
    </style>
</head>
<body><div class="box">{{content}}</div>
<script>
    // ጽሁፍ ሲበዛ ቁመቱ በራሱ እንዲጨምር የሚያደርግ ፋንክሽን
    function autoGrow(element) {
        element.style.height = "5px";
        element.style.height = (element.scrollHeight) + "px";
    }
    
    // ገጹ ሲከፈት ያሉትን ጽሁፎች አይቶ ቁመታቸውን ያስተካክላል
    window.onload = function() {
        document.querySelectorAll('textarea').forEach(el => {
            autoGrow(el);
            el.addEventListener('input', function() { autoGrow(this); });
        });
    };
</script>
</body>
</html>
'''

@app.route('/')
def home():
    content = '<h2>@work.com</h2><p>የግል መረጃ መደበቂያ</p><a href="/register"><button class="main-btn">አዲስ ምዝገባ</button></a><a href="/login" style="display:block; margin-top:15px; color:#1a73e8; text-decoration:none;">መረጃ ለማስገባት ግባ</a>'
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
            return 'ተመዝግበዋል! <a href="/login">አሁን ይግቡ</a>'
        except: return 'IDው ተይዟል! <a href="/register">ድጋሚ ሞክር</a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>@work.com ምዝገባ</h2><form method="POST"><input name="name" placeholder="ሙሉ ስም" required><input name="student_id" placeholder="መለያ ID" required><input name="access_code" type="password" placeholder="ሚስጥራዊ ኮድ" required><button class="main-btn">ተመዝገብ</button></form>'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        s_id, code = request.form.get('student_id'), request.form.get('access_code')
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM students WHERE student_id = ? AND access_code = ?", (s_id, code)).fetchone()
        conn.close()
        if user:
            titles = ["የህይወት ታሪክ", "የወደፊት እቅድ", "ደረጃ 3", "ደረጃ 4", "ደረጃ 5", "ደረጃ 6", "ደረጃ 7"]
            steps_html = f'<h3>@work.com - ሰላም {user["name"]}</h3><form action="/save/{user["student_id"]}" method="POST">'
            for i in range(1, 8):
                active = "active" if i == 1 else ""
                if i <= 2:
                    content_field = f'<textarea class="note-style auto-grow" name="step{i}" placeholder="{titles[i-1]} እዚህ ይጻፉ..." oninput="autoGrow(this)">{user[f"step{i}"]}</textarea>'
                else:
                    content_field = f'<table class="table-style"><tr><td><textarea class="auto-grow" name="step{i}" placeholder="መረጃውን እዚህ ይጻፉ..." oninput="autoGrow(this)">{user[f"step{i}"]}</textarea></td></tr></table>'
                
                steps_html += f'''
                <div class="step {active}" id="step{i}">
                    <div class="info-header">{titles[i-1]}</div>
                    {content_field}
                    <div class="btn-container">
                        {"<button type='button' class='nav-btn' onclick='move("+str(i)+","+str(i-1)+")'>Back</button>" if i > 1 else "<span></span>"}
                        {"<button type='button' class='nav-btn' onclick='move("+str(i)+","+str(i+1)+")'>Next</button>" if i < 7 else "<button type='submit' class='save-btn'>አስቀምጥ</button>"}
                    </div>
                </div>'''
            steps_html += '</form><script>function move(n,x){document.getElementById("step"+n).classList.remove("active");document.getElementById("step"+x).classList.add("active"); window.scrollTo(0,0);}</script>'
            return render_template_string(HTML_LAYOUT.replace('{{content}}', steps_html))
        return 'ID ወይም ኮድ ተሳስቷል! <a href="/login">ድጋሚ ሞክር</a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>@work.com መግቢያ</h2><form method="POST"><input name="student_id" placeholder="ID" required><input name="access_code" type="password" placeholder="ኮድ" required><button class="main-btn">ግባ</button></form>'))

@app.route('/save/<s_id>', methods=['POST'])
def save(s_id):
    conn = get_db_connection()
    conn.execute("UPDATE students SET step1=?, step2=?, step3=?, step4=?, step5=?, step6=?, step7=? WHERE student_id=?", 
              (request.form.get('step1'), request.form.get('step2'), request.form.get('step3'), request.form.get('step4'), request.form.get('step5'), request.form.get('step6'), request.form.get('step7'), s_id))
    conn.commit()
    conn.close()
    return 'መረጃው በሚስጥር ተቀምጧል! <a href="/">ተመለስ</a>'

if __name__ == '__main__':
    app.run()




