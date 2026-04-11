
from flask import Flask, render_template_string, request
import sqlite3

app = Flask(__name__)

# ዳታቤዝ ዝግጅት (ሁሉንም መረጃ እንዲይዝ)
def init_db():
    conn = sqlite3.connect('wollo_v2.db')

    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, student_id TEXT, age TEXT, 
                  birth_place TEXT, nationality TEXT, 
                  religion TEXT, access_code TEXT, biography TEXT)''')
    conn.commit()
    conn.close()
init_db()
# የዌብሳይቱ ገጽታ (HTML/CSS)
HTML_LAYOUT = '''
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wollo Student Portal</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; margin: 0; padding: 20px; }
        .container { background: white; padding: 30px; border-radius: 12px; max-width: 500px; margin: auto; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h2 { text-align: center; color: #1a73e8; }
        input, textarea, select { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background-color: #1a73e8; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; }
        button:hover { background-color: #1557b0; }
        .nav { text-align: center; margin-bottom: 20px; }
        .nav a { margin: 0 10px; text-decoration: none; color: #1a73e8; font-weight: bold; }
        .message { background: #d4edda; color: #155724; padding: 10px; border-radius: 5px; text-align: center; }
    </style>
</head>
<body>
    <div class="nav">
        <a href="/">መመዝገቢያ</a> | <a href="/login">የግል ሳጥን (Lock)</a>
    </div>
    <div class="container">
        {{ content | safe }}
    </div>
</body>
</html>
'''

# 1. የምዝገባ ገጽ (Home)
@app.route('/', methods=['GET', 'POST'])
def index():
    msg = ""
    if request.method == 'POST':
        name = request.form.get('name')
        s_id = request.form.get('student_id')
        age = request.form.get('age')
        code = request.form.get('access_code')
        bio = request.form.get('biography')
        
        conn = sqlite3.connect('wollo_v2.db')

        c = conn.cursor()
        c.execute("INSERT INTO students (name, student_id, age, access_code, biography) VALUES (?, ?, ?, ?, ?)",
                  (name, s_id, age, code, bio))
        conn.commit()
        conn.close()
        msg = f'<div class="message">ተማሪ {name} በስኬት ተመዝግቧል!</div>'

    form_html = f'''
        {msg}
        <h2>የተማሪዎች ምዝገባ</h2>
        <form method="POST">
            <input type="text" name="name" placeholder="ሙሉ ስም" required>
            <input type="text" name="student_id" placeholder="መታወቂያ (ID)" required>
            <input type="number" name="age" placeholder="እድሜ" required>
            <input type="password" name="access_code" placeholder="ለመቆለፊያ የሚሆን ሚስጥራዊ ኮድ" required>
            <textarea name="biography" placeholder="ለህይወትህ የሚጠቅም ሚስጥራዊ ታሪክ ወይም አላማ እዚህ ጻፍ..." rows="5"></textarea>
            <button type="submit">በስኬት መዝግብ</button>
        </form>
    '''
    return render_template_string(HTML_LAYOUT, content=form_html)

# 2. የመግቢያ እና የግል መረጃ ማያ ገጽ (Login/Private Dashboard)
@app.route('/login', methods=['GET', 'POST'])
def login():
    content = ""
    if request.method == 'POST':
        s_id = request.form.get('student_id')
        code = request.form.get('access_code')
        
        conn = sqlite3.connect('wollo_v2.db')

        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE student_id=? AND access_code=?", (s_id, code))
        user = c.fetchone()
        conn.close()
        
        if user:
            content = f'''
                <h2>የ{user[1]} የግል ማስታወሻ</h2>
                <div style="background: #f9f9f9; padding: 15px; border-left: 5px solid #1a73e8;">
                    <p><b>መታወቂያ:</b> {user[2]}</p>
                    <p><b>እድሜ:</b> {user[3]}</p>
                    <p><b>የተቆለፈ ታሪክህ:</b></p>
                    <p style="white-space: pre-wrap;">{user[8]}</p>
                </div>
                <br><a href="/login"><button style="background-color: #6c757d;">ውጣ (Logout)</button></a>
            '''
        else:
            content = '<p style="color:red; text-align:center;">ስህተት! መታወቂያ ወይም ኮድ አልተዛመደም።</p>' + login_form()
    else:
        content = login_form()
        
    return render_template_string(HTML_LAYOUT, content=content)

def login_form():
    return '''
        <h2>የግል ሳጥንህን ክፈት</h2>
        <form method="POST">
            <input type="text" name="student_id" placeholder="መታወቂያ (ID)" required>
            <input type="password" name="access_code" placeholder="ሚስጥራዊ ኮድ" required>
            <button type="submit">ቆልፉን ክፈት</button>
        </form>
    '''

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
