from flask import Flask, request

flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = '%*sW$Vt9OZ$D%eQEY<$7cW.W07MkZAsCCF^l(Y0`5h0ZW#[v;vf0j*.c=:~e}n4'

@flask_app.route('/comp4337/cbf/upload', methods=['POST'])
def cbf_upload():
    pass

@flask_app.route('/comp4337/qbf/query', methods=['POST'])
def qbf_query():
    pass

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True, port=55000, use_reloader=True)