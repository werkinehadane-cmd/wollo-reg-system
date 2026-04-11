import sqlite3
import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# ፎቶና ቪዲዮ የሚቀመጥበት ፎልደር መኖሩን ማረጋገጥ
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def init_db():
    conn = sqlite3.connect('wollo_final.db')
    c = conn.cursor()
    # 1. የተማሪዎች ዋና መረጃ (Profile & Step 1, 2, 5)
    c.execute('''CREATE TABLE IF NOT EXISTS students 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  first_name TEXT, last_name TEXT, grand_name TEXT, 
                  b_year TEXT, b_month TEXT, b_day TEXT, b_week_day TEXT,
                  nationality TEXT, region TEXT, kebele TEXT,
                  biography TEXT, photo TEXT, access_code TEXT, student_id TEXT UNIQUE)''')
    
    # 2. የገቢና ወጪ ሰንጠረዥ (Step 3)
    c.execute('''CREATE TABLE IF NOT EXISTS finance 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, s_id TEXT, income REAL, expense REAL, reason TEXT)''')
    
    # 3. የእቅድ/ኖት ሰንጠረዥ (Step 4)
    c.execute('''CREATE TABLE IF NOT EXISTS plans 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, s_id TEXT, title TEXT, note TEXT)''')
    
    # 4. የትምህርት ውጤት ሰንጠረዥ (Step 6)
    c.execute('''CREATE TABLE IF NOT EXISTS results 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, s_id TEXT, year TEXT, course TEXT, teacher TEXT, grade TEXT)''')
    
    # 5. ሚዲያ ሰንጠረዥ (Step 7)
    c.execute('''CREATE TABLE IF NOT EXISTS media 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, s_id TEXT, file_path TEXT, file_type TEXT)''')
    
    conn.commit()
    conn.close()

# የገጹ ዲዛይን (CSS)
HTML_LAYOUT = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wollo Students Management System</title>
    <style>
        body { font-family: 'Arial', sans-serif; background: #f0f2f5; margin: 0; padding: 10px; }
        .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .step { display: none; }
        .step.active { display: block; }
        h2 { color: #1a73e8; border-bottom: 2px solid #e8f0fe; padding-bottom: 10px; }
        input, textarea, select { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background: #f8f9fa; }
        .btn-row { display: flex; justify-content: space-between; margin-top: 20px; }
        .btn { padding: 12px 25px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
        .next { background: #1a73e8; color: white; }
        .prev { background: #6c757d; color: white; }
        .save { background: #28a745; color: white; width: 100%; }
        .delete-btn { background: #dc3545; color: white; padding: 5px 10px; font-size: 12px; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">{{content}}</div>
    <script>
        let currentStep = 1;
        function showStep(n) {
            document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
            document.getElementById('step' + n).classList.add('active');
            currentStep = n;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    content = '<h1>እንኳን ደህና መጡ!</h1><a href="/login"><button class="btn next">ግባ (Login)</button></a>'
    return render_template_string(HTML_LAYOUT.replace('{{content}}', content))

@app.route('/login', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        s_id = request.form.get('student_id')
        code = request.form.get('access_code')
        
        conn = sqlite3.connect('wollo_final.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE student_id = ? AND access_code = ?", (s_id, code))
        user = c.fetchone()
        
        if user:
            # ሁሉንም መረጃዎች ከየሰንጠረዡ ማምጣት
            c.execute("SELECT * FROM finance WHERE s_id = ?", (s_id,))
            finances = c.fetchall()
            c.execute("SELECT * FROM plans WHERE s_id = ?", (s_id,))
            plans = c.fetchall()
            c.execute("SELECT * FROM results WHERE s_id = ?", (s_id,))
            results = c.fetchall()
            conn.close()

            content = f'''
            <form action="/save_all" method="POST" enctype="multipart/form-data">
                <input type="hidden" name="s_id" value="{user[14]}">
                
                <div id="step1" class="step active">
                    <h2>ደረጃ 1: የግል መረጃ</h2>
                    <input type="text" name="f_name" value="{user[1]}" placeholder="ስም">
                    <input type="text" name="l_name" value="{user[2]}" placeholder="የአባት ስም">
                    <input type="text" name="g_name" value="{user[3]}" placeholder="የአያት ስም">
                    <label>የትውልድ ዘመን (ቀን/ወር/ዓመት/እለት)</label>
                    <div style="display:flex; gap:5px;">
                        <input type="text" name="b_day" value="{user[6]}" placeholder="ቀን">
                        <input type="text" name="b_month" value="{user[5]}" placeholder="ወር">
                        <input type="text" name="b_year" value="{user[4]}" placeholder="ዓመት">
                        <input type="text" name="b_week" value="{user[7]}" placeholder="እለት">
                    </div>
                    <div class="btn-row"><button type="button" class="btn next" onclick="showStep(2)">Next »</button></div>
                </div>

                <div id="step2" class="step">
                    <h2>ደረጃ 2: ዜግነትና አድራሻ</h2>
                    <input type="text" name="nat" value="{user[8]}" placeholder="ዜግነት">
                    <input type="text" name="reg" value="{user[9]}" placeholder="ክልል">
                    <input type="text" name="keb" value="{user[10]}" placeholder="ቀበሌ">
                    <div class="btn-row">
                        <button type="button" class="btn prev" onclick="showStep(1)">« Previous</button>
                        <button type="button" class="btn next" onclick="showStep(3)">Next »</button>
                    </div>
                </div>

                <div id="step3" class="step">
                    <h2>ደረጃ 3: ገቢና ወጪ</h2>
                    <table>
                        <tr><th>ገቢ</th><th>ወጪ</th><th>ምክንያት</th></tr>
            '''
            for f in finances:
                content += f"<tr><td>{f[2]}</td><td>{f[3]}</td><td>{f[4]}</td></tr>"
            
            content += '''
                    </table>
                    <p>አዲስ መዝግብ፡</p>
                    <input type="number" name="inc" placeholder="ገቢ">
                    <input type="number" name="exp" placeholder="ወጪ">
                    <input type="text" name="reason" placeholder="ምክንያት">
                    <div class="btn-row">
                        <button type="button" class="btn prev" onclick="showStep(2)">« Previous</button>
                        <button type="button" class="btn next" onclick="showStep(4)">Next »</button>
                    </div>
                </div>

                <div id="step4" class="step">
                    <h2>ደረጃ 4: እቅድና ማስታወሻ</h2>
                    <input type="text" name="plan_title" placeholder="የእቅድ ርዕስ">
                    <textarea name="plan_note" placeholder="ዝርዝር እቅድ..."></textarea>
                    <div class="btn-row">
                        <button type="button" class="btn prev" onclick="showStep(3)">« Previous</button>
                        <button type="button" class="btn next" onclick="showStep(5)">Next »</button>
                    </div>
                </div>

                <div id="step5" class="step">
                    <h2>ደረጃ 5: የህይወት ታሪክ</h2>
                    <textarea name="bio" style="height:200px;">{user[11]}</textarea>
                    <div class="btn-row">
                        <button type="button" class="btn prev" onclick="showStep(4)">« Previous</button>
                        <button type="button" class="btn next" onclick="showStep(6)">Next »</button>
                    </div>
                </div>

                <div id="step6" class="step">
                    <h2>ደረጃ 6: የትምህርት ውጤት</h2>
                    <input type="text" name="r_year" placeholder="ዓመተ ምህረት">
                    <input type="text" name="r_course" placeholder="የኮርሱ ስም">
                    <input type="text" name="r_teacher" placeholder="የመምህሩ ስም">
                    <input type="text" name="r_grade" placeholder="ውጤት">
                    <div class="btn-row">
                        <button type="button" class="btn prev" onclick="showStep(5)">« Previous</button>
                        <button type="button" class="btn next" onclick="showStep(7)">Next »</button>
                    </div>
                </div>

                <div id="step7" class="step">
                    <h2>ደረጃ 7: ፎቶና ቪዲዮ</h2>
                    <input type="file" name="media_file">
                    <p>የፕሮፋይል ፎቶ ቀይር፡</p>
                    <input type="file" name="p_photo">
                    <div class="btn-row">
                        <button type="button" class="btn prev" onclick="showStep(6)">« Previous</button>
                        <button type="submit" class="btn save">ሁሉንም መረጃ አስቀምጥ</button>
                    </div>
                </div>
            </form>
            '''
            return render_template_string(HTML_LAYOUT.replace('{{content}}', content))
        else:
            return "ስህተት! ተመለስ።"
            
    return render_template_string(HTML_LAYOUT.replace('{{content}}', login_form()))

def login_form():
    return '<h2>ይግቡ</h2><form method="POST"><input name="student_id" placeholder="ID"><input name="access_code" type="password" placeholder="Code"><button type="submit" class="btn next">ግባ</button></form>'

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

