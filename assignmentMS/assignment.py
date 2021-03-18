from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/assignment'#environ.get('dbURL') #'mysql+mysqlconnector://is213@localhost:7777/book' #environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
 
class Assignment(db.Model):
    __tablename__ = 'assignment'
    assignmentId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(64), nullable=False)
    expectedPrice = db.Column(db.Float(precision=2), nullable=False)
    preferredDay = db.Column(db.Integer, nullable=False)
    tutorId = db.Column(db.Integer, default=0)
 
    def __init__(self, assignmentId, userId, subject, location, expectedPrice, preferredDay, tutorId):
        self.assignmentId = assignmentId
        self.userId = userId
        self.subject = subject
        self.location = location
        self.expectedPrice = expectedPrice
        self.preferredDay = preferredDay
        self.tutorId = tutorId
 
    def json(self):
        return {"assignmentId": self.assignmentId, "userId": self.userId, "subject": self.subject, "location": self.location, "expectedPrice": self.expectedPrice, "preferredDay": self.preferredDay, "tutorId": self.tutorId}

@app.route("/assignment")
def get_all():
    return jsonify({"assignments": [assignment.json() for assignment in Assignment.query.all()]})

@app.route("/assignment/<int:assignmentId>")
def find_by_assignmentId(assignmentId):
    assignment = Assignment.query.filter_by(assignmentId=assignmentId).first()
    if assignment:
        return jsonify(assignment.json())
    return jsonify({"message": "Book not found."}), 404

@app.route("/assignment/<int:assignmentId>", methods=['POST'])
def create_assignment(assignmentId):
    if (Assignment.query.filter_by(assignmentId=assignmentId).first()):
        return jsonify({"message": "An assignment with the ID '{}' already exists.".format(assignmentId)}), 400
 
    data = request.get_json()
    assignment = Assignment(assignmentId, **data)
 
    try:
        db.session.add(assignment)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the assignment."}), 500
 
    return jsonify(assignment.json()), 201

@app.route("/assignment/<int:assignmentId>", methods=['PUT'])
def update_assignment(assignmentId):
    try:
        assignment = Assignment.query.filter_by(order_id=order_id).first()
        if not assignment:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "assignmentId": assignmentId
                    },
                    "message": "Order not found."
                }
            ), 404

        # update status
        data = request.get_json()
        if data['status']:
            assignment.status = data['status']
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": assignment.json()
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "assignmentId": assignmentId
                },
                "message": "An error occurred while updating the order. " + str(e)
            }
        ), 500
 
@app.route("/assignment/<int:assignmentId>", methods=['DELETE'])
def delete_assignment(assignmentId):
    assignment = Assignment.query.filter_by(assignmentId=assignmentId).first()
    if assignment:
        db.session.delete(assignment)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "assignmentId": assignmentId
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "assignmentId": assignmentId
            },
            "message": "Assignment not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)