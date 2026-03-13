from flask import Flask, render_template_string, request

app = Flask(__name__)

# የዌብሳይቱ ገጽታ (HTML/CSS)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <title>Wollo Registration System</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; display: flex; justify-content: center; padding: 50px; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); width: 100%; max-width: 400px; }
        h2 { text-align: center; color: #333; }
        input { padding: 12px; margin: 10px 0; width: 100%; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
        button { padding: 12px; width: 100%; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #218838; }
        .result { margin-top: 20px; padding: 10px; background-color: #e2f3f5; border-radius: 5px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h2>የወሎ ዩኒቨርሲቲ ተማሪዎች ምዝገባ</h2>
        <form method="POST">
            <input type="text" name="name" placeholder="ሙሉ ስም" required>
            <input type="text" name="id" placeholder="የተማሪ መታወቂያ (ID)" required>
            <button type="submit">መዝግብ</button>
        </form>

        {% if name %}
        <div class="result">
            <p style="color: green;">✅ ተማሪ <strong>{{ name }}</strong> በትክክል ተመዝግቧል!</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    if request.method == 'POST':
        # መረጃውን መቀበል
        name = request.form.get('name')
        student_id = request.form.get('id')
        
        # ለጊዜው መረጃውን በሰርቨሩ 'Log' ላይ ያሳየዋል
        print(f"New Registration: {name}, ID: {student_id}")
        
    return render_template_string(HTML_TEMPLATE, name=name)

if __name__ == '__main__':
    app.run(debug=True)
