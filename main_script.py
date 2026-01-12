from flask import Flask, render_template


site = Flask(__name__)

@site.route('/')
def index():
    return render_template("index.html")

@site.route('/execute_script')
def execute_script():
    return "Python script executed!"

if __name__ == '__main__':
    site.run(debug=True, host='0.0.0.0')
