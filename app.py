from flask import Flask, render_template_string, request

app = Flask(__name__)

# ቀላል የዲዛይን እና የኤችቲኤምኤል (HTML) ኮድ
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Wollo Registration System</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f4; }
        .container { background: white; padding: 20px; border-radius: 10px; display: inline-block; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }
        input { padding: 10px; margin: 10px; border: 1px solid #ccc; border-radius: 5px; }
        button { padding: 10px 20px; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h2>እንኳን ወደ ወሎ ምዝገባ ሲስተም በሰላም መጡ</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="ሙሉ ስምዎን ያስገቡ" required>
            <br>
            <button type="submit">ይመዝገቡ</button>
        </form>
        {% if name %}
            <p style="color: green; font-weight: bold;">እናመሰግናለን {{ name }}! ምዝገባዎ ተሳክቷል።</p>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    name = None
    if request.method == 'POST':
        name = request.form.get('username')
    return render_template_string(HTML_TEMPLATE, name=name)

if __name__ == '__main__':
    app.run(debug=True)
