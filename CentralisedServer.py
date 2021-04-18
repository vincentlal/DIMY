from flask import Flask, request, jsonify
import base64
from bitarray import bitarray

flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = '%*sW$Vt9OZ$D%eQEY<$7cW.W07MkZAsCCF^l(Y0`5h0ZW#[v;vf0j*.c=:~e}n4'

uploaded_cbfs = []

@flask_app.route('/comp4337/cbf/upload', methods=['POST'])
def cbf_upload():
    jsonContent = request.json
    CBF = None
    try:
        CBF = jsonContent['CBF']
    except KeyError:
        return jsonify({
            "result": "Failed",
            "message": "please check your CBF"
        }), 200
    try:
        decodedCBF = base64.b64decode(CBF)
        CBFBitArray = bitarray(decodedCBF)
    except Exception:
        return jsonify({'error' : 'Unable to decode CBF', 'result' : 'Failed', 'message' : 'please check your CBF'}), 200
    uploaded_cbfs.append(CBFBitArray)
    return jsonify({'result' : 'Success', 'message' : 'upload CBF success'}), 200

@flask_app.route('/comp4337/qbf/query', methods=['POST'])
def qbf_query():
    jsonContent = request.json
    QBF = None
    try:
        QBF = jsonContent['QBF']
    except KeyError:
        return jsonify({
            "result": "Failed",
            "message": "please check your QBF"
        }), 200
    try:
        decodedQBF = base64.b64decode(QBF)
        QBFBitArray = bitarray(decodedQBF)
    except Exception:
        return jsonify({
            "timestamp": "2021-03-22T02:10:13.257+00:00",
            "status": 400,
            "error": "Bad Request",
            "message": "",
            "path": "/comp4337/cbf/upload"
        }), 400
    for cbf in uploaded_cbfs:
        bitwise_AND = cbf & QBFBitArray
        if (bitwise_AND.count() > 0):
            return jsonify({
                "result" : "Match.",
                "message" : "You are potentially at risk. Please consult a health official, self-isolate and do a COVID-19 test at your earliest."
            }), 200
    return jsonify({
        "result" : "No Match.",
        "message" : "You are safe."
    }), 200

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True, port=55000, use_reloader=True)