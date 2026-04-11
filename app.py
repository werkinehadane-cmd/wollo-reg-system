
import os
from flask import Flask, render_template_string, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# --- እዚህ ጋር የራስህን MongoDB ሊንክ አስገባ ---
MONGO_URI = "የአንተን_የሞንጎ_ዲቢ_ሊንክ_እዚህ_ጋር_ለጥፍ" 
client = MongoClient(MONGO_URI)
db = client['work_dot_com_v2']
students_col = db['students']

HTML_LAYOUT = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f4f7f6; margin: 0; padding: 15px; display: flex; justify-content: center; }
        .box { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 100%; max-width: 450px; text-align: center; }
        .step { display: none; }
        .active { display: block; }
        
        h2 { color: #333; margin-bottom: 20px; }
        .profile-img { width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 3px solid #1a73e8; margin-bottom: 10px; }
        
        /* አንተ የፈለግከው የሰንጠረዥ ዲዛይን */
        .info-title { text-align: left; font-weight: bold; color: #1a73e8; margin: 15px 0 5px 0; }
        .data-table { width: 100%; border-collapse: collapse; border: 2px solid #000; margin-bottom: 15px; }
        .data-table td { border: 1px solid #000; padding: 0; }
        textarea { width: 100%; min-height: 120px; border: none; padding: 10px; font-size: 15px; resize: none; outline: none; background: transparent; display: block; }

        .btn { width: 100%; padding: 14px; border-radius: 10px; border: none; font-weight: bold; cursor: pointer; transition: 0.3s; margin-top: 10px; }
        .blue-btn { background: #1a73e8; color: white; }
        .green-btn { background: #2ecc71; color: white; }
        .nav-btn { background: #ecf0f1; color: #333; flex: 1; }
        
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
    </style>
</head>
<body><div class="box">{{content}}</div>
<script>
    function autoGrow(el) { el.style.height = "5px"; el.style.height = (el.scrollHeight) + "px"; }
    window.onload = function() { document.querySelectorAll('textarea').forEach(el => { autoGrow(el); el.addEventListener('input', function() { autoGrow(this); }); }); };
</script>
</body>
</html>
'''

@app.route('/')
def home():
    content = '<h2>@work.com</h2><p>የግል መረጃ መደበቂያ</p><a href="/register"><button class="btn blue-btn">አዲስ ምዝገባ</button></a><a href="/login"><button class="btn green-btn">መረጃ ለማየት ግባ</button></a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', content))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name, s_id, code = request.form.get('name'), request.form.get('student_id'), request.form.get('access_code')
        pic = request.form.get('pic_url') # ለጊዜው የፎቶ ሊንክ፣ በኋላ ፋይል ማድረግ ይቻላል
        if students_col.find_one({"student_id": s_id}): return 'ID ተይዟል! <a href="/register">ተመለስ</a>'
        students_col.insert_one({"name":name, "student_id":s_id, "access_code":code, "pic":pic, "s1":"", "s2":"", "s3":"", "s4":"", "s5":"", "s6":"", "s7":""})
        return 'ተመዝግበዋል! <a href="/login">አሁን ይግቡ</a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>አዲስ ምዝገባ</h2><form method="POST"><input name="name" placeholder="ሙሉ ስም" required><input name="student_id" placeholder="ID" required><input name="access_code" type="password" placeholder="ኮድ" required><input name="pic_url" placeholder="የፎቶ ሊንክ (Profile Pic URL)"><button class="btn blue-btn">ተመዝገብ</button></form>'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        s_id, code = request.form.get('id'), request.form.get('code')
        user = students_col.find_one({"student_id": s_id, "access_code": code})
        if user:
            titles = ["የህይወት ታሪክ", "የትምህርት መረጃ", "የገንዘብ ሁኔታ", "የጤና መረጃ", "የወደፊት እቅድ", "የግል ማስታወሻ", "ሌሎች"]
            res = f'{"<img src="+user["pic"]+" class=\"profile-img\">" if user.get("pic") else ""}<h3>ሰላም {user["name"]}</h3><form action="/save/'+s_id+'" method="POST">'
            for i in range(1, 8):
                active = "active" if i == 1 else ""
                res += f'<div class="step {active}" id="s{i}"><div class="info-title">{titles[i-1]}</div><table class="data-table"><tr><td><textarea name="s{i}" oninput="autoGrow(this)">{user.get("s"+str(i),"")}</textarea></td></tr></table><div style="display:flex; gap:10px;">'
                if i>1: res += f'<button type="button" class="btn nav-btn" onclick="move({i},{i-1})">Back</button>'
                if i<7: res += f'<button type="button" class="btn blue-btn" onclick="move({i},{i+1})">Next</button>'
                else: res += f'<button type="submit" class="btn green-btn">ሁሉንም አስቀምጥ</button>'
                res += '</div></div>'
            res += '</form><script>function move(n,x){document.getElementById("s"+n).classList.remove("active");document.getElementById("s"+x).classList.add("active");}</script>'
            return render_template_string(HTML_LAYOUT.replace('{{content}}', res))
        return 'ስህተት! <a href="/login">ድጋሚ ሞክር</a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', '<h2>መግቢያ</h2><form method="POST"><input name="id" placeholder="ID" required><input name="code" type="password" placeholder="ኮድ" required><button class="btn blue-btn">ግባ</button></form>'))

@app.route('/save/<s_id>', methods=['POST'])
def save(s_id):
    data = {f"s{i}": request.form.get(f"s{i}") for i in range(1, 8)}
    students_col.update_one({"student_id": s_id}, {"$set": data})
    return 'መረጃው በሚስጥር ተቀምጧል! <a href="/">ተመለስ</a>'

@app.route('/admin')
def admin():
    count = students_col.count_documents({})
    return render_template_string(HTML_LAYOUT.replace('{{content}}', f'<h2>Admin Page</h2><div style="background:#e8f4fd; padding:30px; border-radius:15px;"><p>ጠቅላላ የተመዘገቡ ተማሪዎች</p><h1 style="font-size:60px; color:#1a73e8; margin:0;">{count}</h1></div><br><a href="/" class="btn nav-btn">ወደ ዋና ገጽ</a>'))

if __name__ == '__main__':
    app.run()




