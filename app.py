from flask import Flask, render_template, request

app = Flask(__name__)

# ተማሪዎች የሚሞሉት ፎርም (ከምስሉ ላይ የቀጠለ)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Wollo Registration System</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input { padding: 10px; margin: 10px 0; width: 100%; border: 1px solid #ccc; }
        button { padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h2>የተማሪዎች ምዝገባ</h2>
        <form method="POST">
            <input type="text" name="name" placeholder="ሙሉ ስም" required>
            <input type="text" name="id" placeholder="የተማሪ መታወቂያ (ID)" required>
            <button type="submit">መዝግብ</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # ተማሪው የላከውን ዳታ እዚህ ጋር እንቀበላለን
        student_name = request.form.get('name')
        student_id = request.form.get('id')
        
        # ለጊዜው ስክሪኑ ላይ እናሳየው (በኋላ ወደ Database መቀየር እንችላለን)
        return f"ተማሪ {student_name} (ID: {student_id}) በትክክል ተመዝግቧል!"
    
    return HTML_TEMPLATE

if __name__ == '__main__':
    app.run(debug=True)

