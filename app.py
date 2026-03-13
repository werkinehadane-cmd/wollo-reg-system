
from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    # ከታች ያለው መስመር የግድ 4 ባዶ ቦታ (Spaces) ገባ ማለት አለበት
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # ከታች ያለው መስመር የግድ 4 ባዶ ቦታ (Spaces) ገባ ማለት አለበት
    app.run(host='0.0.0.0', port=port)
