from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # ይህ መስመር በ templates ውስጥ ያለውን index.html እንዲከፍት ያደርገዋል
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
