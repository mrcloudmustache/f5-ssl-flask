from flask import Flask, request, jsonify, send_from_directory
from tinydb import TinyDB, Query

app = Flask(__name__)

# Initialize the database
db = TinyDB('ssl_certificates.json')

class SSLCertificate:
    def __init__(self, common_name, sans, vip_name, device_name):
        self.common_name = common_name
        self.sans = sans
        self.vip_name = vip_name
        self.device_name = device_name

    def to_dict(self):
        return {
            'common_name': self.common_name,
            'sans': self.sans,
            'vip_name': self.vip_name,
            'device_name': self.device_name
        }

def add_ssl_certificate(common_name, sans, vip_name, device_name):
    cert = SSLCertificate(common_name, sans, vip_name, device_name)
    db.insert(cert.to_dict())

def get_ssl_certificate_by_common_name(common_name):
    Cert = Query()
    results = db.search(Cert.common_name == common_name)
    return results

def get_all_ssl_certificates():
    return db.all()

def delete_ssl_certificate_by_common_name(common_name):
    Cert = Query()
    db.remove(Cert.common_name == common_name)

@app.route('/add_certificate', methods=['POST'])
def add_certificate():
    data = request.json
    add_ssl_certificate(
        common_name=data['common_name'],
        sans=data['sans'],
        vip_name=data['vip_name'],
        device_name=data['device_name']
    )
    return jsonify({"message": "Certificate added successfully"}), 201

@app.route('/certificates', methods=['GET'])
def view_certificates():
    common_name = request.args.get('common_name')
    if common_name:
        certificates = get_ssl_certificate_by_common_name(common_name)
    else:
        certificates = get_all_ssl_certificates()
    return jsonify(certificates), 200

@app.route('/delete_certificate', methods=['DELETE'])
def delete_certificate():
    data = request.json
    common_name = data['common_name']
    delete_ssl_certificate_by_common_name(common_name)
    return jsonify({"message": "Certificate deleted successfully"}), 200

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
