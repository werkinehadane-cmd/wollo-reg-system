
import sqlite3
import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Render ላይ ዳታቤዙን በMemory እንጠቀማለን (ለደህንነትና ለፍጥነት)
db = sqlite3.connect(':memory:', check_same_thread=False)
db.row_factory = sqlite3.Row

def init_db():
    db.execute('''CREATE TABLE IF NOT EXISTS students 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, student_id TEXT UNIQUE, 
                  access_code TEXT, profile_pic TEXT, step1 TEXT, step2 TEXT, step3 TEXT, 
                  step4 TEXT, step5 TEXT, step6 TEXT, step7 TEXT)''')
    db.commit()

init_db()

HTML_LAYOUT = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #f4f7f6; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .box { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 95%; max-width: 450px; text-align: center; }
        .step { display: none; }
        .active { display: block; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        textarea { width: 100%; height: 100px; border: none; outline: none; font-size: 14px; resize: none; }
        .profile-img { width: 90px; height: 90px; border-radius: 50%; object-fit: cover; border: 3px solid #3498db; margin-bottom: 10px; }
        .btn-group { display: flex; justify-content: space-between; gap: 10px; margin-top: 15px; }
        button { padding: 12px 20px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
        .blue { background: #3498db; color: white; width: 100%; }
        .prev { background: #bdc3c7; color: white; }
        .next { background: #3498db; color: white; }
        .save { background: #2ecc71; color: white; flex-grow: 1; }
        h2 { color: #2c3e50; margin-bottom: 5px; }
    </style>
</head>
<body><div class="box">{{content}}</div></body>
</html>
'''

@app.route('/')
def home():
    content = '<h2>@work.com</h2><p>የግል መረጃን ለመደበቅ</p><a href="/register"><button class="blue">አዲስ ምዝገባ</button></a><a href="/login" style="display:block; margin-top:15px; color:#3498db; text-decoration:none;">መረጃ ለማውጣት ግባ</a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', content))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name, s_id, code = request.form.get('name'), request.form.get('student_id'), request.form.get('access_code')
        # ለጊዜው ፋይል ሰርቨር ስለሌለን የፎቶውን ስም ብቻ እንይዛለን
        pic = request.files.get('profile_pic').filename if request.files.get('profile_pic') else ""
        try:
            db.execute("INSERT INTO students (name, student_id, access_code, profile_pic, step1, step2, step3, step4, step5, step6, step7) VALUES (?, ?, ?, ?, '', '', '', '', '', '', '')", (name, s_id, code, pic))
            db.commit()
            return 'ምዝገባ ተሳክቷል! <a href="/login">አሁን ግባ</a>'
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>አዲስ ምዝገባ</h2><form method="POST" enctype="multipart/form-data"><input name="name" placeholder="ሙሉ ስም" required style="width:100%; padding:10px; margin:5px 0;"><input name="student_id" placeholder="መለያ ID" required style="width:100%; padding:10px; margin:5px 0;"><label style="display:block; text-align:left; font-size:12px;">መለያ ፎቶ ምረጥ፡</label><input type="file" name="profile_pic" accept="image/*" style="width:100%; margin:5px 0;"><input name="access_code" type="password" placeholder="ሚስጥራዊ ኮድ" required style="width:100%; padding:10px; margin:5px 0;"><button class="blue">ተመዝገብ</button></form>'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        s_id, code = request.form.get('student_id'), request.form.get('access_code')
        user = db.execute("SELECT * FROM students WHERE student_id = ? AND access_code = ?", (s_id, code)).fetchone()
        if user:
            labels = ["የህይወት ታሪክ", "የወደፊት እቅድ", "የቤተሰብ ሚስጥር", "የገንዘብ ሁኔታ", "የጤና ታሪክ", "የግል ማስታወሻ", "ተጨማሪ መረጃ"]
            steps_html = f'<h2>ሰላም {user["name"]}</h2><form action="/save/{user["student_id"]}" method="POST">'
            for i in range(1, 8):
                active_class = "active" if i == 1 else ""
                val = user[f"step{i}"] if user[f"step{i}"] else ""
                steps_html += f'''
                <div class="step {active_class}" id="step{i}">
                    <table>
                        <tr><td style="background:#f9f9f9; font-weight:bold;">ክፍል {i}: {labels[i-1]}</td></tr>
                        <tr><td><textarea name="step{i}" placeholder="{labels[i-1]} እዚህ ይደበቁ...">{val}</textarea></td></tr>
                    </table>
                    <div class="btn-group">
                        {"<button type='button' class='prev' onclick='move("+str(i)+","+str(i-1)+")'>Back</button>" if i > 1 else "<span></span>"}
                        {"<button type='button' class='next' onclick='move("+str(i)+","+str(i+1)+")'>Next</button>" if i < 7 else "<button type='submit' class='save'>ሁሉንም ደብቅ</button>"}
                    </div>
                </div>'''
            steps_html += '</form><script>function move(n,x){document.getElementById("step"+n).classList.remove("active");document.getElementById("step"+x).classList.add("active");}</script>'
            return render_template_string(HTML_LAYOUT.replace('{{content}}', steps_html))
        return 'የተሳሳተ መረጃ! <a href="/login">ድጋሚ ሞክር</a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>ግባ</h2><form method="POST"><input name="student_id" placeholder="መለያ ID" required style="width:100%; padding:10px; margin:5px 0;"><input name="access_code" type="password" placeholder="ሚስጥራዊ ኮድ" required style="width:100%; padding:10px; margin:5px 0;"><button class="blue">ግባ</button></form>'))

@app.route('/save/<s_id>', methods=['POST'])
def save(s_id):
    try:
        db.execute("UPDATE students SET step1=?, step2=?, step3=?, step4=?, step5=?, step6=?, step7=? WHERE student_id=?", 
                  (request.form.get('step1'), request.form.get('step2'), request.form.get('step3'), request.form.get('step4'), request.form.get('step5'), request.form.get('step6'), request.form.get('step7'), s_id))
        db.commit()
        return 'መረጃው በሚስጥር ተደብቋል! <a href="/">ተመለስ</a>'
    except Exception as e:
        return f"Save Error: {str(e)}"

if __name__ == '__main__':
    app.run()



