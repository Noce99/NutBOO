from flask import Flask, request, jsonify
from flask_cors import CORS
from get_info_gps import GpsLivelox
app = Flask(__name__)
CORS(app)
live_gps = GpsLivelox()


@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'Ciao dal server Python!'}
    return jsonify(data)


@app.route("/live_gps", methods=["GET"])
def live_gps_aa():
    data = {"lat": live_gps.lat, "lon": live_gps.lon}
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
    live_gps.thread.start()
    print("After the thread!")
    app.run(host="0.0.0.0", ssl_context=('cert1.pem', 'privkey1.pem'), port=4989)


