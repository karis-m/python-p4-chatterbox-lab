from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods= ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messageList = []
        messages = Message.query.order_by(Message.created_at).all()
        for message in messages:
            message_dict = message.to_dict()
            messageList.append(message_dict)

        response = make_response(jsonify(messageList), 200)

        return response
    
    elif request.method == 'POST':
         new_message = Message(
              body = request.form.get("body"),
              username = request.form.get("username"),
         )

         db.session.add(new_message)
         db.session.commit()

         message_to_dict = new_message.to_dict()
         response = make_response(jsonify(message_to_dict), 201)

         return response
         

@app.route('/messages/<int:id>', methods= ['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if request.method == 'PATCH':
        message = Message.query.filter_by(id=id).first()
        for attr in request.form:
            setattr(message, attr, request.form.get(attr))

        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(
                jsonify(message_dict),
                200
            )

        return response

    elif request.method == 'DELETE':
        message = Message.query.filter_by(id=id).first()
        db.session.delete(message)
        db.session.commit()

        response_body = {
                "delete_successful": True,
                "message": "Message deleted."    
            }

        response = make_response(jsonify(response_body), 200)

        return response

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(port=5555)
