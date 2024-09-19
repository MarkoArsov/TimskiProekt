from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///real_estate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String, nullable=True)
    code = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    municipality = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    surfacearea = db.Column(db.String, nullable=True)
    numberofrooms = db.Column(db.Integer, nullable=True)
    numberofsleepingroms = db.Column(db.Integer, nullable=True)
    floornumber = db.Column(db.Integer, nullable=True)
    interior = db.Column(db.String, nullable=True)
    numberofbathrooms = db.Column(db.Integer, nullable=True)
    balcony = db.Column(db.String, nullable=True)
    yard = db.Column(db.String, nullable=True)
    airconditioning = db.Column(db.String, nullable=True)
    heating = db.Column(db.String, nullable=True)
    propertysheet = db.Column(db.String, nullable=True)
    price = db.Column(db.String, nullable=True)
    deposit = db.Column(db.String, nullable=True)
    commission = db.Column(db.String, nullable=True)
    elevator = db.Column(db.String, nullable=True)
    newbuilding = db.Column(db.String, nullable=True)
    shortstay = db.Column(db.String, nullable=True)
    electricheating = db.Column(db.String, nullable=True)
    orientation = db.Column(db.String, nullable=True)
    kitchenappliances = db.Column(db.String, nullable=True)
    yearofconstruction = db.Column(db.String, nullable=True)
    renovated = db.Column(db.String, nullable=True)
    parking = db.Column(db.String, nullable=True)
    basement = db.Column(db.String, nullable=True)
    internet = db.Column(db.String, nullable=True)
    cabletv = db.Column(db.String, nullable=True)
    students = db.Column(db.String, nullable=True)


with app.app_context():
    db.create_all()

@app.route('/api/property', methods=['POST'])
def create_properties():
    data = request.json 
    for property_data in data:
        new_property = Property(**property_data)
        db.session.add(new_property)
    db.session.commit()


    return jsonify({
        "message": "All property data saved successfully",
        "saved_count": len(data)
    }), 201


@app.route('/api/property', methods=['GET'])
def get_properties():
    properties = Property.query.all()
    property_list = []
    for prop in properties:
        property_dict = {
            "id": prop.id,
            "link": prop.link,
            "code": prop.code,
            "description": prop.description,
            "municipality": prop.municipality,
            "location": prop.location,
            "surfacearea": prop.surfacearea,
            "numberofrooms": prop.numberofrooms,
            "numberofsleepingroms": prop.numberofsleepingroms,
            "floornumber": prop.floornumber,
            "interior": prop.interior,
            "numberofbathrooms": prop.numberofbathrooms,
            "balcony": prop.balcony,
            "yard": prop.yard,
            "airconditioning": prop.airconditioning,
            "heating": prop.heating,
            "propertysheet": prop.propertysheet,
            "price": prop.price,
            "deposit": prop.deposit,
            "commission": prop.commission,
            "elevator": prop.elevator,
            "newbuilding": prop.newbuilding,
            "shortstay": prop.shortstay,
            "electricheating": prop.electricheating,
            "orientation": prop.orientation,
            "kitchenappliances": prop.kitchenappliances,
            "yearofconstruction": prop.yearofconstruction,
            "renovated": prop.renovated,
            "parking": prop.parking,
            "basement": prop.basement,
            "internet": prop.internet,
            "cabletv": prop.cabletv,
            "students": prop.students
        }
        property_list.append(property_dict)
   
    return jsonify(property_list), 200


@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "API is running!"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



