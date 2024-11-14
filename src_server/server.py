from flask import Flask, request, jsonify
from flask_cors import CORS
from get_info_gps import GpsLivelox
app = Flask(__name__)
CORS(app)


@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'Ciao dal server Python!'}
    return jsonify(data)


@app.route('/api/data', methods=['POST'])
def post_data():
    content = request.json
    response = {'received': content}
    return jsonify(response)


@app.route('/login', methods=['POST'])
def post_login():
    content = request.json
    print(content)
    response = {'received': content}
    return jsonify(response)


if __name__ == '__main__':
    # app.run(port=4989)
    my_gps = GpsLivelox()
    my_gps.listen_forever()
