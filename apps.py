
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://josua:123@localhost:3306/restapiflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

###Models####
class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(20))
    alamat = db.Column(db.String(100))
    notlpn = db.Column(db.String(20))
    
    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,nama,alamat,notlpn):
        self.nama = nama
        self.alamat = alamat
        self.notlpn = notlpn
    def __repr__(self):
        return '' % self.id
db.create_all()

class CustomerSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Customer
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    nama = fields.String(required=True)
    alamat = fields.String(required=True)
    notlpn = fields.String(required=True)

@app.route('/customer', methods = ['GET'])
def index():
    get_customers = Customer.query.all()
    customer_schema = CustomerSchema(many=True)
    customer = customer_schema.dump(get_customers)
    return make_response(jsonify({"customer": customer}))

@app.route('/customer/<id>', methods = ['GET'])
def get_customer_by_id(id):
    get_customer = Customer.query.get(id)
    customer_schema = CustomerSchema()
    customer = customer_schema.dump(get_customer)
    return make_response(jsonify({"customer": customer}))

@app.route('/customer/<id>', methods = ['PUT'])
def update_customer_by_id(id):
    data = request.get_json()
    get_customer = Customer.query.get(id)
    if data.get('nama'):
        get_customer.nama = data['nama']
    if data.get('alamat'):
        get_customer.alamat = data['alamat']
    if data.get('notlpn'):
        get_customer.notlpn = data['notlpn']
        db.session.add(get_customer)
    db.session.commit()
    customer_schema = CustomerSchema(only=['id', 'nama', 'alamat','notlpn'])
    customer = customer_schema.dump(get_customer)
    return make_response(jsonify({"customer": customer}))

@app.route('/customers/<id>', methods = ['DELETE'])
def delete_customer_by_id(id):
    get_customer = Customer.query.get(id)
    db.session.delete(get_customer)
    db.session.commit()
    return make_response("data terhapus",204)

@app.route('/customers', methods = ['POST'])
def create_customer():
    data = request.get_json()
    customer_schema = CustomerSchema()
    customer = customer_schema.load(data)
    result = customer_schema.dump(customer.create())
    return make_response(jsonify({"customer": result}),200)

if __name__ == "__main__":
    app.run(debug=True)
