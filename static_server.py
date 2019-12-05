from flask import Flask, render_template

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/demo', methods=['GET'])
def demo():
    return render_template('demo.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
