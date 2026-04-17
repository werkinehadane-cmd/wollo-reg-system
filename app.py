
import os
from flask import Flask, render_template_string, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# --- MONGO_URI እዚህ ጋር በትክክል ማስገባትህን አረጋግጥ ---
MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['work_dot_com_db']
students_col = db['students']
HTML_LAYOUT = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .box { background: white; padding: 30px; border-radius: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
        .step { display: none; }
        .active { display: block; }
        
        h2 { color: #333; margin-bottom: 25px; font-size: 28px; }
        input { width: 100%; padding: 15px; margin: 10px 0; border: 1px solid #eee; border-radius: 12px; background: #f9f9f9; box-sizing: border-box; font-size: 16px; }
        
        .main-btn { background: #1a73e8; color: white; width: 100%; padding: 15px; border: none; border-radius: 12px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 15px; }
        
        /* የሠንጠረዥ እና የኖት ዲዛይን */
        .info-header { text-align: left; font-weight: bold; margin-bottom: 10px; color: #1a73e8; }
        .table-style { width: 100%; border-collapse: collapse; margin-bottom: 15px; border: 2.5px solid #000; }
        .table-style td { padding: 0; vertical-align: top; }
        .note-style { width: 100%; min-height: 150px; border: 1px solid #ccc; border-radius: 12px; padding: 15px; background: #fffbe6; box-sizing: border-box; margin-bottom: 15px; font-size: 16px; }
        textarea.auto-grow { width: 100%; min-height: 150px; border: none; padding: 10px; box-sizing: border-box; font-size: 16px; resize: none; outline: none; background: transparent; }

        .btn-container { display: flex; justify-content: space-between; gap: 10px; margin-top: 15px; }
        .nav-btn { background: #f1f3f4; color: #3c4043; flex: 1; padding: 12px; border-radius: 10px; border: none; font-weight: bold; cursor: pointer; }
        .save-btn { background: #27ae60; color: white; flex: 2; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="box">{{content}}</div>
    <script>
        function autoGrow(element) {
            element.style.height = "5px";
            element.style.height = (element.scrollHeight) + "px";
        }
        function move(n, x) {
            document.getElementById("step" + n).classList.remove("active");
            document.getElementById("step" + x).classList.add("active");
            window.scrollTo(0, 0);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    content = '<h2>@work.com</h2><p style="color:666;">የግል መረጃ መደበቂያ</p><a href="/register" style="text-decoration:none;"><button class="main-btn">አዲስ ምዝገባ</button></a><a href="/login" style="display:block; margin-top:20px; color:#1a73e8; text-decoration:none; font-weight:bold;">መረጃ ለማስገባት ግባ</a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', content))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name, s_id, code = request.form.get('name'), request.form.get('student_id'), request.form.get('access_code')
        if students_col.find_one({"student_id": s_id}):
            return 'IDው ተይዟል! <a href="/register">ተመለስ</a>'
        students_col.insert_one({"name": name, "student_id": s_id, "access_code": code, "step1":"", "step2":"", "step3":"", "step4":"", "step5":"", "step6":"", "step7":""})
        return redirect(url_for('login'))
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>አዲስ ምዝገባ</h2><form method="POST"><input name="name" placeholder="ሙሉ ስም" required><input name="student_id" placeholder="ID" required><input name="access_code" type="password" placeholder="ኮድ" required><button class="main-btn">ተመዝገብ</button></form>'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        s_id, code = request.form.get('student_id'), request.form.get('access_code')
        user = students_col.find_one({"student_id": s_id, "access_code": code})
        if user:
            titles = ["የህይወት ታሪክ", "የወደፊት እቅድ", "ደረጃ 3", "ደረጃ 4", "ደረጃ 5", "ደረጃ 6", "ደረጃ 7"]
            steps_html = f'<h3 style="margin-bottom:20px;">ሰላም {user["name"]}</h3><form action="/save/{user["student_id"]}" method="POST">'
            for i in range(1, 8):
                active = "active" if i == 1 else ""
                val = user.get(f"step{i}", "")
                field = f'<textarea class="note-style auto-grow" name="step{i}" oninput="autoGrow(this)">{val}</textarea>' if i <= 2 else f'<table class="table-style"><tr><td><textarea class="auto-grow" name="step{i}" oninput="autoGrow(this)">{val}</textarea></td></tr></table>'
                steps_html += f'<div class="step {active}" id="step{i}"><div class="info-header">{titles[i-1]}</div>{field}<div class="btn-container">{"<button type=\'button\' class=\'nav-btn\' onclick=\'move("+str(i)+","+str(i-1)+")\'>Back</button>" if i > 1 else "<span></span>"}{"<button type=\'button\' class=\'nav-btn\' onclick=\'move("+str(i)+","+str(i+1)+")\'>Next</button>" if i < 7 else "<button type=\'submit\' class=\'save-btn\'>አስቀምጥ</button>"}</div></div>'
            return render_template_string(HTML_LAYOUT.replace('{{content}}', steps_html + '</form>'))
        return 'ስህተት! <a href="/login">ድጋሚ ሞክር</a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>መግቢያ</h2><form method="POST"><input name="student_id" placeholder="ID" required><input name="access_code" type="password" placeholder="ኮድ" required><button class="main-btn">ግባ</button></form>'))

@app.route('/save/<s_id>', methods=['POST'])
def save(s_id):
    update_data = {f"step{i}": request.form.get(f"step{i}") for i in range(1, 8)}
    students_col.update_one({"student_id": s_id}, {"$set": update_data})
    return 'መረጃው በሚስጥር ተቀምጧል! <a href="/">ተመለስ</a>'

if __name__ == '__main__':
    app.run()




