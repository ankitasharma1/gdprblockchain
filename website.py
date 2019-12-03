from flask import Flask, request, render_template, jsonify, redirect

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/blockchain', methods=['GET', 'POST'])
def blockchain():
    if request.method == 'POST':
        # do things with params
        pass
    else:
        return render_template('blockchain.html')


@app.route('/demo', methods=['GET'])
def demo():
    return render_template('demo.html')


@app.route('/dashboard/<entity_type>/<name>', methods=['GET', 'POST'])
def dashboard(entity_type, name):
    if request.method == 'GET':
        # TODO: get more info based upon these values and send it into render
        #       template below
        return render_template('dashboard.html', entity_type=entity_type, name=name)
    elif request.method == 'POST':
        req_dict = request.get_json()
        response = None
        if entity_type.lower() == 'physician':
            # TODO: do something with name and get commands from req_dict
            #       then return a json response so we can use jquery to update
            #       the page
            return jsonify(response)
        elif entity_type.lower() == 'patient':
            # TODO: do something with name and get commands from req_dict
            #       then return a json response so we can use jquery to update
            #       the page
            return jsonify(response)
        elif entity_type.lower() == 'hospital':
            # TODO: do something with name and get commands from req_dict
            #       then return a json response so we can use jquery to update
            #       the page
            return jsonify(response)
        else:
            # TODO: handle bad request
            return jsonify(response)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
