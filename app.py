
from flask import Flask, render_template_string, request
import sqlite3

app = Flask(__name__)

# ዳታቤዝ ለመፍጠር እና ሰንጠረዥ ለማዘጋጀት
def init_db():
    conn = sqlite3.connect('wollo_university.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, student_id TEXT, age TEXT, 
                  birth_place TEXT, nationality TEXT, 
                  religion TEXT, access_code TEXT, biography TEXT)''')
    conn.commit()
    conn.close()

# HTML ገጽ (ፎርሙን ያካተተ)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <title>Wollo Registration System</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }
        .container { background: white; padding: 20px; border-radius: 8px; max-width: 500px; margin: auto; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h2 { text-align: center; color: #2c3e50; }
        input, textarea, select { width: 95%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
        button { padding: 12px; width: 100%; background-color: #27ae60; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #219150; }
        .success { color: green; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>የወሎ ዩኒቨርሲቲ ተማሪዎች ምዝገባ</h2>
        {% if msg %} <p class="success">{{ msg }}</p> {% endif %}
        <form method="POST">
            <input type="text" name="name" placeholder="ሙሉ ስም" required>
            <input type="text" name="student_id" placeholder="መታወቂያ (ID)" required>
            <input type="number" name="age" placeholder="እድሜ" required>
            <input type="text" name="birth_place" placeholder="የትውልድ ቦታ" required>
            <select name="nationality">
                <option value="ኢትዮጵያዊ">ኢትዮጵያዊ</option>
                <option value="ሌላ">ሌላ</option>
            </select>
            <input type="text" name="religion" placeholder="ሃይማኖት" required>
            <input type="password" name="access_code" placeholder="ለራስህ ሚስጥራዊ ኮድ ስጥ" required>
            <textarea name="biography" placeholder="ለህይወቴ ይጠቅመኛል የምትለው የግል ታሪክ (Biography)..." rows="4"></textarea>
            <button type="submit">በስኬት መዝግብ</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    msg = None
    if request.method == 'POST':
        name = request.form.get('name')
        s_id = request.form.get('student_id')
        age = request.form.get('age')
        birth_place = request.form.get('birth_place')
        nat = request.form.get('nationality')
        rel = request.form.get('religion')
        code = request.form.get('access_code')
        bio = request.form.get('biography')

        conn = sqlite3.connect('wollo_university.db')
        c = conn.cursor()
        c.execute("INSERT INTO students (name, student_id, age, birth_place, nationality, religion, access_code, biography) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (name, s_id, age, birth_place, nat, rel, code, bio))
        conn.commit()
        conn.close()
        msg = f"ተማሪ {name} በትክክል ተመዝግቧል!"

    return render_template_string(HTML_TEMPLATE, msg=msg)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
