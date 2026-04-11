
import sqlite3
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Render ላይ Error እንዳይመጣ ዳታቤዙን በMemory እንጠቀማለን
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
        body { font-family: sans-serif; background: #1a1a2e; color: white; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .box { background: #16213e; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); width: 90%; max-width: 400px; text-align: center; border: 1px solid #0f3460; }
        .step { display: none; }
        .active { display: block; }
        input, textarea { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #0f3460; border-radius: 8px; box-sizing: border-box; background: #1a1a2e; color: white; }
        .profile-img { width: 80px; height: 80px; border-radius: 50%; border: 3px solid #3498db; object-fit: cover; margin-bottom: 10px; }
        .btn-group { display: flex; justify-content: space-between; gap: 10px; margin-top: 15px; }
        button { padding: 12px 20px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
        .blue { background: #e94560; color: white; width: 100%; }
        .prev { background: #4e4e4e; color: white; }
        .next { background: #0f3460; color: white; border: 1px solid #3498db; }
        .save { background: #2ecc71; color: white; flex-grow: 1; }
        h2 { color: #3498db; margin-bottom: 5px; }
        p { font-size: 14px; color: #abb2bf; }
    </style>
</head>
<body><div class="box">{{content}}</div></body>
</html>
'''

@app.route('/')
def home():
    content = '<h2>@work.com</h2><p>የግል መረጃዎን በደህንነት ይደበቁ</p><a href="/register"><button class="blue">አዲስ ምዝገባ</button></a><a href="/login" style="display:block; margin-top:15px; color:#3498db; text-decoration:none;">መረጃን ለመደበቅ ግባ</a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', content))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name, s_id, code, pic = request.form.get('name'), request.form.get('student_id'), request.form.get('access_code'), request.form.get('profile_pic')
        try:
            db.execute("INSERT INTO students (name, student_id, access_code, profile_pic, step1, step2, step3, step4, step5, step6, step7) VALUES (?, ?, ?, ?, '', '', '', '', '', '', '')", (name, s_id, code, pic))
            db.commit()
            return 'ምዝገባ ተሳክቷል! <a href="/login" style="color:#3498db;">አሁን ግባ</a>'
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>አዲስ ምዝገባ</h2><form method="POST"><input name="name" placeholder="ሙሉ ስም" required><input name="student_id" placeholder="ID" required><input name="profile_pic" placeholder="የፎቶ ሊንክ (Profile URL)"><input name="access_code" type="password" placeholder="ሚስጥራዊ ኮድ" required><button class="blue">ተመዝገብ</button></form>'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        s_id, code = request.form.get('student_id'), request.form.get('access_code')
        user = db.execute("SELECT * FROM students WHERE student_id = ? AND access_code = ?", (s_id, code)).fetchone()
        if user:
            img_tag = f'<img src="{user["profile_pic"]}" class="profile-img" onerror="this.src=\'https://via.placeholder.com/80\'">'
            labels = ["የመጀመሪያ ሚስጥር", "የቤተሰብ መረጃ", "የገንዘብ ሁኔታ", "የጤና መረጃ", "የወደፊት እቅድ", "የግል ማስታወሻ", "ሌሎች"]
            steps_html = f'{img_tag}<h2>ሰላም {user["name"]}</h2><p>መረጃዎን እዚህ ይደበቁ</p><form action="/save/{user["student_id"]}" method="POST">'
            for i in range(1, 8):
                active_class = "active" if i == 1 else ""
                val = user[f"step{i}"] if user[f"step{i}"] else ""
                steps_html += f'''
                <div class="step {active_class}" id="step{i}">
                    <h3 style="color:#3498db; font-size:16px;">ደረጃ {i}: {labels[i-1]}</h3>
                    <textarea name="step{i}" placeholder="የሚደበቅ መረጃ እዚህ ይጻፉ...">{val}</textarea>
                    <div class="btn-group">
                        {"<button type='button' class='prev' onclick='move("+str(i)+","+str(i-1)+")'>Back</button>" if i > 1 else "<span></span>"}
                        {"<button type='button' class='next' onclick='move("+str(i)+","+str(i+1)+")'>Next</button>" if i < 7 else "<button type='submit' class='save'>ሁሉንም ደብቅ</button>"}
                    </div>
                </div>'''
            steps_html += '</form><script>function move(n,x){document.getElementById("step"+n).classList.remove("active");document.getElementById("step"+x).classList.add("active");}</script>'
            return render_template_string(HTML_LAYOUT.replace('{{content}}', steps_html))
        return 'የተሳሳተ መረጃ! <a href="/login" style="color:#3498db;">ድጋሚ ሞክር</a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>ግባ</h2><form method="POST"><input name="student_id" placeholder="ID" required><input name="access_code" type="password" placeholder="Code" required><button class="blue">ግባ</button></form>'))

@app.route('/save/<s_id>', methods=['POST'])
def save(s_id):
    try:
        db.execute("UPDATE students SET step1=?, step2=?, step3=?, step4=?, step5=?, step6=?, step7=? WHERE student_id=?", 
                  (request.form.get('step1'), request.form.get('step2'), request.form.get('step3'), request.form.get('step4'), request.form.get('step5'), request.form.get('step6'), request.form.get('step7'), s_id))
        db.commit()
        return 'መረጃው በሚስጥር ተደብቋል! <a href="/" style="color:#3498db;">ተመለስ</a>'
    except Exception as e:
        return f"Save Error: {str(e)}"

if __name__ == '__main__':
    app.run()



