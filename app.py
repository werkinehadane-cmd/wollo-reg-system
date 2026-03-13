from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    # index.html በ templates ፎልደር ውስጥ መሆኑን ያረጋግጣል
    return render_template('index.html')

if __name__ == '__main__':
    # Render ላይ እንዲሰራ ይህ መስመር የግድ ያስፈልጋል
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

