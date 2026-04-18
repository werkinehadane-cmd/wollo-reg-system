
import os
import base64
from flask import Flask, render_template_string, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Connection
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
        .box { background: white; padding: 30px; border-radius: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; position: relative; }
        .step { display: none; }
        .active { display: block; }
        h2 { color: #333; margin-bottom: 10px; font-size: 28px; }
        input { width: 100%; padding: 15px; margin: 10px 0; border: 1px solid #eee; border-radius: 12px; background: #f9f9f9; box-sizing: border-box; font-size: 16px; }
        .file-label { display: block; background: #34495e; color: white; padding: 12px; border-radius: 10px; cursor: pointer; margin: 10px 0; font-size: 14px; }
        .profile-img { width: 90px; height: 90px; border-radius: 50%; object-fit: cover; border: 3px solid #1a73e8; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .main-btn { background: #1a73e8; color: white; width: 100%; padding: 15px; border: none; border-radius: 12px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 15px; }
        .info-header { text-align: left; font-weight: bold; margin-bottom: 10px; color: #1a73e8; font-size: 18px; }
        .note-style { width: 100%; min-height: 200px; border: 1px solid #eee; border-radius: 15px; padding: 10px; background: #fffbe6; box-shadow: inset 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 15px; }
        textarea.auto-grow { width: 100%; min-height: 180px; border: none; padding: 5px; box-sizing: border-box; font-size: 16px; resize: none; outline: none; background: transparent; font-family: inherit; }
        .btn-container { display: flex; justify-content: space-between; gap: 10px; margin-top: 15px; }
        .nav-btn { background: #f1f3f4; color: #3c4043; flex: 1; padding: 12px; border-radius: 10px; border: none; font-weight: bold; cursor: pointer; }
        .save-btn { background: #27ae60; color: white; flex: 2; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; }
        
        .admin-link { position: absolute; bottom: 15px; right: 20px; font-size: 14px; color: #1a73e8; text-decoration: none; font-weight: bold; background: #e8f0fe; padding: 5px 10px; border-radius: 10px; }
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
    count = students_col.count_documents({})
    # እዚህ ጋር ትክክለኛውን የዩኒቨርሲቲውን የሎጎ ሊንክ አስገባ
    logo_url = "https://www.wollo.edu.et/path/to/logo.png"
    img_html = f'<img src="{logo_url}" class="profile-img" style="display: block; margin: 0 auto 15px;">'
    
    content = f'''
    {img_html}
    <h2>@work.com</h2>
    <p style="color:#666; margin-bottom: 20px;">የግል መረጃ መደበቂያ</p>
    <a href="/register" style="text-decoration:none;"><button class="main-btn">አዲስ ምዝገባ</button></a>
    <a href="/login" style="display:block; margin-top:20px; color:#1a73e8; text-decoration:none; font-weight:bold;">መረጃ ለማስገባት ግባ</a>
    <a href="/admin_login" class="admin-link">ተጠቃሚዎች: {count}</a>
    '''
    return render_template_string(HTML_LAYOUT.replace('{{content}}', content))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name, s_id, code = request.form.get('name'), request.form.get('student_id'), request.form.get('access_code')
        photo = request.files.get('profile_photo')
        photo_data = ""
        if photo:
            photo_data = "data:image/jpeg;base64," + base64.b64encode(photo.read()).decode('utf-8')

        if students_col.find_one({"student_id": s_id}):
            return 'IDው ተይዟል! <a href="/register">ተመለስ</a>'
            
        students_col.insert_one({"name": name, "student_id": s_id, "access_code": code, "photo": photo_data, "step1":"", "step2":"", "step3":"", "step4":"", "step5":"", "step6":"", "step7":""})
        return redirect(url_for('login'))
        
    content = '''<h2>አዲስ ምዝገባ</h2><form method="POST" enctype="multipart/form-data"><input name="name" placeholder="ሙሉ ስም" required><input name="student_id" placeholder="ID" required><input name="access_code" type="password" placeholder="ሚስጥር ኮድ" required><label class="file-label">የፕሮፋይል ፎቶ ምረጥ<input type="file" name="profile_photo" accept="image/*" style="display:none;"></label><button class="main-btn">ተመዝገብ</button></form>'''
    return render_template_string(HTML_LAYOUT.replace('{{content}}', content))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        s_id, code = request.form.get('student_id'), request.form.get('access_code')
        user = students_col.find_one({"student_id": s_id, "access_code": code})
        if user:
            img = f'<img src="{user.get("photo", "")}" class="profile-img">' if user.get("photo") else ""
            titles = ["የገቢና ወጭ መመዝገቢያ", "የህይወት ታሪክ", "በህይወት ስንኖር ገጠመኝ", "የተማርናቸው ኮርስና የመምህሩ ስም እና GPA", "የጓደኛ ሚስጢር መመዝገቢያ", "የሀገርና ሃይማኖታዊ ታሪክ መመዝገቢያ", "የንግድ / ገንዘብ ነክ ስራ ማስታወሻ"]
            steps_html = f'{img}<h3 style="margin-top:5px;">ሰላም {user["name"]}</h3><form action="/save/{user["student_id"]}" method="POST">'
            for i in range(1, 8):
                active = "active" if i == 1 else ""
                val = user.get(f"step{i}", "")
                field = f'<div class="note-style"><textarea class="auto-grow" name="step{i}" oninput="autoGrow(this)" placeholder="እዚህ ጋር ይጻፉ...">{val}</textarea></div>'
                steps_html += f'''<div class="step {active}" id="step{i}"><div class="info-header">{titles[i-1]}</div>{field}<div class="btn-container">{"<button type='button' class='nav-btn' onclick='move("+str(i)+","+str(i-1)+")'>Back</button>" if i > 1 else "<span></span>"}{"<button type='button' class='nav-btn' onclick='move("+str(i)+","+str(i+1)+")'>Next</button>" if i < 7 else "<button type='submit' class='save-btn'>አስቀምጥ</button>"}</div></div>'''
            return render_template_string(HTML_LAYOUT.replace('{{content}}', steps_html + '</form>'))
        return 'ID ወይም ኮድ ተሳስተሃል! <a href="/login">ድጋሚ ሞክር</a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>መግቢያ</h2><form method="POST"><input name="student_id" placeholder="ID" required><input name="access_code" type="password" placeholder="ኮድ" required><button class="main-btn">ግባ</button></form>'))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('pass') == "Admin123":
            users = list(students_col.find({}, {"name": 1, "student_id": 1}))
            user_list = "".join([f"<li style='margin-bottom:10px;'><b>{u['name']}</b> (ID: {u['student_id']})</li>" for u in users])
            return f'<div style="padding:20px; font-family:sans-serif;"><h2>ተጠቃሚዎች ({len(users)})</h2><ul>{user_list}</ul><a href="/" style="color:#1a73e8; font-weight:bold;">ተመለስ</a></div>'
        return 'ኮድ ተሳስተሃል!'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>Admin Access</h2><form method="POST"><input name="pass" type="password" placeholder="Admin Code"><button class="main-btn">ግባ</button></form>'))

@app.route('/save/<s_id>', methods=['POST'])
def save(s_id):
    update_data = {f"step{i}": request.form.get(f"step{i}") for i in range(1, 8)}
    students_col.update_one({"student_id": s_id}, {"$set": update_data})
    return 'መረጃው ተቀምጧል! <a href="/">ተመለስ</a>'

if __name__ == '__main__':
    app.run()





